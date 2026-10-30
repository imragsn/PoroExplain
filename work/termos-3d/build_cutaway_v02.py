import bpy
import math
import os
import json
from mathutils import Vector


ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
RENDER_DIR = os.path.join(ROOT, "work", "termos-3d", "renders-v02")
BLEND_PATH = os.path.join(ROOT, "outputs", "termos-03-master-cutaway-v0.2.blend")
MANIFEST_PATH = os.path.join(ROOT, "outputs", "termos-03-manifest-bukti-v0.2.json")
os.makedirs(RENDER_DIR, exist_ok=True)


def mat(name, color, roughness=0.55, metallic=0.0):
    existing = bpy.data.materials.get(name)
    if existing:
        return existing
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1.0)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return m


MAT_OUTER = mat("cut_outer_gray", (0.43, 0.52, 0.53), 0.58, 0.03)
MAT_CUT = mat("cut_surface_yellow", (0.95, 0.62, 0.05), 0.55, 0.02)
MAT_STEEL = mat("inner_steel", (0.42, 0.45, 0.46), 0.30, 0.65)
MAT_REFLECT = mat("reflective_layer_gold", (0.96, 0.72, 0.12), 0.32, 0.35)
MAT_VACUUM = mat("vacuum_marker_blue", (0.25, 0.68, 0.85), 0.42, 0.05)
MAT_WATER = mat("hot_water_orange", (0.62, 0.035, 0.012), 0.34, 0.00)
MAT_GASKET = mat("gasket_dark", (0.10, 0.12, 0.12), 0.65, 0.00)


def apply_evidence(obj, evidence_status, geometry_status, source_ids):
    obj["evidence_status"] = evidence_status
    obj["geometry_status"] = geometry_status
    obj["source_ids"] = ",".join(source_ids)


def partial_shell(name, r_outer, r_inner, z0, z1, start_deg=0.0, end_deg=270.0,
                  segments=96, side_mat=None, cut_mat=None, collection=None):
    angles = [math.radians(start_deg + (end_deg - start_deg) * i / segments) for i in range(segments + 1)]
    verts = []
    # Per angle: outer bottom/top, inner bottom/top.
    for a in angles:
        ca, sa = math.cos(a), math.sin(a)
        verts.extend([
            (r_outer * ca, r_outer * sa, z0),
            (r_outer * ca, r_outer * sa, z1),
            (r_inner * ca, r_inner * sa, z0),
            (r_inner * ca, r_inner * sa, z1),
        ])
    faces = []
    mats = []
    for i in range(segments):
        a, b = i * 4, (i + 1) * 4
        faces.extend([
            (a, b, b + 1, a + 1),          # outer
            (a + 2, a + 3, b + 3, b + 2),  # inner
            (a, a + 2, b + 2, b),          # bottom
            (a + 1, b + 1, b + 3, a + 3),  # top
        ])
        mats.extend([0, 0, 0, 0])
    faces.extend([(0, 1, 3, 2), (segments * 4, segments * 4 + 2, segments * 4 + 3, segments * 4 + 1)])
    mats.extend([1, 1])
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    (collection or bpy.context.collection).objects.link(obj)
    obj.data.materials.append(side_mat or MAT_OUTER)
    obj.data.materials.append(cut_mat or MAT_CUT)
    for p, idx in zip(obj.data.polygons, mats):
        p.material_index = idx
        p.use_smooth = idx == 0
    return obj


