import bpy
import bmesh
import math
import os
import json
import shutil
from mathutils import Vector, Euler

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
MIRROR_ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style_antigravity"
OUTPUTS_DIR = os.path.join(ROOT, "outputs")
MIRROR_OUTPUTS_DIR = os.path.join(MIRROR_ROOT, "outputs")
WORK_RENDER_DIR = os.path.join(ROOT, "work", "termos-3d", "renders-v03")

BLEND_PATH = os.path.join(OUTPUTS_DIR, "termos-03-master-semi-realis-v0.3.blend")
HERO_PNG = os.path.join(OUTPUTS_DIR, "termos-03-lookdev-hero-v0.3.png")
PEELED_PNG = os.path.join(OUTPUTS_DIR, "termos-03-lookdev-peeled-v0.3.png")
ANCHORS_JSON = os.path.join(OUTPUTS_DIR, "termos-03-anchors-semi-realis-v0.3.json")

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(MIRROR_OUTPUTS_DIR, exist_ok=True)
os.makedirs(WORK_RENDER_DIR, exist_ok=True)


def srgb_to_linear(c):
    if c <= 0.04045:
        return c / 12.92
    return ((c + 0.055) / 1.055) ** 2.4


def hex_to_linear(hex_str):
    h = hex_str.lstrip("#")
    r = int(h[0:2], 16) / 255.0
    g = int(h[2:4], 16) / 255.0
    b = int(h[4:6], 16) / 255.0
    return (srgb_to_linear(r), srgb_to_linear(g), srgb_to_linear(b))


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for col in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights, bpy.data.curves):
        for item in list(col):
            if item.users == 0:
                col.remove(item)


# ==============================================================================
# 1. SEMI-REALISTIC SHADING & MATERIAL SETUP (SSS, AO/Curvature, Clearcoat, Metal)
# ==============================================================================
def create_semi_real_material(
    name,
    base_hex,
    edge_hex=None,
    roughness=0.35,
    metallic=0.0,
    coat_weight=0.0,
    coat_roughness=0.15,
    sss_weight=0.0,
    sss_radius=(1.0, 0.45, 0.35),
    sss_scale=0.15,
    transmission=0.0,
    ior=1.45,
    anisotropic=0.0,
    emission_hex=None,
    emission_strength=0.0,
    ao_darken=0.22,
):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    bsdf = nodes.get("Principled BSDF")

    base_col = hex_to_linear(base_hex)
    edge_col = hex_to_linear(edge_hex) if edge_hex else (
        min(1.0, base_col[0] * 1.18),
        min(1.0, base_col[1] * 1.18),
        min(1.0, base_col[2] * 1.18),
    )

    ao_node = nodes.new("ShaderNodeAmbientOcclusion")
    ao_node.samples = 16
    ao_node.inputs["Distance"].default_value = 0.80
    ao_node.inputs["Color"].default_value = (*base_col, 1.0)

    lw_node = nodes.new("ShaderNodeLayerWeight")
    lw_node.inputs["Blend"].default_value = 0.25

    mix_fresnel = nodes.new("ShaderNodeMix")
    mix_fresnel.data_type = "RGBA"
    mix_fresnel.inputs["Factor"].default_value = 0.30
    mix_fresnel.inputs["A"].default_value = (*base_col, 1.0)
    mix_fresnel.inputs["B"].default_value = (*edge_col, 1.0)
    links.new(lw_node.outputs["Facing"], mix_fresnel.inputs["Factor"])

    shadow_col = (
        base_col[0] * (1.0 - ao_darken),
        base_col[1] * (1.0 - ao_darken),
        base_col[2] * (1.0 - ao_darken),
    )
    mix_ao = nodes.new("ShaderNodeMix")
    mix_ao.data_type = "RGBA"
    mix_ao.inputs["A"].default_value = (*shadow_col, 1.0)
    links.new(ao_node.outputs["AO"], mix_ao.inputs["Factor"])
    links.new(mix_fresnel.outputs["Result"], mix_ao.inputs["B"])
    links.new(mix_ao.outputs["Result"], bsdf.inputs["Base Color"])

    bsdf.inputs["Roughness"].default_value = roughness
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["IOR"].default_value = ior

    if "Coat Weight" in bsdf.inputs:
        bsdf.inputs["Coat Weight"].default_value = coat_weight
        bsdf.inputs["Coat Roughness"].default_value = coat_roughness

    if "Subsurface Weight" in bsdf.inputs and sss_weight > 0:
        bsdf.inputs["Subsurface Weight"].default_value = sss_weight
        bsdf.inputs["Subsurface Radius"].default_value = sss_radius
        bsdf.inputs["Subsurface Scale"].default_value = sss_scale

    if "Transmission Weight" in bsdf.inputs and transmission > 0:
        bsdf.inputs["Transmission Weight"].default_value = transmission

    if "Anisotropic" in bsdf.inputs and anisotropic > 0:
        bsdf.inputs["Anisotropic"].default_value = anisotropic

    if emission_hex and emission_strength > 0:
        em_col = hex_to_linear(emission_hex)
        bsdf.inputs["Emission Color"].default_value = (*em_col, 1.0)
        bsdf.inputs["Emission Strength"].default_value = emission_strength

    mat.diffuse_color = (*base_col, 1.0)
    return mat


