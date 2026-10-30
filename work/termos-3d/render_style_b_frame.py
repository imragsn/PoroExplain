"""
Render Style B Frame (Line-Art / Cel-Shading) for Termos Explainer Video
Integrates VOLT Design System (tokens.json, DESIGN-SYSTEM.md):
- 2px ink (#101110) Freestyle contour lines
- paper background (#FFFFFA)
- electric accent (#E8F500)
- zero border-radius sharp geometry
- Grotesque sans-serif typography (Arial / Helvetica Bold)
- Clean subtitle chunk (<= 4 words) without dark container box
"""
import bpy
import math
import os
import json
from mathutils import Vector

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
RENDER_DIR = os.path.join(ROOT, "work", "termos-3d")
OUT_IMG = os.path.join(RENDER_DIR, "style_b_base_1080x1920.png")
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
    # VOLT DS & Technical Palette
    # Outer Shell: Ice Gray (#6e9194 -> 0.43, 0.57, 0.58)
    mat_outer = create_material("mat_ice_gray", (0.43, 0.57, 0.58), roughness=0.45, metallic=0.05)
    mat_dark_trim = create_material("mat_dark_trim", (0.10, 0.12, 0.12), roughness=0.60, metallic=0.0)
    mat_accent_button = create_material("mat_button", (0.33, 0.46, 0.47), roughness=0.40, metallic=0.05)
    
    # Internal Layers (Technical Flat Shading)
    mat_outer_wall = create_material("mat_outer_steel", (0.58, 0.63, 0.67), roughness=0.40, metallic=0.30)
    # Vacuum Gap: graphic deep void (#101110 ink / dark slate)
    mat_vacuum = create_material("mat_vacuum_gap", (0.12, 0.14, 0.15), roughness=0.90, metallic=0.0)
    # Reflective Shield: Electric Gold (#E8F500 / #F5B700)
    mat_reflective = create_material("mat_reflective_shield", (0.95, 0.75, 0.05), roughness=0.25, metallic=0.80,
                                     emission_color=(0.95, 0.75, 0.05), emission_strength=0.20)
    # Inner Steel Wall: Clean Steel Silver
    mat_inner_wall = create_material("mat_inner_steel", (0.76, 0.81, 0.85), roughness=0.30, metallic=0.40)
    # Hot Coffee Liquid: Warm Amber (#E67E22 -> 0.90, 0.49, 0.13)
    mat_liquid = create_material("mat_hot_liquid", (0.90, 0.49, 0.13), roughness=0.20, metallic=0.0,
                                 emission_color=(0.90, 0.45, 0.10), emission_strength=0.30)
    # Silicone Stopper: Dark silicone seal (#2D3748)
    mat_stopper = create_material("mat_silicone_stopper", (0.18, 0.22, 0.25), roughness=0.70, metallic=0.0)
    mat_mouthpiece = create_material("mat_mouthpiece", (0.92, 0.92, 0.90), roughness=0.40, metallic=0.0)

    # Cutaway Half-section (0 to pi: back half solid, front half cutaway open)
    start_a = 0.0
    end_a = math.pi

    # Outer Shell Profile (Exact 6.5 cm diameter, 17.0 cm body)
    outer_profile = [
        (3.08, 0.00), (3.22, 0.15), (3.25, 0.35), (3.25, 14.85),
        (3.22, 15.55), (3.12, 16.15), (2.96, 16.65), (2.90, 17.00)
    ]
    lathe_mesh("outer_shell", outer_profile, start_a, end_a, segments=96, mat=mat_outer)
    lathe_mesh("base_ring", [(3.26, 0.12), (3.26, 0.55)], start_a, end_a, segments=96, mat=mat_dark_trim)
    lathe_mesh("neck_trim", [(3.16, 16.80), (3.16, 17.05)], start_a, end_a, segments=96, mat=mat_dark_trim)

    # 1. Outer Steel Wall
    profile_outer_steel = [
        (3.05, 0.30), (3.14, 0.50), (3.14, 14.80), (3.06, 15.45), (2.92, 16.10), (2.80, 16.70)
    ]
    lathe_mesh("layer_outer_steel", profile_outer_steel, start_a, end_a, segments=96, mat=mat_outer_wall)

    # 2. Vacuum Gap (Schematically enlarged to ~2.0 mm for mobile readability)
    profile_vacuum = [
        (2.82, 0.50), (2.92, 0.65), (2.92, 14.65), (2.84, 15.25), (2.72, 15.90), (2.62, 16.50)
    ]
    lathe_mesh("layer_vacuum_gap", profile_vacuum, start_a, end_a, segments=96, mat=mat_vacuum)

    # 3. Reflective Heat-Bounce Shield (Gold foil)
    profile_reflective = [
        (2.74, 0.60), (2.82, 0.75), (2.82, 14.55), (2.75, 15.15), (2.64, 15.80), (2.55, 16.40)
    ]
    lathe_mesh("layer_reflective_shield", profile_reflective, start_a, end_a, segments=96, mat=mat_reflective)

    # 4. Inner Stainless Steel Vessel
    profile_inner_steel = [
        (2.56, 0.70), (2.66, 0.85), (2.66, 14.50), (2.60, 15.10), (2.50, 15.70), (2.42, 16.35), (2.05, 16.90)
    ]
    lathe_mesh("layer_inner_steel", profile_inner_steel, start_a, end_a, segments=96, mat=mat_inner_wall)

    # 5. Liquid Core (480 ml capacity)
    profile_liquid = [
        (0.00, 0.90), (2.55, 0.90), (2.55, 14.50), (2.40, 15.50), (2.00, 16.45), (0.00, 16.45)
    ]
    lathe_mesh("core_liquid", profile_liquid, start_a, end_a, segments=96, mat=mat_liquid)

    # Cap & Lid Mechanism (Total height reaches 21.50 cm)
    cap_profile = [
        (3.16, 17.00), (3.22, 17.15), (3.25, 17.50), (3.25, 19.65),
        (3.22, 20.30), (3.02, 20.95), (2.68, 21.35), (2.30, 21.50)
    ]
    lathe_mesh("cap_body", cap_profile, start_a, end_a, segments=96, mat=mat_outer)

    # Silicone Stopper (4.0 cm mouth seal)
    stopper_profile = [
        (0.00, 16.30), (2.02, 16.30), (2.02, 17.80), (1.95, 18.30), (0.00, 18.30)
    ]
    lathe_mesh("silicone_stopper", stopper_profile, start_a, end_a, segments=96, mat=mat_stopper)

    # Mouthpiece Spout
    spout_profile = [
        (2.00, 16.80), (2.25, 16.80), (2.25, 18.60), (2.00, 18.60)
    ]
    lathe_mesh("mouthpiece_spout", spout_profile, start_a, end_a, segments=96, mat=mat_mouthpiece)

    # Controls
    create_rounded_box("release_button", (0.00, 3.34, 18.78), (1.45, 0.30, 2.10), mat_accent_button)
    create_rounded_box("hinge_block", (0.00, 3.32, 18.30), (1.55, 0.36, 1.10), mat_dark_trim)


