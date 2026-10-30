"""
Render Style B Frame (Line-Art / Cel-Shading) with Transparent Background
Enables flawless compositing on both:
1. Pure VOLT DS Paper (#FFFFFA)
2. Contextual Minimalist Tabletop Environment
"""
import bpy
import math
import os
from mathutils import Vector

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
RENDER_DIR = os.path.join(ROOT, "work", "termos-3d")
OUT_IMG = os.path.join(RENDER_DIR, "style_b_base_transparent.png")
os.makedirs(RENDER_DIR, exist_ok=True)


def clear_scene():
    bpy.ops.object.select_all(action="SELECT")
    bpy.ops.object.delete(use_global=False)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights, bpy.data.linestyles):
        pass


def create_material(name, color, roughness=0.5, metallic=0.0, emission_color=(0, 0, 0), emission_strength=0.0):
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


def lathe_mesh(name, profile, start_angle=0.0, end_angle=math.pi, segments=96, mat=None):
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


def create_rounded_box(name, location, dimensions, mat):
    bpy.ops.mesh.primitive_cube_add(location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for poly in obj.data.polygons:
        poly.use_smooth = True
    if mat:
        obj.data.materials.append(mat)
    return obj


def build_model():
    mat_outer = create_material("mat_outer_ice_gray", (0.43, 0.57, 0.58), roughness=0.35, metallic=0.05)
    mat_vacuum = create_material("mat_vacuum_gap", (0.05, 0.05, 0.06), roughness=0.9, metallic=0.0)
    mat_copper = create_material("mat_copper_shield", (0.95, 0.62, 0.22), roughness=0.25, metallic=0.85)
    mat_inner_steel = create_material("mat_inner_steel", (0.85, 0.86, 0.88), roughness=0.20, metallic=0.90)
    mat_liquid = create_material("mat_tea_liquid", (0.75, 0.28, 0.08), roughness=0.15, metallic=0.0, emission_color=(0.9, 0.35, 0.1), emission_strength=0.15)
    mat_silicone = create_material("mat_silicone_stopper", (0.92, 0.90, 0.85), roughness=0.55, metallic=0.0)
    mat_lid_plastic = create_material("mat_lid_plastic", (0.22, 0.24, 0.26), roughness=0.40, metallic=0.0)
    mat_mouthpiece = create_material("mat_mouthpiece", (0.88, 0.89, 0.87), roughness=0.30, metallic=0.0)
    mat_accent_button = create_material("mat_accent_button", (0.85, 0.86, 0.85), roughness=0.30, metallic=0.1)
    mat_dark_trim = create_material("mat_dark_trim", (0.15, 0.16, 0.17), roughness=0.45, metallic=0.0)

    start_a = 0.0
    end_a = math.pi

    outer_shell_profile = [
        (0.00, 0.00), (3.00, 0.00), (3.20, 0.08), (3.25, 0.25),
        (3.25, 16.50), (3.20, 16.85), (3.00, 17.00), (2.85, 17.00),
        (2.85, 16.70), (3.10, 16.50), (3.13, 0.35), (2.95, 0.12), (0.00, 0.12)
    ]
    lathe_mesh("outer_shell_cutaway", outer_shell_profile, start_a, end_a, segments=96, mat=mat_outer)

    vacuum_gap_profile = [
        (0.00, 0.12), (2.95, 0.12), (3.13, 0.35), (3.13, 16.50),
        (2.85, 16.70), (2.85, 16.75), (2.93, 16.60), (2.93, 0.55),
        (2.75, 0.32), (0.00, 0.32)
    ]
    lathe_mesh("vacuum_gap_cutaway", vacuum_gap_profile, start_a, end_a, segments=96, mat=mat_vacuum)

    copper_shield_profile = [
        (0.00, 0.32), (2.75, 0.32), (2.93, 0.55), (2.93, 16.60),
        (2.85, 16.75), (2.85, 16.78), (2.90, 16.62), (2.90, 0.58),
        (2.72, 0.35), (0.00, 0.35)
    ]
    lathe_mesh("copper_shield_cutaway", copper_shield_profile, start_a, end_a, segments=96, mat=mat_copper)

    inner_wall_profile = [
        (0.00, 0.35), (2.72, 0.35), (2.90, 0.58), (2.90, 16.62),
        (2.85, 16.78), (2.40, 17.00), (2.00, 17.00), (2.00, 16.88),
        (2.35, 16.88), (2.78, 16.50), (2.78, 0.68), (2.60, 0.47), (0.00, 0.47)
    ]
    lathe_mesh("inner_wall_cutaway", inner_wall_profile, start_a, end_a, segments=96, mat=mat_inner_steel)

    liquid_profile = [
        (0.00, 0.47), (2.60, 0.47), (2.78, 0.68), (2.78, 16.20),
        (0.00, 16.20)
    ]
    lathe_mesh("hot_liquid_cutaway", liquid_profile, start_a, end_a, segments=96, mat=mat_liquid)

    stopper_profile = [
        (0.00, 16.10), (1.95, 16.10), (2.05, 16.35), (2.05, 17.10),
        (2.25, 17.30), (2.25, 17.55), (1.80, 17.55), (1.80, 16.90),
        (0.00, 16.90)
    ]
    lathe_mesh("silicone_stopper_cutaway", stopper_profile, start_a, end_a, segments=96, mat=mat_silicone)

    lid_profile = [
        (0.00, 17.00), (3.30, 17.00), (3.35, 17.20), (3.35, 20.80),
        (3.10, 21.30), (2.50, 21.50), (0.00, 21.50), (0.00, 21.10),
        (2.35, 21.10), (2.90, 20.70), (2.95, 17.50), (2.00, 17.50),
        (2.00, 17.10), (0.00, 17.10)
    ]
    lathe_mesh("lid_assembly_cutaway", lid_profile, start_a, end_a, segments=96, mat=mat_lid_plastic)

    spout_profile = [
        (1.50, 17.05), (2.30, 17.05), (2.35, 17.80), (2.10, 18.50),
        (1.70, 18.50), (1.80, 17.80), (1.50, 17.80)
    ]
    lathe_mesh("mouthpiece_spout", spout_profile, start_a, end_a, segments=96, mat=mat_mouthpiece)

    create_rounded_box("release_button", (0.00, 3.34, 18.78), (1.45, 0.30, 2.10), mat_accent_button)
    create_rounded_box("hinge_block", (0.00, 3.32, 18.30), (1.55, 0.36, 1.10), mat_dark_trim)


def setup_stage():
    world = bpy.context.scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    bg.inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0)
    bg.inputs["Strength"].default_value = 1.0

    lights = [
        ("key_light", (-16, -26, 32), 1100, 12.0),
        ("fill_light", (20, -14, 22), 700, 10.0),
        ("rim_back_light", (0, 22, 28), 850, 8.0),
        ("under_bounce", (0, -10, 2), 300, 6.0),
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
    cam.location = Vector((0.0, -60.0, 10.75))
    target = Vector((0.0, 0.0, 10.75))
    direction = target - cam.location
    cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
    bpy.context.scene.camera = cam
    bpy.context.view_layer.update()
    return cam


def setup_freestyle_cel_shading():
    scene = bpy.context.scene
    scene.render.use_freestyle = True
    scene.render.line_thickness = 1.8

    vl = bpy.context.view_layer
    fs = vl.freestyle_settings
    lineset = fs.linesets.get("LineSet") or fs.linesets.new("LineSet")
    lineset.select_silhouette = True
    lineset.select_crease = True
    lineset.select_border = True
    lineset.select_material_boundary = True

    style = lineset.linestyle
    style.color = (0.063, 0.067, 0.063)
    style.thickness = 1.8


def render():
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    scene.render.resolution_x = 1080
    scene.render.resolution_y = 1920
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.render.image_settings.color_mode = "RGBA"
    scene.render.film_transparent = True  # TRANSPARENT ALPHA BACKGROUND
    scene.view_settings.view_transform = "Standard"  # TRUE UN-REMAP-ED SCOLORS
    scene.render.filepath = OUT_IMG

    print(f"Rendering Style B Transparent 3D base to {OUT_IMG}...")
    bpy.ops.render.render(write_still=True)
    print("Transparent 3D Base render complete!")


if __name__ == "__main__":
    clear_scene()
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 0.01
    bpy.context.scene.unit_settings.length_unit = "CENTIMETERS"
    build_model()
    setup_stage()
    setup_freestyle_cel_shading()
    render()