def build_material_library():
    mats = {}
    # 1. Outer Shell: Zojirushi Matte Ice Gray (#73868A -> vibrant satin Ice Gray)
    mats["outer_ice_gray"] = create_semi_real_material(
        "MAT_Outer_IceGray",
        base_hex="#73868A",
        edge_hex="#9BB0B5",
        roughness=0.34,
        metallic=0.15,
        coat_weight=0.32,
        coat_roughness=0.16,
        ao_darken=0.26,
    )
    mats["outer_cut_face"] = create_semi_real_material(
        "MAT_Outer_CutFace",
        base_hex="#A8BDC2",
        edge_hex="#D0E2E6",
        roughness=0.22,
        metallic=0.35,
        coat_weight=0.25,
        ao_darken=0.12,
    )
    # 2. Dark Slate Trim & Neck Collar (with subtle SSS)
    mats["dark_trim"] = create_semi_real_material(
        "MAT_Dark_Slate_Trim",
        base_hex="#263336",
        edge_hex="#405459",
        roughness=0.36,
        metallic=0.06,
        coat_weight=0.22,
        sss_weight=0.18,
        sss_radius=(0.5, 0.5, 0.6),
        sss_scale=0.08,
    )
    # 3. Release Button & Safety Lock Accent
    mats["button_accent"] = create_semi_real_material(
        "MAT_Button_Accent",
        base_hex="#51686D",
        edge_hex="#749096",
        roughness=0.30,
        metallic=0.10,
        coat_weight=0.38,
        sss_weight=0.22,
        sss_radius=(0.6, 0.65, 0.7),
        sss_scale=0.10,
    )
    mats["lock_red_indicator"] = create_semi_real_material(
        "MAT_Lock_Red_Indicator",
        base_hex="#E04836",
        edge_hex="#FF7A6B",
        roughness=0.22,
        coat_weight=0.45,
        sss_weight=0.40,
        emission_hex="#E04836",
        emission_strength=0.35,
    )
    # 4. Outer & Inner Stainless Steel SUS304
    mats["stainless_outer"] = create_semi_real_material(
        "MAT_Stainless_Outer_SUS304",
        base_hex="#A4B2BC",
        edge_hex="#D6E2EB",
        roughness=0.22,
        metallic=0.88,
        coat_weight=0.18,
        anisotropic=0.35,
        ao_darken=0.22,
    )
    mats["stainless_inner"] = create_semi_real_material(
        "MAT_Stainless_Inner_SUS304",
        base_hex="#BCC9D2",
        edge_hex="#EAF3FA",
        roughness=0.18,
        metallic=0.90,
        coat_weight=0.22,
        anisotropic=0.42,
        ao_darken=0.18,
    )
    mats["steel_cut_bevel"] = create_semi_real_material(
        "MAT_Steel_Cut_Bevel",
        base_hex="#E4EEF5",
        edge_hex="#FFFFFF",
        roughness=0.14,
        metallic=0.92,
        coat_weight=0.35,
        ao_darken=0.08,
    )
    # 5. Layer 2: Vacuum Chamber Void (Deep Cobalt-Blue Void so the ~2mm vacuum gap pops unmistakably)
    mats["vacuum_void"] = create_semi_real_material(
        "MAT_Vacuum_Chamber_Void",
        base_hex="#15283B",
        edge_hex="#274C6E",
        roughness=0.50,
        metallic=0.18,
        emission_hex="#1D568A",
        emission_strength=0.24,
        ao_darken=0.40,
    )
    # 6. Layer 3: Reflective Copper/Gold Mirror Shield
    mats["copper_gold_mirror"] = create_semi_real_material(
        "MAT_Copper_Gold_Mirror",
        base_hex="#F5AE24",
        edge_hex="#FFE68A",
        roughness=0.08,
        metallic=0.96,
        coat_weight=0.45,
        coat_roughness=0.04,
        anisotropic=0.28,
        emission_hex="#E8920C",
        emission_strength=0.16,
        ao_darken=0.18,
    )
    # 7. Layer 5: Hot Liquid Core 480ml (Translucent Warm Amber Tea/Water with SSS & Thermal Glow)
    mats["hot_liquid"] = create_semi_real_material(
        "MAT_Hot_Liquid_Core",
        base_hex="#EE721B",
        edge_hex="#FFB84D",
        roughness=0.07,
        metallic=0.0,
        coat_weight=0.65,
        coat_roughness=0.04,
        sss_weight=0.60,
        sss_radius=(1.0, 0.58, 0.22),
        sss_scale=0.38,
        transmission=0.48,
        ior=1.333,
        emission_hex="#FF7B19",
        emission_strength=0.48,
        ao_darken=0.12,
    )
    mats["liquid_meniscus"] = create_semi_real_material(
        "MAT_Liquid_Meniscus_Top",
        base_hex="#FFA542",
        edge_hex="#FFDC94",
        roughness=0.05,
        coat_weight=0.80,
        sss_weight=0.45,
        transmission=0.52,
        emission_hex="#FFA542",
        emission_strength=0.62,
    )
    # 8. Silicone Stopper & Seal Gaskets (Pixar-style SSS — Soft Elastic Silicone)
    mats["silicone_stopper_sss"] = create_semi_real_material(
        "MAT_Silicone_Stopper_SSS",
        base_hex="#2B7A57",
        edge_hex="#5CE0A2",
        roughness=0.35,
        metallic=0.0,
        coat_weight=0.26,
        coat_roughness=0.22,
        sss_weight=0.82,
        sss_radius=(0.85, 1.0, 0.65),
        sss_scale=0.26,
        ao_darken=0.20,
    )
    mats["silicone_gasket_warm_sss"] = create_semi_real_material(
        "MAT_Silicone_Gasket_Warm_SSS",
        base_hex="#F2EFE6",
        edge_hex="#FFFFFF",
        roughness=0.32,
        metallic=0.0,
        coat_weight=0.28,
        sss_weight=0.88,
        sss_radius=(1.0, 0.88, 0.72),
        sss_scale=0.30,
        ao_darken=0.15,
    )
    # 9. Polypropylene Mouthpiece / Spout (Warm Ivory with soft SSS)
    mats["mouthpiece_pp"] = create_semi_real_material(
        "MAT_Mouthpiece_Spout_PP",
        base_hex="#F0ECE1",
        edge_hex="#FFFFFF",
        roughness=0.26,
        metallic=0.0,
        coat_weight=0.38,
        sss_weight=0.52,
        sss_radius=(1.0, 0.92, 0.82),
        sss_scale=0.20,
    )
    # 10. Thermal Radiation Bounce Arrows (Glowing stylized 3D energy cues)
    mats["heat_arrow"] = create_semi_real_material(
        "MAT_Thermal_Radiation_Arrow",
        base_hex="#FF5514",
        edge_hex="#FFE066",
        roughness=0.15,
        metallic=0.1,
        emission_hex="#FF6A14",
        emission_strength=2.2,
    )
    # 11. Vacuum Suction Particles (Cool Cyan spheres inside vacuum gap)
    mats["vacuum_particle"] = create_semi_real_material(
        "MAT_Vacuum_Particle_Cyan",
        base_hex="#38BDF8",
        edge_hex="#E0F2FE",
        roughness=0.12,
        emission_hex="#0EA5E9",
        emission_strength=1.8,
    )
    # 12. Seamless Curved Studio Cyclorama Floor/Backdrop (Warm Bright Editorial Paper #F4F1EA)
    mats["studio_floor"] = create_semi_real_material(
        "MAT_Studio_Cyclorama",
        base_hex="#F4F1EA",
        edge_hex="#FAF8F3",
        roughness=0.72,
        metallic=0.0,
        coat_weight=0.04,
        ao_darken=0.10,
    )
    return mats