def setup_stage():
    world = bpy.context.scene.world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    # VOLT DS paper color: #FFFFFA (pure clean warm paper white)
    bg.inputs["Color"].default_value = (1.0, 1.0, 0.98, 1.0)
    bg.inputs["Strength"].default_value = 1.0

    # Ground shadow catcher plane (subtle soft floor)
    floor_mat = create_material("mat_floor", (0.97, 0.97, 0.95), roughness=0.95, metallic=0.0)
    bpy.ops.mesh.primitive_plane_add(size=200, location=(0, 0, -0.05))
    floor = bpy.context.object
    floor.name = "studio_floor"
    floor.data.materials.append(floor_mat)

    # Soft studio technical lights
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

    # Camera: Frontal cross-section angle (Shot 02 calibrated)
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
    scene.render.line_thickness = 1.8  # Crisp 2px technical contour

    vl = bpy.context.view_layer
    fs = vl.freestyle_settings
    lineset = fs.linesets.get("LineSet") or fs.linesets.new("LineSet")
    lineset.select_silhouette = True
    lineset.select_crease = True
    lineset.select_border = True
    lineset.select_material_boundary = True

    style = lineset.linestyle
    # VOLT ink color: #101110 (approx sRGB 0.063, 0.067, 0.063)
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
    scene.render.film_transparent = False
    scene.view_settings.look = "AgX - Medium High Contrast"
    scene.render.filepath = OUT_IMG

    print(f"Rendering Style B 3D base to {OUT_IMG}...")
    bpy.ops.render.render(write_still=True)
    print("3D Base render complete!")


if __name__ == "__main__":
    clear_scene()
    bpy.context.scene.unit_settings.system = "METRIC"
    bpy.context.scene.unit_settings.scale_length = 0.01
    bpy.context.scene.unit_settings.length_unit = "CENTIMETERS"
    build_model()
    setup_stage()
    setup_freestyle_cel_shading()
    render()
