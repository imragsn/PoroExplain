import bpy
import math
import os
import json
from mathutils import Vector

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
RENDER_DIR = os.path.join(ROOT, "work", "termos-3d", "renders-v02")
OUTPUTS_DIR = os.path.join(ROOT, "outputs")
BLEND_PATH = os.path.join(OUTPUTS_DIR, "termos-03-master-model-v0.2.blend")
ANCHORS_JSON = os.path.join(OUTPUTS_DIR, "termos-05-anchors-v0.2.json")

os.makedirs(RENDER_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        pass


def create_material(name, color, roughness=0.45, metallic=0.0, emission_color=(0, 0, 0), emission_strength=0.0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
        if "Emission Color" in bsdf.inputs and emission_strength > 0:
            bsdf.inputs["Emission Color"].default_value = (*emission_color, 1.0)
            bsdf.inputs["Emission Strength"].default_value = emission_strength
    return mat


def lathe_mesh(name, profile, start_angle=0.0, end_angle=2*math.pi, segments=96, mat=None, cap_cut=False):
    """
    Creates a lathe / revolved mesh.
    profile is a list of (radius, z) coordinates.
    Supports partial angle for cutaway (e.g. start_angle=0, end_angle=1.5*pi for 90-degree wedge cut,
    or start_angle=0, end_angle=pi for 180-degree half-cut).
    """
    total_angle = end_angle - start_angle
    is_closed = math.isclose(total_angle, 2 * math.pi, abs_tol=1e-4)
    num_steps = segments if is_closed else segments + 1
    
    verts = []
    for r, z in profile:
        for i in range(num_steps):
            frac = i / segments
            a = start_angle + frac * total_angle
            x = r * math.cos(a)
            y = r * math.sin(a)
            verts.append((x, y, z))
            
    faces = []
    rings = len(profile)
    for j in range(rings - 1):
        for i in range(segments if is_closed else segments):
            ni = (i + 1) % segments if is_closed else i + 1
            a = j * num_steps + i
            b = j * num_steps + ni
            c = (j + 1) * num_steps + ni
            d = (j + 1) * num_steps + i
            faces.append((a, b, c, d))
            
    # Bottom cap
    if is_closed:
        faces.append(tuple(reversed(tuple(range(segments)))))
        # Top cap
        top = tuple((rings - 1) * segments + i for i in range(segments))
        faces.append(top)
        
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    
    for poly in mesh.polygons:
        poly.use_smooth = True
        
    if mat:
        obj.data.materials.append(mat)
    return obj


def create_solid_cylinder(name, radius, depth, location, mat, vertices=96):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    for poly in obj.data.polygons:
        poly.use_smooth = True
    if mat:
        obj.data.materials.append(mat)
    return obj


def create_rounded_box(name, location, dimensions, bevel, mat):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel > 0:
        mod = obj.modifiers.new("bevel", "BEVEL")
        mod.width = bevel
        mod.segments = 4
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
    for poly in obj.data.polygons:
        poly.use_smooth = True
    if mat:
        obj.data.materials.append(mat)
    return obj


def build_complete_termos(wedge_cut=False, half_cut=False):
    """
    Builds the complete hierarchical termos model.
    wedge_cut: removes 90 degrees (front-right) to reveal interior.
    half_cut: removes 180 degrees (front half) for pure technical cross-section.
    """
    # Stylized Palette
    # Outer Shell: Ice Gray (#6e9194 -> sRGB approx 0.43, 0.57, 0.58)
    mat_outer = create_material("mat_ice_gray", (0.43, 0.57, 0.58), roughness=0.35, metallic=0.08)
    mat_dark_trim = create_material("mat_dark_trim", (0.22, 0.31, 0.33), roughness=0.50, metallic=0.02)
    mat_accent_button = create_material("mat_button", (0.33, 0.46, 0.47), roughness=0.35, metallic=0.05)
    
    # Interior Technical Layers
    # Outer Steel Wall (#8e99a2)
    mat_outer_wall = create_material("mat_outer_steel", (0.58, 0.63, 0.67), roughness=0.30, metallic=0.45)
    # Vacuum Gap: Ghosted schematic void / contrast boundary (#242d33)
    mat_vacuum = create_material("mat_vacuum_gap", (0.16, 0.20, 0.23), roughness=0.80, metallic=0.0)
    # Reflective Layer: Yellow/Gold heat bounce shield (#f5b700 -> approx 0.96, 0.72, 0.05)
    mat_reflective = create_material("mat_reflective_shield", (0.96, 0.72, 0.05), roughness=0.20, metallic=0.85,
                                     emission_color=(0.96, 0.72, 0.05), emission_strength=0.15)
    # Inner Steel Wall (#b0bec5)
    mat_inner_wall = create_material("mat_inner_steel", (0.75, 0.80, 0.84), roughness=0.25, metallic=0.60)
    # Liquid: Warm amber coffee/tea (#e67e22 -> approx 0.90, 0.49, 0.13)
    mat_liquid = create_material("mat_hot_liquid", (0.90, 0.49, 0.13), roughness=0.20, metallic=0.0,
                                 emission_color=(0.90, 0.45, 0.10), emission_strength=0.25)
    # Stopper / Seal: Silicone rubber dark gray (#2d3748)
    mat_stopper = create_material("mat_silicone_stopper", (0.18, 0.22, 0.25), roughness=0.70, metallic=0.0)
    mat_mouthpiece = create_material("mat_mouthpiece", (0.92, 0.92, 0.90), roughness=0.40, metallic=0.0)

    # Angle settings for cutaways
    if wedge_cut:
        # Cut away from 0 to 90 degrees (X > 0, Y > 0) or front quadrant
        start_a = math.pi * 0.5
        end_a = math.pi * 2.0
    elif half_cut:
        # Cut away front half (Y < 0), leave back half (Y >= 0)
        start_a = 0.0
        end_a = math.pi
    else:
        start_a = 0.0
        end_a = math.pi * 2.0

    # 1. OUTER SHELL (Dinding luar pembungkus)
    # Profile: (radius, z) in cm - exactly 6.5 cm diameter, body height 17.0 cm
    outer_profile = [
        (3.08, 0.00),
        (3.22, 0.15),
        (3.25, 0.35),
        (3.25, 14.85),
        (3.22, 15.55),
        (3.12, 16.15),
        (2.96, 16.65),
        (2.90, 17.00)
    ]
    lathe_mesh("outer_shell", outer_profile, start_a, end_a, segments=96, mat=mat_outer)

    # Base ring & neck trim
    lathe_mesh("base_ring", [(3.26, 0.12), (3.26, 0.55)], start_a, end_a, segments=96, mat=mat_dark_trim)
    lathe_mesh("neck_trim", [(3.16, 16.80), (3.16, 17.05)], start_a, end_a, segments=96, mat=mat_dark_trim)

    # 2. INTERNAL LAYERS (Layered Double-Wall Vacuum Chamber)
    # Note: Vacuum gap is schematically enlarged (~0.20 cm) for readability on vertical mobile screens
    # Layer A: Outer Steel Wall
    profile_outer_steel = [
        (3.05, 0.30),
        (3.14, 0.50),
        (3.14, 14.80),
        (3.06, 15.45),
        (2.92, 16.10),
        (2.80, 16.70),
    ]
    lathe_mesh("layer_outer_steel", profile_outer_steel, start_a, end_a, segments=96, mat=mat_outer_wall)

    # Layer B: Vacuum Gap (Celah Ruang Hampa)
    profile_vacuum = [
        (2.82, 0.50),
        (2.92, 0.65),
        (2.92, 14.65),
        (2.84, 15.25),
        (2.72, 15.90),
        (2.62, 16.50),
    ]
    lathe_mesh("layer_vacuum_gap", profile_vacuum, start_a, end_a, segments=96, mat=mat_vacuum)

    # Layer C: Reflective Heat-Bounce Shield (Lapisan Pemantul Radiasi)
    profile_reflective = [
        (2.74, 0.60),
        (2.82, 0.75),
        (2.82, 14.55),
        (2.75, 15.15),
        (2.64, 15.80),
        (2.55, 16.40),
    ]
    lathe_mesh("layer_reflective_shield", profile_reflective, start_a, end_a, segments=96, mat=mat_reflective)

    # Layer D: Inner Stainless Steel Vessel (Dinding Baja Dalam)
    profile_inner_steel = [
        (2.56, 0.70),
        (2.66, 0.85),
        (2.66, 14.50),
        (2.60, 15.10),
        (2.50, 15.70),
        (2.42, 16.35),
        (2.05, 16.90),
    ]
    lathe_mesh("layer_inner_steel", profile_inner_steel, start_a, end_a, segments=96, mat=mat_inner_wall)

    # Layer E: Hot/Cold Liquid Core (Isi Cairan 480ml - naik sampai mendekati leher)
    profile_liquid = [
        (0.00, 0.90),
        (2.55, 0.90),
        (2.55, 14.50),
        (2.40, 15.50),
        (2.00, 16.45),
        (0.00, 16.45),
    ]
    lathe_mesh("core_liquid", profile_liquid, start_a, end_a, segments=96, mat=mat_liquid)

    # 3. CAP & LID MECHANISM (Tutup, Engsel, Stopper Silikon, Tombol)
    # Total height reaches 21.50 cm exactly
    cap_profile = [
        (3.16, 17.00),
        (3.22, 17.15),
        (3.25, 17.50),
        (3.25, 19.65),
        (3.22, 20.30),
        (3.02, 20.95),
        (2.68, 21.35),
        (2.30, 21.50)
    ]
    lathe_mesh("cap_body", cap_profile, start_a if half_cut else 0.0, end_a if half_cut else math.pi * 2.0, segments=96, mat=mat_outer)

    # Silicone Stopper (Sumbat Mulut Botol - Pencegah Konveksi)
    stopper_profile = [
        (0.00, 16.30),
        (2.02, 16.30),
        (2.02, 17.80),
        (1.95, 18.30),
        (0.00, 18.30)
    ]
    lathe_mesh("silicone_stopper", stopper_profile, start_a, end_a, segments=96, mat=mat_stopper)

    # Mouthpiece / Spout (Corong Minum - Koukei 4.0 cm)
    spout_profile = [
        (2.00, 16.80),
        (2.25, 16.80),
        (2.25, 18.60),
        (2.00, 18.60)
    ]
    lathe_mesh("mouthpiece_spout", spout_profile, start_a, end_a, segments=96, mat=mat_mouthpiece)

    # Exterior Controls (Button, Lock, Hinge)
    # Button is at front (negative Y: (0, -3.34, 18.78))
    create_rounded_box("release_button", (0.00, -3.34, 18.78), (1.45, 0.30, 2.10), 0.25, mat_accent_button)
    create_rounded_box("button_recess", (0.00, -3.48, 18.78), (1.00, 0.05, 1.58), 0.15, mat_dark_trim)
    create_rounded_box("safety_lock_slider", (1.62, -3.32, 18.55), (1.15, 0.30, 0.74), 0.18, mat_accent_button)
    create_rounded_box("hinge_block", (0.00, 3.32, 18.30), (1.55, 0.36, 1.10), 0.22, mat_dark_trim)

    # 4. ANCHOR LOCATORS (Empty Points for Remotion HUD labels)
    anchors = {
        "ANCHOR_HERO_TITLE": (0.0, -4.5, 22.5),
        "ANCHOR_CAP_LID": (0.0, -3.6, 20.2),
        "ANCHOR_RELEASE_BUTTON": (0.0, -3.7, 18.8),
        "ANCHOR_SILICONE_STOPPER": (0.0, 0.0, 17.5),
        "ANCHOR_OUTER_WALL": (3.2, 0.0, 11.0),
        "ANCHOR_VACUUM_GAP": (2.85, 0.0, 10.0),
        "ANCHOR_REFLECTIVE_SHIELD": (2.75, 0.0, 9.0),
        "ANCHOR_INNER_WALL": (2.55, 0.0, 8.0),
        "ANCHOR_HOT_LIQUID": (0.0, 0.0, 7.0),
        "ANCHOR_BASE": (0.0, -3.5, 0.4),
    }
    
    for aname, apos in anchors.items():
        empty = bpy.data.objects.new(aname, None)
        empty.empty_display_type = "PLAIN_AXES"
        empty.empty_display_size = 0.4
        empty.location = apos
        bpy.context.collection.objects.link(empty)

    return anchors


def setup_lighting_and_stage():
    world = bpy.context.scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    # Soft warm neutral studio background (#EFE9E0 -> 0.937, 0.914, 0.878)
    bg.inputs["Color"].default_value = (0.937, 0.914, 0.878, 1.0)
    bg.inputs["Strength"].default_value = 0.85

    # Ground shadow catcher plane
    floor_mat = create_material("mat_floor", (0.90, 0.88, 0.85), roughness=0.9, metallic=0.0)
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -0.05))
    floor = bpy.context.object
    floor.name = "studio_floor"
    floor.data.materials.append(floor_mat)

    # 3-Point Technical Clean Lighting (Soft highlights, zero harsh specular noise)
    lights = [
        ("key_light", (-16, -24, 32), 1200, 12.0),
        ("fill_light", (20, -12, 22), 750, 10.0),
        ("rim_back_light", (0, 22, 28), 900, 8.0),
        ("under_bounce", (0, -10, 2), 350, 6.0),
    ]
    for lname, lpos, lenergy, lsize in lights:
        ldata = bpy.data.lights.new(lname, type="AREA")
        ldata.energy = lenergy
        ldata.shape = "DISK"
        ldata.size = lsize
        lobj = bpy.data.objects.new(lname, ldata)
        bpy.context.collection.objects.link(lobj)
        lobj.location = lpos
        direction = Vector((0, 0, 10)) - lobj.location
        lobj.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    cam_data = bpy.data.cameras.new("render_cam")
    cam = bpy.data.objects.new("render_cam", cam_data)
    bpy.context.collection.objects.link(cam)
    cam.data.lens = 60
    cam.data.sensor_width = 36
    bpy.context.scene.camera = cam
    return cam


