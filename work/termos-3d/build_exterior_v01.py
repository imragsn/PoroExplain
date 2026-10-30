import bpy
import math
import os
from mathutils import Vector


ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
RENDER_DIR = os.path.join(ROOT, "work", "termos-3d", "renders-v01")
BLEND_PATH = os.path.join(ROOT, "outputs", "termos-03-master-exterior-v0.1.blend")
os.makedirs(RENDER_DIR, exist_ok=True)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.curves, bpy.data.materials, bpy.data.cameras, bpy.data.lights):
        pass


def material(name, color, roughness=0.55, metallic=0.0):
    mat = bpy.data.materials.new(name)
    mat.diffuse_color = (*color, 1.0)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*color, 1.0)
        bsdf.inputs["Roughness"].default_value = roughness
        bsdf.inputs["Metallic"].default_value = metallic
    return mat


def lathe(name, profile, segments=128, y_scale=1.0, mat=None):
    verts = []
    for radius, z in profile:
        for i in range(segments):
            a = 2.0 * math.pi * i / segments
            verts.append((radius * math.cos(a), radius * math.sin(a) * y_scale, z))
    faces = []
    rings = len(profile)
    for j in range(rings - 1):
        for i in range(segments):
            ni = (i + 1) % segments
            a = j * segments + i
            b = j * segments + ni
            c = (j + 1) * segments + ni
            d = (j + 1) * segments + i
            faces.append((a, b, c, d))
    faces.append(tuple(reversed(tuple(range(segments)))))
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


def rounded_box(name, location, dimensions, bevel, mat):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    mod = obj.modifiers.new("edge_rounding", "BEVEL")
    mod.width = bevel
    mod.segments = 6
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.modifier_apply(modifier=mod.name)
    for poly in obj.data.polygons:
        poly.use_smooth = True
    obj.data.materials.append(mat)
    return obj