def partial_profile_shell(name, outer_profile, inner_profile, start_deg=0.0, end_deg=270.0,
                          segments=96, side_mat=None, cut_mat=None, collection=None):
    assert len(outer_profile) == len(inner_profile)
    rings = len(outer_profile)
    angles = [math.radians(start_deg + (end_deg - start_deg) * i / segments) for i in range(segments + 1)]
    verts = []
    # Per angle, all outer profile points followed by all inner profile points.
    for a in angles:
        ca, sa = math.cos(a), math.sin(a)
        for r, z in outer_profile:
            verts.append((r * ca, r * sa, z))
        for r, z in inner_profile:
            verts.append((r * ca, r * sa, z))
    stride = rings * 2
    faces, mats = [], []
    for i in range(segments):
        a0, a1 = i * stride, (i + 1) * stride
        for j in range(rings - 1):
            faces.append((a0 + j, a1 + j, a1 + j + 1, a0 + j + 1))
            mats.append(0)
            faces.append((a0 + rings + j, a0 + rings + j + 1, a1 + rings + j + 1, a1 + rings + j))
            mats.append(0)
        faces.append((a0, a0 + rings, a1 + rings, a1))
        mats.append(0)
        faces.append((a0 + rings - 1, a1 + rings - 1, a1 + 2 * rings - 1, a0 + 2 * rings - 1))
        mats.append(0)
    for angle_index in (0, segments):
        base = angle_index * stride
        for j in range(rings - 1):
            faces.append((base + j, base + j + 1, base + rings + j + 1, base + rings + j))
            mats.append(1)
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    (collection or bpy.context.collection).objects.link(obj)
    obj.data.materials.append(side_mat or MAT_OUTER)
    obj.data.materials.append(cut_mat or MAT_CUT)
    for p, idx in zip(obj.data.polygons, mats):
        p.material_index = idx
        p.use_smooth = idx == 0
    return obj


def partial_sector(name, radius, z0, z1, start_deg=0.0, end_deg=270.0,
                   segments=96, material=None, cut_material=None, collection=None):
    angles = [math.radians(start_deg + (end_deg - start_deg) * i / segments) for i in range(segments + 1)]
    verts = [(0, 0, z0), (0, 0, z1)]
    for a in angles:
        verts.append((radius * math.cos(a), radius * math.sin(a), z0))
        verts.append((radius * math.cos(a), radius * math.sin(a), z1))
    faces, mats = [], []
    for i in range(segments):
        a = 2 + i * 2
        b = a + 2
        faces.extend([(a, b, b + 1, a + 1), (0, b, a), (1, a + 1, b + 1)])
        mats.extend([0, 0, 0])
    first, last = 2, 2 + segments * 2
    faces.extend([(0, first, first + 1, 1), (0, 1, last + 1, last)])
    mats.extend([1, 1])
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    (collection or bpy.context.collection).objects.link(obj)
    obj.data.materials.append(material or MAT_WATER)
    obj.data.materials.append(cut_material or MAT_CUT)
    for p, idx in zip(obj.data.polygons, mats):
        p.material_index = idx
        p.use_smooth = idx == 0
    return obj


def ensure_collection(name):
    col = bpy.data.collections.get(name)
    if not col:
        col = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(col)
    return col


EXTERIOR = ensure_collection("MODEL_EXTERIOR")
CUTAWAY = ensure_collection("MODEL_CUTAWAY_SCHEMATIC")

# Organize existing model objects without duplicating collection links.
existing_model_names = {
    "outer_shell", "base_ring", "neck_band", "cap_outer", "release_button",
    "release_button_inset", "safety_lock", "safety_lock_ridge", "hinge_block",
    "brand_mark_placeholder",
}
for obj in list(bpy.context.scene.objects):
    if obj.name in existing_model_names:
        for col in list(obj.users_collection):
            col.objects.unlink(obj)
        EXTERIOR.objects.link(obj)

body_outer = [
    (3.08, 0.00), (3.20, 0.12), (3.25, 0.35), (3.25, 14.65),
    (3.22, 15.25), (3.12, 15.85), (2.96, 16.32), (2.90, 16.70),
]
body_inner = [
    (2.82, 0.26), (2.92, 0.30), (2.98, 0.48), (2.98, 14.58),
    (2.95, 15.15), (2.84, 15.70), (2.67, 16.12), (2.61, 16.42),
]
outer_wall = partial_profile_shell("outer_wall_cutaway", body_outer, body_inner, collection=CUTAWAY)
apply_evidence(outer_wall, "verified_external_inferred_internal", "internal_thickness_exaggerated", ["F-PRODUCT-DIMS", "F-PRODUCT-FRONT"])