# ==============================================================================
# 2. SOLID MANIFOLD GEOMETRY BUILDERS WITH BEVEL & SOFTENING
# ==============================================================================
def apply_smooth_and_bevel(obj, bevel_width=0.04, bevel_segments=3):
    for poly in obj.data.polygons:
        poly.use_smooth = True
    if bevel_width > 0:
        mod = obj.modifiers.new("SemiReal_Bevel", "BEVEL")
        mod.width = bevel_width
        mod.segments = bevel_segments
        mod.limit_method = "ANGLE"
        mod.angle_limit = math.radians(32.0)
        mod.harden_normals = False
    return obj


def create_solid_lathe_wall(
    name,
    outer_profile,
    inner_profile,
    start_angle=0.0,
    end_angle=2.0 * math.pi,
    segments=96,
    mat_main=None,
    mat_cut=None,
    bevel_width=0.035,
    parent=None,
):
    loop_pts = list(outer_profile) + list(inner_profile)
    n_loop = len(loop_pts)
    total_angle = end_angle - start_angle
    is_full = math.isclose(total_angle, 2.0 * math.pi, abs_tol=1e-4)
    n_steps = segments if is_full else segments + 1

    verts = []
    for step in range(n_steps):
        frac = step / segments
        ang = start_angle + frac * total_angle
        ca, sa = math.cos(ang), math.sin(ang)
        for r, z in loop_pts:
            verts.append((r * ca, r * sa, z))

    faces = []
    mat_indices = []
    ring_steps = segments if is_full else segments
    for step in range(ring_steps):
        next_step = (step + 1) % segments if is_full else step + 1
        for k in range(n_loop):
            nk = (k + 1) % n_loop
            v0 = step * n_loop + k
            v1 = next_step * n_loop + k
            v2 = next_step * n_loop + nk
            v3 = step * n_loop + nk
            faces.append((v0, v1, v2, v3))
            mat_indices.append(0)

    if not is_full:
        start_cap = tuple(range(n_loop - 1, -1, -1))
        end_offset = (n_steps - 1) * n_loop
        end_cap = tuple(end_offset + k for k in range(n_loop))
        faces.append(start_cap)
        mat_indices.append(1 if mat_cut else 0)
        faces.append(end_cap)
        mat_indices.append(1 if mat_cut else 0)

    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)

    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    if mat_main:
        obj.data.materials.append(mat_main)
    if mat_cut:
        obj.data.materials.append(mat_cut)
        for poly, midx in zip(obj.data.polygons, mat_indices):
            poly.material_index = midx

    apply_smooth_and_bevel(obj, bevel_width=bevel_width, bevel_segments=3)
    if parent:
        obj.parent = parent
    return obj


def create_solid_revolved_core(
    name,
    radius_z_profile,
    start_angle=0.0,
    end_angle=2.0 * math.pi,
    segments=96,
    mat_main=None,
    mat_top=None,
    bevel_width=0.03,
    parent=None,
):
    mesh = bpy.data.meshes.new(name + "_mesh")
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)

    total_angle = end_angle - start_angle
    is_full = math.isclose(total_angle, 2.0 * math.pi, abs_tol=1e-4)
    n_steps = segments if is_full else segments + 1

    verts = []
    n_rings = len(radius_z_profile)
    for j, (r, z) in enumerate(radius_z_profile):
        verts.append((0.0, 0.0, z))
        for i in range(n_steps):
            frac = i / segments
            a = start_angle + frac * total_angle
            verts.append((r * math.cos(a), r * math.sin(a), z))

    stride = n_steps + 1
    faces = []
    mat_indices = []

    for j in range(n_rings - 1):
        for i in range(segments):
            ni = (i + 1) % segments if is_full else i + 1
            a = j * stride + 1 + i
            b = j * stride + 1 + ni
            c = (j + 1) * stride + 1 + ni
            d = (j + 1) * stride + 1 + i
            faces.append((a, b, c, d))
            mat_indices.append(0)

    for i in range(segments):
        ni = (i + 1) % segments if is_full else i + 1
        faces.append((0, 1 + ni, 1 + i))
        mat_indices.append(0)
        top_c = (n_rings - 1) * stride
        faces.append((top_c, top_c + 1 + i, top_c + 1 + ni))
        mat_indices.append(1 if mat_top else 0)

    if not is_full:
        for j in range(n_rings - 1):
            c0 = j * stride
            c1 = (j + 1) * stride
            s0 = j * stride + 1
            s1 = (j + 1) * stride + 1
            faces.append((c0, s0, s1, c1))
            mat_indices.append(0)
            e0 = j * stride + 1 + segments
            e1 = (j + 1) * stride + 1 + segments
            faces.append((c0, c1, e1, e0))
            mat_indices.append(0)

    mesh.from_pydata(verts, [], faces)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    if mat_main:
        obj.data.materials.append(mat_main)
    if mat_top:
        obj.data.materials.append(mat_top)
        for poly, midx in zip(obj.data.polygons, mat_indices):
            poly.material_index = midx

    apply_smooth_and_bevel(obj, bevel_width=bevel_width, bevel_segments=3)
    if parent:
        obj.parent = parent
    return obj


def create_rounded_box(name, location, dimensions, bevel, mat, parent=None):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if mat:
        obj.data.materials.append(mat)
    apply_smooth_and_bevel(obj, bevel_width=bevel, bevel_segments=4)
    if parent:
        obj.parent = parent
    return obj