def cylinder(name, radius, depth, location, scale_y, mat, bevel=0.0, vertices=128):
    bpy.ops.mesh.primitive_cylinder_add(vertices=vertices, radius=radius, depth=depth, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.scale.y = scale_y
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    if bevel:
        mod = obj.modifiers.new("edge_rounding", "BEVEL")
        mod.width = bevel
        mod.segments = 6
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
    for poly in obj.data.polygons:
        poly.use_smooth = True
    obj.data.materials.append(mat)
    return obj


def add_logo(mat):
    # Small verified placement cue only; not a trademark-shape reconstruction.
    rounded_box("brand_mark_placeholder", (0.0, -3.265, 5.1), (0.75, 0.035, 0.38), 0.09, mat)


def create_model():
    ice_gray = material("ice_gray_body", (0.43, 0.57, 0.58), 0.42, 0.05)
    ice_gray_dark = material("ice_gray_shadow", (0.22, 0.31, 0.32), 0.48, 0.03)
    button_mat = material("button_face", (0.34, 0.47, 0.48), 0.38, 0.02)
    seam_mat = material("seam_detail", (0.12, 0.19, 0.20), 0.50, 0.00)

    body_profile = [
        (3.08, 0.00),
        (3.20, 0.12),
        (3.25, 0.35),
        (3.25, 14.65),
        (3.22, 15.25),
        (3.12, 15.85),
        (2.96, 16.32),
        (2.90, 16.70),
    ]
    lathe("outer_shell", body_profile, y_scale=1.0, mat=ice_gray)

    cylinder("base_ring", 3.26, 0.42, (0, 0, 0.34), 1.0, ice_gray_dark, bevel=0.10)
    cylinder("neck_band", 3.18, 0.50, (0, 0, 16.76), 1.0, ice_gray_dark, bevel=0.09)

    cap_profile = [
        (3.18, 16.70),
        (3.23, 16.88),
        (3.25, 17.28),
        (3.25, 19.55),
        (3.25, 20.25),
        (3.05, 20.90),
        (2.72, 21.32),
        (2.35, 21.50),
    ]
    lathe("cap_outer", cap_profile, y_scale=1.0, mat=ice_gray)

    # Front is negative Y. Controls are separate so they can animate later.
    rounded_box("release_button", (0.00, -3.34, 18.78), (1.45, 0.30, 2.10), 0.28, button_mat)
    rounded_box("release_button_inset", (0.00, -3.50, 18.78), (1.00, 0.04, 1.58), 0.22, ice_gray_dark)
    rounded_box("safety_lock", (1.62, -3.32, 18.55), (1.15, 0.30, 0.74), 0.18, button_mat)
    rounded_box("safety_lock_ridge", (1.62, -3.48, 18.55), (0.60, 0.04, 0.25), 0.08, seam_mat)
    rounded_box("hinge_block", (0.00, 3.32, 18.30), (1.55, 0.36, 1.10), 0.24, ice_gray_dark)
    add_logo(seam_mat)

    # Empty locators become stable animation/label anchors.
    for name, pos in {
        "ANCHOR_CAP": (0, -3.6, 19.0),
        "ANCHOR_BODY": (0, -3.35, 10.0),
        "ANCHOR_BASE": (0, -3.35, 0.4),
        "ANCHOR_HINGE": (0, 3.5, 18.4),
    }.items():
        empty = bpy.data.objects.new(name, None)
        empty.empty_display_type = "PLAIN_AXES"
        empty.empty_display_size = 0.45
        empty.location = pos
        bpy.context.collection.objects.link(empty)


def point_camera(camera, target=(0, 0, 10.75)):
    direction = Vector(target) - camera.location
    camera.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()


def create_stage():
    world = bpy.context.scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (0.78, 0.73, 0.64, 1.0)
    bg.inputs["Strength"].default_value = 0.30

    floor_mat = material("warm_floor", (0.62, 0.57, 0.48), 0.88, 0.0)
    bpy.ops.mesh.primitive_plane_add(size=160, location=(0, 0, -0.02))
    floor = bpy.context.object
    floor.name = "validation_floor"
    floor.data.materials.append(floor_mat)

    for name, location, energy, size in [
        ("key_light", (-12, -18, 30), 1050, 9.0),
        ("fill_light", (16, -8, 19), 650, 7.0),
        ("rim_light", (2, 17, 26), 850, 6.0),
    ]:
        data = bpy.data.lights.new(name, type="AREA")
        data.energy = energy
        data.shape = "DISK"
        data.size = size
        light = bpy.data.objects.new(name, data)
        bpy.context.collection.objects.link(light)
        light.location = location
        direction = Vector((0, 0, 10)) - light.location
        light.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()

    cam_data = bpy.data.cameras.new("validation_camera")
    cam = bpy.data.objects.new("validation_camera", cam_data)
    bpy.context.collection.objects.link(cam)
    cam.data.lens = 68
    cam.data.sensor_width = 36
    bpy.context.scene.camera = cam
    return cam


def render_views(cam):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 900
    scene.render.resolution_y = 900
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = False
    scene.render.image_settings.color_depth = "8"
    scene.view_settings.look = "AgX - Medium High Contrast"

    views = {
        "front": (0.0, -43.0, 12.0),
        "three_quarter": (27.0, -34.0, 14.0),
        "side": (43.0, 0.0, 12.0),
        "rear_three_quarter": (24.0, 35.0, 14.0),
    }
    for name, location in views.items():
        cam.location = location
        point_camera(cam)
        scene.render.filepath = os.path.join(RENDER_DIR, f"{name}.png")
        bpy.ops.render.render(write_still=True)


clear_scene()
bpy.context.scene.unit_settings.system = "METRIC"
bpy.context.scene.unit_settings.scale_length = 0.01
bpy.context.scene.unit_settings.length_unit = "CENTIMETERS"
create_model()
camera = create_stage()
render_views(camera)
bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH)
print(f"SAVED_BLEND={BLEND_PATH}")
print(f"RENDER_DIR={RENDER_DIR}")