cap_outer_profile = [
    (3.18, 16.70), (3.23, 16.88), (3.25, 17.28), (3.25, 19.55),
    (3.25, 20.25), (3.05, 20.90), (2.72, 21.32), (2.35, 21.50),
]
cap_inner_profile = [(max(0.2, r - 0.28), z - (0.02 if i > 0 else -0.18)) for i, (r, z) in enumerate(cap_outer_profile)]
cap_shell = partial_profile_shell("cap_cutaway", cap_outer_profile, cap_inner_profile, collection=CUTAWAY)
apply_evidence(cap_shell, "verified_external_schematic_internal", "cap_mechanism_omitted", ["F-LID-PHOTO"])

inner_wall = partial_shell("inner_vessel", 2.50, 2.34, 0.64, 16.05, collection=CUTAWAY, side_mat=MAT_STEEL)
apply_evidence(inner_wall, "principle_verified", "thickness_and_profile_schematic", ["F-VACUUM-PRINCIPLE"])

reflective = partial_shell("reflective_layer", 2.61, 2.53, 0.72, 15.92, collection=CUTAWAY, side_mat=MAT_REFLECT)
apply_evidence(reflective, "principle_verified_not_model_specific", "thickness_exaggerated", ["F-REFLECTIVE-PRINCIPLE"])

# Vacuum remains empty. Two very thin cyan boundary markers make the gap readable.
vacuum_outer_marker = partial_shell("vacuum_gap_outer_marker", 2.94, 2.91, 0.62, 16.02, collection=CUTAWAY, side_mat=MAT_VACUUM, cut_mat=MAT_VACUUM)
vacuum_inner_marker = partial_shell("vacuum_gap_inner_marker", 2.67, 2.64, 0.70, 15.94, collection=CUTAWAY, side_mat=MAT_VACUUM, cut_mat=MAT_VACUUM)
for obj in (vacuum_outer_marker, vacuum_inner_marker):
    apply_evidence(obj, "principle_verified", "boundary_marker_not_material", ["F-VACUUM-PRINCIPLE"])

water = partial_sector("hot_water", 2.28, 0.82, 14.72, collection=CUTAWAY)
apply_evidence(water, "illustrative_content", "fill_level_schematic", ["F-THERMAL-TEST-CONTEXT"])

neck_bridge = partial_shell("neck_heat_bridge", 2.90, 2.42, 15.82, 16.52, collection=CUTAWAY, side_mat=MAT_STEEL)
apply_evidence(neck_bridge, "principle_verified", "exact_geometry_schematic", ["F-NECK-HEAT-PATH"])

gasket = partial_shell("cap_gasket", 2.62, 2.28, 16.72, 17.08, collection=CUTAWAY, side_mat=MAT_GASKET, cut_mat=MAT_GASKET)
apply_evidence(gasket, "presence_verified", "exact_profile_schematic", ["F-LID-PHOTO", "F-PRODUCT-PAGE"])

for name, location, status in [
    ("ANCHOR_INNER_WALL", (2.50, -0.15, 10.0), "principle_verified"),
    ("ANCHOR_REFLECTIVE", (2.61, -0.15, 11.4), "principle_verified_not_model_specific"),
    ("ANCHOR_VACUUM_GAP", (2.80, -0.15, 8.5), "principle_verified"),
    ("ANCHOR_HOT_WATER", (1.20, -0.15, 9.6), "illustrative_content"),
    ("ANCHOR_NECK", (2.65, -0.15, 16.15), "principle_verified"),
]:
    empty = bpy.data.objects.new(name, None)
    empty.empty_display_type = "SPHERE"
    empty.empty_display_size = 0.18
    empty.location = location
    empty["evidence_status"] = status
    CUTAWAY.objects.link(empty)