def point_camera_at(camera, target=(0, 0, 10.75)):
    direction = Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    bpy.context.view_layer.update()


def project_3d_to_screen(camera, scene, point_3d):
    """Calculates screen coordinate (X%, Y%) from 3D world position."""
    from bpy_extras.object_utils import world_to_camera_view
    co_2d = world_to_camera_view(scene, camera, Vector(point_3d))
    return {
        "x_percent": round(co_2d.x * 100, 2),
        "y_percent": round((1.0 - co_2d.y) * 100, 2),  # Inverted for standard UI top-left origin
        "depth": round(co_2d.z, 2),
        "is_visible": bool(0.0 <= co_2d.x <= 1.0 and 0.0 <= co_2d.y <= 1.0 and co_2d.z > 0)
    }


def execute_all_renders():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    # Format vertical 9:16 (1080 x 1920) matching final video specification
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1920
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = False
    scene.view_settings.look = "AgX - Medium High Contrast"

    # Define the 4 intentional angles with calibrated framing (no clipping!)
    shots = [
        {
            "id": "shot_01_hero_exterior",
            "name": "Shot 01: Hero 3-Quarter (Exterior Utuh)",
            "cam_pos": (36.0, -50.0, 16.0),
            "cam_target": (0.0, 0.0, 10.75),
            "model_type": "full",
            "desc": "Bentuk luar utuh: siluet botol, proporsi ramping, tombol buka dan pengunci samping."
        },
        {
            "id": "shot_02_frontal_cutaway",
            "name": "Shot 02: Frontal Cross-Section (Penampang Frontal)",
            "cam_pos": (0.0, -60.0, 10.75),
            "cam_target": (0.0, 0.0, 10.75),
            "model_type": "half",
            "desc": "Penampang teknis frontal: urutan 5 lapisan (Dinding Luar, Vakum, Reflektif, Dinding Dalam, Cairan)."
        },
        {
            "id": "shot_03_close_stopper",
            "name": "Shot 03: Close-Up Neck & Silicone Stopper (Penyekat Panas)",
            "cam_pos": (18.0, -32.0, 21.0),
            "cam_target": (0.0, 0.0, 17.5),
            "model_type": "half",
            "desc": "Detail mulut botol & stopper silikon penahan uap panas konveksi."
        },
        {
            "id": "shot_04_iso_wedge_cut",
            "name": "Shot 04: Isometric 3D Wedge Cut (Potongan Isometrik 90 Derajat)",
            "cam_pos": (40.0, -42.0, 22.0),
            "cam_target": (0.0, 0.0, 10.75),
            "model_type": "wedge",
            "desc": "Potongan isometrik 3D: memperlihatkan volume luar silinder dan lapisan dalam sekaligus."
        }
    ]

    all_anchor_data = {}

    for shot in shots:
        clear_scene()
        if shot["model_type"] == "full":
            anchors = build_complete_termos(wedge_cut=False, half_cut=False)
        elif shot["model_type"] == "half":
            anchors = build_complete_termos(wedge_cut=False, half_cut=True)
        elif shot["model_type"] == "wedge":
            anchors = build_complete_termos(wedge_cut=True, half_cut=False)
            
        cam = setup_lighting_and_stage()
        cam.location = shot["cam_pos"]
        point_camera_at(cam, shot["cam_target"])

        # Calculate screen coordinates for all anchors for this camera shot
        shot_anchors = {}
        for aname, apos in anchors.items():
            shot_anchors[aname] = project_3d_to_screen(cam, scene, apos)

        all_anchor_data[shot["id"]] = {
            "name": shot["name"],
            "description": shot["desc"],
            "camera_position": list(shot["cam_pos"]),
            "camera_target": list(shot["cam_target"]),
            "anchors_screen_space": shot_anchors
        }

        out_img = os.path.join(RENDER_DIR, f"{shot['id']}.png")
        scene.render.filepath = out_img
        print(f"Rendering {shot['id']} to {out_img}...")
        bpy.ops.render.render(write_still=True)

    # Save final blend file (with half-cut model and complete setup)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
    print(f"Master Blender file saved to: {BLEND_PATH}")

    # Export anchors JSON
    with open(ANCHORS_JSON, "w", encoding="utf-8") as f:
        json.dump(all_anchor_data, f, indent=2)
    print(f"Anchors exported to: {ANCHORS_JSON}")


if __name__ == "__main__":
    execute_all_renders()