def create_torus_gasket(name, z_height, major_radius, minor_radius, mat, start_angle=0.0, end_angle=2*math.pi, parent=None):
    outer_prof = []
    ring_pts = 16
    for k in range(ring_pts):
        theta = (k / ring_pts) * 2.0 * math.pi
        r = major_radius + minor_radius * math.cos(theta)
        z = z_height + minor_radius * math.sin(theta)
        outer_prof.append((r, z))
    return create_solid_lathe_wall(
        name,
        outer_profile=outer_prof[:ring_pts//2 + 1],
        inner_profile=outer_prof[ring_pts//2:],
        start_angle=start_angle,
        end_angle=end_angle,
        segments=72,
        mat_main=mat,
        bevel_width=0.015,
        parent=parent,
    )


def create_heat_bounce_arrow(name, z_level, angle_rad, r_inner=1.70, r_mirror=2.60, mat=None, parent=None):
    """
    Creates a clearly visible 3D V-shaped ricochet arrow showing infrared heat radiating
    from the Hot Liquid Core, hitting the exposed Copper/Gold Mirror Shield, and bouncing back!
    """
    curve_data = bpy.data.curves.new(name + "_curve", type="CURVE")
    curve_data.dimensions = "3D"
    curve_data.bevel_depth = 0.085
    curve_data.bevel_resolution = 4
    curve_data.use_fill_caps = True

    spline = curve_data.splines.new("POLY")
    pts = [
        (r_inner * math.cos(angle_rad - 0.10), r_inner * math.sin(angle_rad - 0.10), z_level + 0.65),
        (r_mirror * math.cos(angle_rad), r_mirror * math.sin(angle_rad), z_level),
        (r_inner * math.cos(angle_rad + 0.10), r_inner * math.sin(angle_rad + 0.10), z_level - 0.65),
    ]
    spline.points.add(len(pts) - 1)
    for i, (x, y, z) in enumerate(pts):
        spline.points[i].co = (x, y, z, 1.0)

    obj = bpy.data.objects.new(name, curve_data)
    bpy.context.collection.objects.link(obj)
    if mat:
        obj.data.materials.append(mat)
    if parent:
        obj.parent = parent

    tip_x, tip_y, tip_z = pts[2]
    bpy.ops.mesh.primitive_cone_add(
        vertices=24, radius1=0.18, radius2=0.0, depth=0.38, location=(tip_x, tip_y, tip_z)
    )
    cone = bpy.context.object
    cone.name = name + "_tip"
    direction = Vector(pts[2]) - Vector(pts[1])
    cone.rotation_euler = direction.to_track_quat("Z", "Y").to_euler()
    for poly in cone.data.polygons:
        poly.use_smooth = True
    if mat:
        cone.data.materials.append(mat)
    if parent:
        cone.parent = parent
    return obj


# ==============================================================================
# 3. MASTER MULTI-LAYER CONCENTRIC PEELING TERMOS ASSEMBLY (1:1 ZOJIRUSHI SM-WA48)
# ==============================================================================
def build_semi_realistic_termos(mode="hero"):
    mats = build_material_library()

    root = bpy.data.objects.new("GEO_TERMOS_ROOT", None)
    root.empty_display_type = "PLAIN_AXES"
    root.empty_display_size = 2.0
    bpy.context.collection.objects.link(root)

    is_peeled = (mode == "peeled")

    # --------------------------------------------------------------------------
    # LAYER 1: OUTER SHELL (Matte Ice Gray) — Split into Main Body + Peeled Door Wing
    # --------------------------------------------------------------------------
    grp_outer_left = bpy.data.objects.new("GRP_OUTER_SHELL_LEFT", None)
    grp_outer_right = bpy.data.objects.new("GRP_OUTER_SHELL_RIGHT", None)
    for g in (grp_outer_left, grp_outer_right):
        g.empty_display_type = "ARROWS"
        g.empty_display_size = 1.5
        bpy.context.collection.objects.link(g)
        g.parent = root

    outer_ext_prof = [
        (3.05, 0.00),
        (3.20, 0.14),
        (3.25, 0.35),
        (3.25, 14.85),
        (3.22, 15.55),
        (3.12, 16.15),
        (2.98, 16.65),
        (2.92, 17.00),
    ]
    outer_int_prof = [
        (2.80, 17.00),
        (2.86, 16.65),
        (2.98, 16.15),
        (3.08, 15.55),
        (3.11, 14.85),
        (3.11, 0.45),
        (2.95, 0.22),
        (0.00, 0.22),
        (0.00, 0.00),
    ]

    if not is_peeled:
        create_solid_lathe_wall(
            "GEO_Outer_Shell_Full",
            outer_ext_prof,
            outer_int_prof,
            0.0,
            2.0 * math.pi,
            segments=112,
            mat_main=mats["outer_ice_gray"],
            bevel_width=0.03,
            parent=grp_outer_left,
        )
        create_solid_lathe_wall(
            "GEO_Base_Trim_Full",
            [(3.26, 0.10), (3.26, 0.52)],
            [(3.10, 0.52), (3.10, 0.10)],
            0.0,
            2.0 * math.pi,
            segments=112,
            mat_main=mats["dark_trim"],
            bevel_width=0.02,
            parent=grp_outer_left,
        )
        create_solid_lathe_wall(
            "GEO_Neck_Trim_Full",
            [(2.95, 16.72), (2.95, 17.04)],
            [(2.78, 17.04), (2.78, 16.72)],
            0.0,
            2.0 * math.pi,
            segments=112,
            mat_main=mats["dark_trim"],
            bevel_width=0.02,
            parent=grp_outer_left,
        )
    else:
        # Camera looks from front-right (-Y, slightly +X, around -70 deg).
        # Main Outer Shell covers -12 deg counter-clockwise to 182 deg (leaving the entire front open).
        main_start = math.radians(-12.0)
        main_end = math.radians(182.0)
        # Detached Left Wing Door covers 195 deg to 238 deg, shifted radially outward to the left (-X)
        # so there is a clean physical gap between the peeled wing and the inner layers!
        wing_start = math.radians(196.0)
        wing_end = math.radians(236.0)

        create_solid_lathe_wall(
            "GEO_Outer_Shell_Main",
            outer_ext_prof,
            outer_int_prof,
            main_start,
            main_end,
            segments=72,
            mat_main=mats["outer_ice_gray"],
            mat_cut=mats["outer_cut_face"],
            bevel_width=0.035,
            parent=grp_outer_left,
        )
        create_solid_lathe_wall(
            "GEO_Base_Trim_Main",
            [(3.26, 0.10), (3.26, 0.52)],
            [(3.10, 0.52), (3.10, 0.10)],
            main_start,
            main_end,
            segments=72,
            mat_main=mats["dark_trim"],
            bevel_width=0.02,
            parent=grp_outer_left,
        )
        create_solid_lathe_wall(
            "GEO_Outer_Shell_Detached_Door",
            outer_ext_prof,
            outer_int_prof,
            wing_start,
            wing_end,
            segments=36,
            mat_main=mats["outer_ice_gray"],
            mat_cut=mats["outer_cut_face"],
            bevel_width=0.035,
            parent=grp_outer_right,
        )
        # Shift detached wing door cleanly to the left (-X = -1.65 cm) so the gap is unmistakable
        grp_outer_right.location = (-1.65, -0.35, 0.0)

    # --------------------------------------------------------------------------
    # LAYER 2: VACUUM CHAMBER & OUTER STAINLESS WALL (~2.0mm Schematic Vacuum Gap)
    # --------------------------------------------------------------------------
    vac_outer_ext = [
        (3.02, 0.35),
        (3.09, 0.55),
        (3.09, 14.80),
        (3.03, 15.50),
        (2.90, 16.15),
        (2.76, 16.80),
        (2.18, 17.02),
    ]
    vac_outer_int = [
        (2.08, 17.02),
        (2.64, 16.75),
        (2.78, 16.10),
        (2.91, 15.45),
        (2.97, 14.75),
        (2.97, 0.65),
        (0.00, 0.65),
        (0.00, 0.35),
    ]
    # Stepped Peel Angle 2: Outer stainless wall & Vacuum Void extend further than Outer Shell
    s_angle_vac = math.radians(-26.0) if is_peeled else 0.0
    e_angle_vac = math.radians(196.0) if is_peeled else 2.0 * math.pi

    create_solid_lathe_wall(
        "GEO_Outer_Stainless_Wall",
        vac_outer_ext,
        vac_outer_int,
        s_angle_vac,
        e_angle_vac,
        segments=84,
        mat_main=mats["stainless_outer"],
        mat_cut=mats["steel_cut_bevel"],
        bevel_width=0.03,
        parent=root,
    )

    vac_void_ext = [
        (2.95, 0.68),
        (2.95, 14.70),
        (2.89, 15.40),
        (2.76, 16.05),
        (2.62, 16.68),
    ]
    vac_void_int = [
        (2.54, 16.68),
        (2.68, 16.05),
        (2.81, 15.40),
        (2.87, 14.70),
        (2.87, 0.68),
    ]
    create_solid_lathe_wall(
        "GEO_Vacuum_Chamber_Recess",
        vac_void_ext,
        vac_void_int,
        s_angle_vac,
        e_angle_vac,
        segments=84,
        mat_main=mats["vacuum_void"],
        mat_cut=mats["vacuum_void"],
        bevel_width=0.02,
        parent=root,
    )

    if is_peeled:
        vac_particles_grp = bpy.data.objects.new("GRP_VACUUM_PARTICLES", None)
        bpy.context.collection.objects.link(vac_particles_grp)
        vac_particles_grp.parent = root
        for idx, (ang_deg, z_ht) in enumerate([
            (-22, 4.0), (-18, 6.5), (-24, 9.0), (-19, 11.5), (-22, 13.8),
            (192, 4.5), (188, 7.5), (194, 10.5), (189, 13.2)
        ]):
            rad = 2.86
            ar = math.radians(ang_deg)
            bpy.ops.mesh.primitive_uv_sphere_add(
                segments=20, ring_count=12, radius=0.085,
                location=(rad * math.cos(ar), rad * math.sin(ar), z_ht)
            )
            sp = bpy.context.object
            sp.name = f"GEO_Vacuum_Particle_{idx:02d}"
            for p in sp.data.polygons:
                p.use_smooth = True
            sp.data.materials.append(mats["vacuum_particle"])
            sp.parent = vac_particles_grp

    # --------------------------------------------------------------------------
    # LAYER 3: COPPER / GOLD MIRROR RADIATION SHIELD (Stepped Rotational Peel!)
    # --------------------------------------------------------------------------
    shield_ext = [
        (2.68, 0.78),
        (2.76, 0.95),
        (2.76, 14.55),
        (2.70, 15.20),
        (2.58, 15.85),
        (2.46, 16.45),
    ]
    shield_int = [
        (2.38, 16.45),
        (2.50, 15.85),
        (2.62, 15.20),
        (2.67, 14.55),
        (2.67, 0.95),
        (0.00, 0.95),
        (0.00, 0.78),
    ]
    # Stepped Peel Angle 3: Copper/Gold Mirror extends from -56 deg to +214 deg
    s_angle_shield = math.radians(-56.0) if is_peeled else 0.0
    e_angle_shield = math.radians(214.0) if is_peeled else 2.0 * math.pi

    create_solid_lathe_wall(
        "GEO_Copper_Gold_Mirror_Shield",
        shield_ext,
        shield_int,
        s_angle_shield,
        e_angle_shield,
        segments=96,
        mat_main=mats["copper_gold_mirror"],
        mat_cut=mats["copper_gold_mirror"],
        bevel_width=0.025,
        parent=root,
    )

    # --------------------------------------------------------------------------
    # LAYER 4: INNER STAINLESS STEEL VESSEL SUS304 (Stepped Window Cut!)
    # --------------------------------------------------------------------------
    inner_ext = [
        (2.56, 0.96),
        (2.65, 1.12),
        (2.65, 14.50),
        (2.59, 15.15),
        (2.48, 15.80),
        (2.36, 16.40),
        (2.12, 16.98),
    ]
    inner_int = [
        (2.00, 16.98),
        (2.24, 16.40),
        (2.36, 15.80),
        (2.47, 15.15),
        (2.53, 14.50),
        (2.53, 1.22),
        (0.00, 1.22),
        (0.00, 0.96),
    ]
    # Stepped Peel Angle 4: Inner Stainless Vessel extends from -74 deg to +230 deg
    s_angle_inner = math.radians(-74.0) if is_peeled else 0.0
    e_angle_inner = math.radians(230.0) if is_peeled else 2.0 * math.pi

    create_solid_lathe_wall(
        "GEO_Inner_Stainless_Vessel",
        inner_ext,
        inner_int,
        s_angle_inner,
        e_angle_inner,
        segments=96,
        mat_main=mats["stainless_inner"],
        mat_cut=mats["steel_cut_bevel"],
        bevel_width=0.03,
        parent=root,
    )

    # --------------------------------------------------------------------------
    # LAYER 5: HOT LIQUID CORE 480 ML (Warm Translucent Amber Tea/Water + Ricochet Waves)
    # --------------------------------------------------------------------------
    liquid_prof = [
        (2.49, 1.25),
        (2.51, 1.45),
        (2.51, 13.80),
        (2.46, 14.40),
    ]
    s_angle_liq = math.radians(-48.0) if is_peeled else 0.0
    e_angle_liq = math.radians(255.0) if is_peeled else 2.0 * math.pi

    create_solid_revolved_core(
        "GEO_Hot_Liquid_Core_480ml",
        liquid_prof,
        s_angle_liq,
        e_angle_liq,
        segments=96,
        mat_main=mats["hot_liquid"],
        mat_top=mats["liquid_meniscus"],
        bevel_width=0.035,
        parent=root,
    )

    # Place 3D Thermal Radiation Bounce Arrows right in the open front-left cutaway window (angle = 222 deg / -138 deg)
    # and front-right cutaway window so they are 100% unobstructed from the camera!
    if is_peeled:
        grp_arrows = bpy.data.objects.new("GRP_THERMAL_BOUNCE_ARROWS", None)
        bpy.context.collection.objects.link(grp_arrows)
        grp_arrows.parent = root
        for idx, z_lvl in enumerate([4.5, 7.6, 10.7]):
            create_heat_bounce_arrow(
                f"GEO_Heat_Bounce_Arrow_{idx:02d}",
                z_level=z_lvl,
                angle_rad=math.radians(212.0),
                r_inner=1.75,
                r_mirror=2.62,
                mat=mats["heat_arrow"],
                parent=grp_arrows,
            )

    # --------------------------------------------------------------------------
    # UPPER NECK, MOUTHPIECE SPOUT (4.0 CM), SSS SILICONE STOPPER, & FLIP LID
    # Cleanly Staggered Axial Exploded Heights in Peeled Mode (Zero Overlap!)
    # --------------------------------------------------------------------------
    z_explode_spout = 1.35 if is_peeled else 0.0
    z_explode_gasket = 1.35 if is_peeled else 0.0
    z_explode_stopper = 3.65 if is_peeled else 0.0
    z_explode_collar = 6.20 if is_peeled else 0.0
    z_explode_cap = 6.20 if is_peeled else 0.0

    # Level 1: Polypropylene Mouthpiece / Drinking Spout (Koukei 4.00 cm) + Warm SSS Gasket
    grp_spout = bpy.data.objects.new("GRP_MOUTHPIECE_SPOUT", None)
    bpy.context.collection.objects.link(grp_spout)
    grp_spout.parent = root
    grp_spout.location = (0.0, 0.0, z_explode_spout)

    spout_ext = [
        (2.82, 16.85),
        (2.88, 17.35),
        (2.42, 17.55),
        (2.32, 18.45),
        (2.18, 18.60),
    ]
    spout_int = [
        (2.00, 18.60),
        (2.00, 16.85),
    ]
    s_angle_spout = math.radians(-55.0) if is_peeled else 0.0
    e_angle_spout = math.radians(225.0) if is_peeled else 2.0 * math.pi
    create_solid_lathe_wall(
        "GEO_Mouthpiece_Spout",
        spout_ext,
        spout_int,
        s_angle_spout,
        e_angle_spout,
        segments=84,
        mat_main=mats["mouthpiece_pp"],
        mat_cut=mats["mouthpiece_pp"],
        bevel_width=0.025,
        parent=grp_spout,
    )

    grp_gasket = bpy.data.objects.new("GRP_SILICONE_GASKET", None)
    bpy.context.collection.objects.link(grp_gasket)
    grp_gasket.parent = root
    grp_gasket.location = (0.0, 0.0, z_explode_gasket)

    create_torus_gasket(
        "GEO_Silicone_Neck_Gasket_SSS",
        z_height=17.05,
        major_radius=2.12,
        minor_radius=0.18,
        mat=mats["silicone_gasket_warm_sss"],
        start_angle=s_angle_spout,
        end_angle=e_angle_spout,
        parent=grp_gasket,
    )

    # Level 2: Silicone Stopper Plug (Pixar-style SSS — Forest Green Elastic Silicone)
    # Floating in its own dedicated vertical band (Z + 3.65 cm) so 100% of it is visible!
    grp_stopper = bpy.data.objects.new("GRP_SILICONE_STOPPER_SSS", None)
    bpy.context.collection.objects.link(grp_stopper)
    grp_stopper.parent = root
    grp_stopper.location = (0.0, 0.0, z_explode_stopper)

    stopper_prof = [
        (1.85, 17.30),
        (2.12, 17.55),
        (2.12, 18.25),
        (2.32, 18.45),
        (2.32, 18.85),
        (1.65, 19.12),
    ]
    create_solid_revolved_core(
        "GEO_Silicone_Stopper_Plug_SSS",
        stopper_prof,
        start_angle=math.radians(-45.0) if is_peeled else 0.0,
        end_angle=math.radians(225.0) if is_peeled else 2.0 * math.pi,
        segments=84,
        mat_main=mats["silicone_stopper_sss"],
        mat_top=mats["silicone_stopper_sss"],
        bevel_width=0.03,
        parent=grp_stopper,
    )

    # Level 3: Cap Lower Collar + One-Hand Push Button + Flip Lid (Z + 6.20 cm)
    grp_collar = bpy.data.objects.new("GRP_CAP_COLLAR", None)
    bpy.context.collection.objects.link(grp_collar)
    grp_collar.parent = root
    grp_collar.location = (0.0, 0.0, z_explode_collar)

    collar_ext = [
        (3.14, 17.02),
        (3.25, 17.25),
        (3.25, 18.55),
    ]
    collar_int = [
        (2.88, 18.55),
        (2.88, 17.02),
    ]
    create_solid_lathe_wall(
        "GEO_Cap_Lower_Collar",
        collar_ext,
        collar_int,
        start_angle=math.radians(-35.0) if is_peeled else 0.0,
        end_angle=math.radians(215.0) if is_peeled else 2.0 * math.pi,
        segments=96,
        mat_main=mats["outer_ice_gray"],
        mat_cut=mats["outer_cut_face"],
        bevel_width=0.03,
        parent=grp_collar,
    )

    create_rounded_box(
        "GEO_Button_Housing", (0.0, -3.28, 18.15), (1.55, 0.34, 1.85), 0.08, mats["dark_trim"], parent=grp_collar
    )
    create_rounded_box(
        "GEO_Release_Push_Button", (0.0, -3.38, 18.15), (1.18, 0.28, 1.38), 0.07, mats["button_accent"], parent=grp_collar
    )
    create_rounded_box(
        "GEO_Safety_Lock_Slider", (1.42, -3.22, 18.15), (0.85, 0.28, 0.62), 0.06, mats["button_accent"], parent=grp_collar
    )
    create_rounded_box(
        "GEO_Safety_Lock_Red_Dot", (1.72, -3.32, 18.15), (0.22, 0.12, 0.28), 0.04, mats["lock_red_indicator"], parent=grp_collar
    )
    create_rounded_box(
        "GEO_Rear_Hinge_Block", (0.0, 3.24, 18.35), (1.50, 0.38, 1.25), 0.08, mats["dark_trim"], parent=grp_collar
    )

    grp_cap = bpy.data.objects.new("GRP_CAP_ASSEMBLY", None)
    grp_cap.empty_display_type = "SPHERE"
    grp_cap.empty_display_size = 1.2
    bpy.context.collection.objects.link(grp_cap)
    grp_cap.parent = root
    grp_cap.location = (0.0, 3.15, 18.55 + z_explode_cap)

    lid_ext = [
        (3.25, 18.58),
        (3.25, 19.75),
        (3.20, 20.35),
        (3.02, 20.95),
        (2.68, 21.35),
        (2.25, 21.50),
    ]
    lid_int = [
        (0.00, 21.50),
        (0.00, 20.95),
        (2.45, 20.95),
        (2.85, 20.25),
        (2.90, 18.58),
    ]
    lid_obj = create_solid_lathe_wall(
        "GEO_Flip_Lid_Dome",
        lid_ext,
        lid_int,
        start_angle=math.radians(-35.0) if is_peeled else 0.0,
        end_angle=math.radians(215.0) if is_peeled else 2.0 * math.pi,
        segments=96,
        mat_main=mats["outer_ice_gray"],
        mat_cut=mats["outer_cut_face"],
        bevel_width=0.035,
    )
    for v in lid_obj.data.vertices:
        v.co.y -= 3.15
        v.co.z -= 18.55
    lid_obj.data.update()
    lid_obj.parent = grp_cap
    lid_obj.location = (0.0, 0.0, 0.0)

    # Negative X rotation tilts the front (-Y) of the lid UP and BACK around the rear hinge (+Y)!
    grp_cap.rotation_euler = Euler((math.radians(-32.0 if is_peeled else 0.0), 0.0, 0.0), "XYZ")

    # --------------------------------------------------------------------------
    # 3D ANCHOR LOCATORS FOR HUD PIN SYNCHRONIZATION
    # --------------------------------------------------------------------------
    anchors = {
        "ANCHOR_HERO_TITLE": (0.0, 0.0, 23.5 + (z_explode_cap if is_peeled else 0.0)),
        "ANCHOR_CAP_LID": (0.0, -2.5, 19.8 + (z_explode_cap if is_peeled else 0.0)),
        "ANCHOR_SILICONE_STOPPER": (0.0, -1.8, 18.2 + z_explode_stopper),
        "ANCHOR_MOUTHPIECE_SPOUT": (-1.8, -1.2, 17.8 + z_explode_spout),
        "ANCHOR_OUTER_SHELL_ICEGRAY": (-4.6 if is_peeled else -3.25, -0.5, 11.8),
        "ANCHOR_VACUUM_GAP_2MM": (2.75, -1.2, 11.2),
        "ANCHOR_COPPER_GOLD_MIRROR": (2.25, -1.5, 8.8),
        "ANCHOR_INNER_STEEL_SUS304": (1.65, -1.8, 6.4),
        "ANCHOR_HOT_LIQUID_CORE": (-0.4, -1.5, 5.0),
    }
    for aname, apos in anchors.items():
        emp = bpy.data.objects.new(aname, None)
        emp.empty_display_type = "SPHERE"
        emp.empty_display_size = 0.25
        emp.location = apos
        emp.parent = root
        bpy.context.collection.objects.link(emp)

    return mats, anchors


# ==============================================================================
# 4. CURVED INFINITY CYCLORAMA & THREE-POINT + STRONG RIM LIGHTING
# ==============================================================================
def create_curved_infinity_cyclorama(mat):
    """
    Creates a true curved L-shaped studio infinity backdrop so there is NEVER
    a visible horizon line behind the thermos!
    """
    verts = []
    faces = []
    width = 160.0
    # Profile in (Y, Z): from front floor Y=-70, curving smoothly at Y=+25..+60 up to Z=+140
    yz_pts = [
        (-75.0, -0.02),
        (18.0, -0.02),
    ]
    bend_r = 35.0
    bend_cy = 18.0
    bend_cz = bend_r - 0.02
    for k in range(1, 16):
        ang = -math.pi * 0.5 + (k / 15.0) * (math.pi * 0.5)
        y = bend_cy + bend_r * math.cos(ang)
        z = bend_cz + bend_r * math.sin(ang)
        yz_pts.append((y, z))
    yz_pts.append((bend_cy + bend_r, 150.0))

    for y, z in yz_pts:
        verts.append((-width, y, z))
        verts.append((width, y, z))

    for i in range(len(yz_pts) - 1):
        v0 = i * 2
        v1 = i * 2 + 1
        v2 = (i + 1) * 2 + 1
        v3 = (i + 1) * 2
        faces.append((v0, v1, v2, v3))

    mesh = bpy.data.meshes.new("GEO_Infinity_Cyclorama_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new("GEO_Infinity_Cyclorama", mesh)
    bpy.context.collection.objects.link(obj)
    for p in obj.data.polygons:
        p.use_smooth = True
    if mat:
        obj.data.materials.append(mat)
    return obj


def setup_semi_realistic_stage_and_lights(mats, mode="hero"):
    scene = bpy.context.scene

    world = scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (*hex_to_linear("#F4F1EA"), 1.0)
    bg.inputs["Strength"].default_value = 0.95

    create_curved_infinity_cyclorama(mats["studio_floor"])

    # Three-Point Lighting + Dual Strong Rim Lights + Backdrop Wash + Top Specular Bar
    light_specs = [
        # 1. Key Light (Warm-white dramatic main light from front-left)
        ("LIGHT_Key_Main", (-28.0, -34.0, 34.0), (0.0, 0.0, 12.0), 2600.0, 18.0, "#FFFBF2"),
        # 2. Fill Light (Cool-soft fill from front-right for vibrant shadow detail)
        ("LIGHT_Fill_Soft", (32.0, -28.0, 22.0), (0.0, 0.0, 11.0), 1300.0, 24.0, "#EBF4FF"),
        # 3. Strong Rim Light Left-Back (Separates Matte Ice Gray silhouette & ignites SSS)
        ("LIGHT_Rim_Strong_Left", (-22.0, 24.0, 28.0), (0.0, 0.0, 13.0), 3400.0, 11.0, "#FFF2D6"),
        # 4. Strong Rim Light Right-Back (Ignites Copper/Gold Mirror & beveled cutaway edges)
        ("LIGHT_Rim_Strong_Right", (24.0, 20.0, 25.0), (0.0, 0.0, 12.0), 3200.0, 11.0, "#FFEAB8"),
        # 5. Top Specular Highlight Bar (Brings out rounded bevels & SSS Silicone Stopper)
        ("LIGHT_Top_Specular", (0.0, -6.0, 44.0), (0.0, 0.0, 16.0), 1500.0, 15.0, "#FFFFFF"),
        # 6. Cyclorama Backdrop Wash (Keeps the studio paper background bright, warm & clean)
        ("LIGHT_Backdrop_Wash", (0.0, -15.0, 38.0), (0.0, 48.0, 28.0), 4200.0, 45.0, "#FFFDF9"),
    ]
    for lname, lpos, ltarget, lenergy, lsize, lhex in light_specs:
        ldata = bpy.data.lights.new(lname, type="AREA")
        ldata.energy = lenergy
        ldata.shape = "DISK"
        ldata.size = lsize
        ldata.color = hex_to_linear(lhex)
        lobj = bpy.data.objects.new(lname, ldata)
        bpy.context.collection.objects.link(lobj)
        lobj.location = lpos
        direction = Vector(ltarget) - Vector(lpos)
        lobj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    cam_data = bpy.data.cameras.new("CAM_SemiReal_Master")
    cam = bpy.data.objects.new("CAM_SemiReal_Master", cam_data)
    bpy.context.collection.objects.link(cam)
    cam_data.lens = 68.0
    cam_data.sensor_width = 36.0
    cam_data.dof.use_dof = True

    if mode == "hero":
        cam.location = (22.0, -56.0, 15.0)
        target = Vector((0.0, 0.0, 11.0))
        cam_data.dof.focus_distance = (target - cam.location).length
        cam_data.dof.aperture_fstop = 4.5
    else:
        # Framed to comfortably include both the base and the axial-exploded lid stack (Z = 0..27 cm)
        cam.location = (22.0, -68.0, 17.5)
        target = Vector((-0.3, 0.0, 13.5))
        cam_data.dof.focus_distance = (target - cam.location).length
        cam_data.dof.aperture_fstop = 5.0

    direction = target - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    scene.camera = cam
    bpy.context.view_layer.update()
    return cam


def configure_raytraced_renderer():
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = 64
    scene.cycles.use_adaptive_sampling = True
    scene.cycles.adaptive_threshold = 0.02
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = "OPENIMAGEDENOISE"
    scene.cycles.max_bounces = 8
    scene.cycles.diffuse_bounces = 3
    scene.cycles.glossy_bounces = 4
    scene.cycles.transmission_bounces = 6
    scene.cycles.volume_bounces = 2

    scene.render.use_freestyle = False
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1920
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = False

    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.view_settings.exposure = 0.35
    scene.view_settings.gamma = 1.0


def project_anchors(cam, scene, anchors):
    from bpy_extras.object_utils import world_to_camera_view
    out = {}
    for k, pos in anchors.items():
        co = world_to_camera_view(scene, cam, Vector(pos))
        out[k] = {
            "x_px": round(co.x * 1080),
            "y_px": round((1.0 - co.y) * 1920),
            "x_pct": round(co.x * 100, 2),
            "y_pct": round((1.0 - co.y) * 100, 2),
            "depth_cm": round(co.z, 2),
        }
    return out


def sync_to_mirror():
    for fname in [
        "termos-03-lookdev-hero-v0.3.png",
        "termos-03-lookdev-peeled-v0.3.png",
        "termos-03-master-semi-realis-v0.3.blend",
        "termos-03-anchors-semi-realis-v0.3.json",
        "guideline-render-3d-semi-realis-v0.1.md",
    ]:
        src = os.path.join(OUTPUTS_DIR, fname)
        dst = os.path.join(MIRROR_OUTPUTS_DIR, fname)
        if os.path.exists(src):
            shutil.copy2(src, dst)


def main():
    anchor_export = {}

    print(">>> Rendering Polished LookDev Gate 1: HERO EXTERIOR...")
    clear_scene()
    mats_hero, anchors_hero = build_semi_realistic_termos(mode="hero")
    cam_hero = setup_semi_realistic_stage_and_lights(mats_hero, mode="hero")
    configure_raytraced_renderer()
    anchor_export["lookdev_hero"] = project_anchors(cam_hero, bpy.context.scene, anchors_hero)
    bpy.context.scene.render.filepath = HERO_PNG
    bpy.ops.render.render(write_still=True)

    print(">>> Rendering Polished LookDev Gate 2: MULTI-LAYER PEELED + AXIAL EXPLODED...")
    clear_scene()
    mats_peel, anchors_peel = build_semi_realistic_termos(mode="peeled")
    cam_peel = setup_semi_realistic_stage_and_lights(mats_peel, mode="peeled")
    configure_raytraced_renderer()
    anchor_export["lookdev_peeled"] = project_anchors(cam_peel, bpy.context.scene, anchors_peel)
    bpy.context.scene.render.filepath = PEELED_PNG
    bpy.ops.render.render(write_still=True)

    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
    with open(ANCHORS_JSON, "w", encoding="utf-8") as f:
        json.dump(anchor_export, f, indent=2)

    sync_to_mirror()
    print(">>> ALL LOOKDEV GATE RENDERS & MIRROR SYNC COMPLETE!")


if __name__ == "__main__":
    main()