def point_camera(camera, target=(0, 0, 10.75)):
    direction = Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


scene = bpy.context.scene
scene.render.engine = "BLENDER_EEVEE"
scene.render.resolution_x = 1000
scene.render.resolution_y = 1000
scene.render.resolution_percentage = 100
scene.render.image_settings.file_format = "PNG"
scene.view_settings.look = "AgX - Medium High Contrast"
camera = bpy.data.objects.get("validation_camera")
scene.camera = camera

for obj in EXTERIOR.objects:
    obj.hide_render = True
    obj.hide_viewport = True
for obj in CUTAWAY.objects:
    obj.hide_render = False
    obj.hide_viewport = False

camera.location = (28.0, -36.0, 15.0)
point_camera(camera)
scene.render.filepath = os.path.join(RENDER_DIR, "cutaway_three_quarter.png")
bpy.ops.render.render(write_still=True)

camera.location = (0.0, -44.0, 12.5)
point_camera(camera)
scene.render.filepath = os.path.join(RENDER_DIR, "cutaway_front.png")
bpy.ops.render.render(write_still=True)

# Exploded validation pose: offsets are schematic and restored after rendering.
exploded_offsets = {
    "outer_wall_cutaway": Vector((-5.0, 0.0, 0.0)),
    "cap_cutaway": Vector((-5.0, 0.0, 0.0)),
    "vacuum_gap_outer_marker": Vector((-2.5, 0.0, 0.0)),
    "vacuum_gap_inner_marker": Vector((-2.5, 0.0, 0.0)),
    "reflective_layer": Vector((0.0, 0.0, 0.0)),
    "inner_vessel": Vector((2.5, 0.0, 0.0)),
    "neck_heat_bridge": Vector((2.5, 0.0, 0.0)),
    "cap_gasket": Vector((2.5, 0.0, 0.0)),
    "hot_water": Vector((5.0, 0.0, 0.0)),
}
original_locations = {}
for name, offset in exploded_offsets.items():
    obj = bpy.data.objects.get(name)
    if obj:
        original_locations[name] = obj.location.copy()
        obj.location += offset
camera.location = (32.0, -47.0, 17.0)
point_camera(camera, target=(0, 0, 10.0))
scene.render.filepath = os.path.join(RENDER_DIR, "exploded_three_quarter.png")
bpy.ops.render.render(write_still=True)
for name, location in original_locations.items():
    bpy.data.objects[name].location = location

manifest = {
    "asset": "Zojirushi SM-WA48-inspired thermos reconstruction",
    "version": "0.2",
    "model_scope": "educational cutaway; not manufacturing CAD",
    "external_dimensions_cm": {"width": 6.5, "depth": 7.0, "height": 21.5, "status": "official_approx"},
    "components": {
        obj.name: {
            "evidence_status": obj.get("evidence_status"),
            "geometry_status": obj.get("geometry_status"),
            "source_ids": obj.get("source_ids", "").split(",") if obj.get("source_ids") else [],
        }
        for obj in CUTAWAY.objects
        if obj.type == "MESH"
    },
    "prohibited_claims": [
        "Internal wall thickness is exact",
        "Vacuum gap width is exact",
        "Reflective layer material or thickness is confirmed for SM-WA48",
        "Cap internal mechanism is a faithful manufacturing reconstruction",
    ],
}
with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest, f, ensure_ascii=False, indent=2)

# Save in intact-review state. Cutaway remains available as a named collection.
for obj in EXTERIOR.objects:
    obj.hide_render = False
    obj.hide_viewport = False
for obj in CUTAWAY.objects:
    obj.hide_render = True
    obj.hide_viewport = True
bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
print(f"SAVED_BLEND={BLEND_PATH}")
print(f"MANIFEST={MANIFEST_PATH}")
print(f"RENDER_DIR={RENDER_DIR}")
