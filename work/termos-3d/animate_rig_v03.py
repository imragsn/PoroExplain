import bpy
import math
import os
import json
import time
from mathutils import Vector, Euler

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
INPUT_BLEND = os.path.join(ROOT, "outputs", "termos-03-master-semi-realis-v0.3.blend")
OUTPUT_BLEND = os.path.join(ROOT, "outputs", "termos-03-animated-semi-realis-v0.3.blend")
FRAMES_DIR = os.path.join(ROOT, "work", "termos-3d", "anim_frames")
ANCHORS_OUTPUT = os.path.join(ROOT, "outputs", "termos-05-anim-anchors-v0.3.json")

os.makedirs(FRAMES_DIR, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=INPUT_BLEND)
scene = bpy.context.scene

# Scene setup: 30 fps, 1680 frames (0 to 1679) = 55.967s matching audio master 55.968s
scene.render.fps = 30
scene.frame_start = 0
scene.frame_end = 1679

# Render settings: EEVEE Next with Raytracing, shadows & fast GI
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100

scene.eevee.use_raytracing = True
scene.eevee.use_fast_gi = True
scene.eevee.taa_render_samples = 4
scene.eevee.use_shadows = True

scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure = 0.05

# Balanced lights
for light in bpy.data.lights:
    if "Backdrop" in light.name:
        light.energy = 2400.0
    elif "Rim" in light.name:
        light.energy = 2800.0
    elif "Key" in light.name:
        light.energy = 2200.0
    elif "Fill" in light.name:
        light.energy = 1200.0
    elif "Top" in light.name:
        light.energy = 1400.0

cam = bpy.data.objects.get("CAM_SemiReal_Master")
root = bpy.data.objects.get("GEO_TERMOS_ROOT")
grp_cap = bpy.data.objects.get("GRP_CAP_ASSEMBLY")
grp_collar = bpy.data.objects.get("GRP_CAP_COLLAR")
grp_stopper = bpy.data.objects.get("GRP_SILICONE_STOPPER_SSS")
grp_spout = bpy.data.objects.get("GRP_MOUTHPIECE_SPOUT")
grp_door = bpy.data.objects.get("GRP_OUTER_SHELL_RIGHT")
grp_arrows = bpy.data.objects.get("GRP_THERMAL_BOUNCE_ARROWS")
grp_particles = bpy.data.objects.get("GRP_VACUUM_PARTICLES")

# Clear existing animation data if any
for obj in [cam, root, grp_cap, grp_collar, grp_stopper, grp_spout, grp_door, grp_arrows, grp_particles]:
    if obj and obj.animation_data:
        obj.animation_data_clear()

# Camera Focus Target Empty (animates smoothly so camera always tracks target)
cam_target = bpy.data.objects.new("CAM_Focus_Target", None)
cam_target.empty_display_type = "SPHERE"
cam_target.empty_display_size = 0.5
bpy.context.collection.objects.link(cam_target)

# Add Track-To constraint to camera
tt = cam.constraints.new(type='TRACK_TO')
tt.target = cam_target
tt.track_axis = 'TRACK_NEGATIVE_Z'
tt.up_axis = 'UP_Y'


def set_kfs(obj, data_path, keyframes):
    """Sets keyframes with default Bezier interpolation."""
    for f, val in keyframes:
        if isinstance(val, (tuple, list, Vector, Euler)):
            for idx, subval in enumerate(val):
                setattr(getattr(obj, data_path), "xyz"[idx], subval)
                obj.keyframe_insert(data_path=data_path, index=idx, frame=f)
        else:
            setattr(obj, data_path, val)
            obj.keyframe_insert(data_path=data_path, frame=f)


# ------------------------------------------------------------------------------
# 1. CAMERA POSITION & TARGET KEYFRAMES (16-BEAT CINEMATIC CHOREOGRAPHY)
# ------------------------------------------------------------------------------
# Camera positions (X, Y, Z) in cm
cam_kfs = [
    (0,    Vector((16.0, -56.0, 10.5))),  # B-01: Low angle hero push-in
    (66,   Vector((14.0, -48.0, 12.0))),
    (111,  Vector((11.0, -40.0, 18.0))),  # B-02: Tilt up to mouth
    (160,  Vector((19.0, -50.0, 16.0))),  # B-03: Quick orbit & dolly out (cap opens)
    (228,  Vector((15.0, -43.0, 13.0))),  # B-04: Dolly in to splitting shell
    (336,  Vector((9.0,  -38.0, 12.0))),  # B-05: Truck left to profile walls
    (456,  Vector((4.5,  -28.0, 11.2))),  # B-06: Macro close-up on 2mm vacuum gap
    (534,  Vector((4.5,  -28.0, 14.2))),  # B-07: Vertical track along vacuum gap
    (612,  Vector((17.0, -45.0, 13.5))),  # B-08: Pull back mild
    (726,  Vector((27.0, -35.0, 15.0))),  # B-09: 40 deg orbit to inner vessel & core
    (825,  Vector((23.0, -37.0, 10.5))),  # B-10: Arc shot catching Copper/Gold mirror
    (915,  Vector((18.0, -36.0, 12.0))),  # B-11: Push in to heat bounce point
    (1059, Vector((13.0, -38.0, 20.5))),  # B-12: Whip-tilt up to exploding stopper
    (1167, Vector((16.0, -36.0, 19.5))),  # B-13: Close orbit around neck leak path
    (1296, Vector((22.0, -66.0, 17.0))),  # B-14: Crane down & pull out (full exploded)
    (1450, Vector((18.0, -67.0, 16.8))),  # B-15A: Slow orbital drift (metric card)
    (1593, Vector((14.0, -68.0, 16.5))),  # B-15B: Slow orbital drift
    (1679, Vector((16.0, -56.0, 10.5))),  # B-16: Smooth return to B-01 loop coords!
]
set_kfs(cam, "location", cam_kfs)

# Camera Focus Target positions (X, Y, Z)
target_kfs = [
    (0,    Vector((0.0, 0.0, 10.5))),
    (66,   Vector((0.0, 0.0, 11.5))),
    (111,  Vector((0.0, 0.0, 17.5))),  # Focus mouth
    (160,  Vector((0.0, 0.0, 16.0))),
    (228,  Vector((0.0, 0.0, 11.5))),  # Focus split
    (336,  Vector((0.5, 0.0, 11.5))),
    (456,  Vector((2.8, 0.0, 11.2))),  # Focus 2mm vacuum gap
    (534,  Vector((2.8, 0.0, 14.2))),
    (612,  Vector((0.0, 0.0, 11.5))),
    (726,  Vector((-0.2, 0.0, 11.0))), # Focus liquid core
    (825,  Vector((1.5, 0.0, 9.5))),   # Focus copper mirror
    (915,  Vector((0.5, 0.0, 10.0))),
    (1059, Vector((0.0, 0.0, 19.5))),  # Focus exploding stopper
    (1167, Vector((0.0, 0.0, 18.0))),  # Focus neck
    (1296, Vector((-0.2, 0.0, 13.0))), # Focus full exploded architecture
    (1450, Vector((-0.2, 0.0, 13.0))),
    (1593, Vector((-0.2, 0.0, 13.0))),
    (1679, Vector((0.0, 0.0, 10.5))),  # Focus B-01 loop
]
set_kfs(cam_target, "location", target_kfs)

# Camera Lens / Focal Length (DoF & Macro Zooms)
lens_kfs = [
    (0,    68.0),
    (66,   70.0),
    (111,  74.0),
    (160,  68.0),
    (336,  70.0),
    (456,  84.0),  # Macro telephoto on vacuum gap
    (534,  84.0),
    (612,  68.0),
    (1059, 72.0),
    (1296, 68.0),
    (1679, 68.0),
]
for f, l in lens_kfs:
    cam.data.lens = l
    cam.data.keyframe_insert(data_path="lens", frame=f)


# ------------------------------------------------------------------------------
# 2. COMPONENT ANIMATION KEYFRAMES (PEELING, AXIAL EXPLODE, HINGE FLIP, LOOP)
# ------------------------------------------------------------------------------
# A. Flip Lid Opening (Rotation X on rear hinge: 0 -> -36 deg -> 0)
cap_rot_kfs = [
    (0,    Euler((0.0, 0.0, 0.0))),
    (111,  Euler((0.0, 0.0, 0.0))),
    (145,  Euler((math.radians(-42.0), 0.0, 0.0))), # Spring overshoot open
    (160,  Euler((math.radians(-36.0), 0.0, 0.0))), # Settle open
    (1593, Euler((math.radians(-36.0), 0.0, 0.0))),
    (1650, Euler((math.radians(-4.0),  0.0, 0.0))), # Closing
    (1679, Euler((0.0, 0.0, 0.0))),                 # Snapped shut
]
set_kfs(grp_cap, "rotation_euler", cap_rot_kfs)

# B. Outer Shell Door (Location X: slides left 0 -> -1.65 cm -> 0)
door_loc_kfs = [
    (0,    Vector((0.0, 0.0, 0.0))),
    (160,  Vector((0.0, 0.0, 0.0))),
    (210,  Vector((-1.75, -0.35, 0.0))), # Overshoot slide
    (228,  Vector((-1.65, -0.35, 0.0))), # Settle open
    (1593, Vector((-1.65, -0.35, 0.0))),
    (1650, Vector((-0.15, -0.05, 0.0))),
    (1679, Vector((0.0, 0.0, 0.0))),     # Closed seamless
]
set_kfs(grp_door, "location", door_loc_kfs)

# C. Axial Exploded Lid Collar (Location Z: 0 -> 6.20 cm -> 0)
collar_z_kfs = [
    (0,    Vector((0.0, 0.0, 0.0))),
    (915,  Vector((0.0, 0.0, 0.0))),
    (960,  Vector((0.0, 0.0, 6.40))), # Explode up
    (980,  Vector((0.0, 0.0, 6.20))), # Settle
    (1593, Vector((0.0, 0.0, 6.20))),
    (1650, Vector((0.0, 0.0, 0.50))),
    (1679, Vector((0.0, 0.0, 0.0))),
]
set_kfs(grp_collar, "location", collar_z_kfs)

# Also lift cap assembly root with collar
cap_z_kfs = [
    (0,    Vector((0.0, 3.15, 18.55))),
    (915,  Vector((0.0, 3.15, 18.55))),
    (960,  Vector((0.0, 3.15, 18.55 + 6.40))),
    (980,  Vector((0.0, 3.15, 18.55 + 6.20))),
    (1593, Vector((0.0, 3.15, 18.55 + 6.20))),
    (1650, Vector((0.0, 3.15, 18.55 + 0.50))),
    (1679, Vector((0.0, 3.15, 18.55))),
]
set_kfs(grp_cap, "location", cap_z_kfs)

# D. SSS Silicone Stopper (Location Z: 0 -> 3.65 cm -> 0)
stopper_z_kfs = [
    (0,    Vector((0.0, 0.0, 0.0))),
    (915,  Vector((0.0, 0.0, 0.0))),
    (955,  Vector((0.0, 0.0, 3.80))),
    (975,  Vector((0.0, 0.0, 3.65))),
    (1593, Vector((0.0, 0.0, 3.65))),
    (1650, Vector((0.0, 0.0, 0.30))),
    (1679, Vector((0.0, 0.0, 0.0))),
]
set_kfs(grp_stopper, "location", stopper_z_kfs)

# E. Mouthpiece Spout (Location Z: 0 -> 1.35 cm -> 0)
spout_z_kfs = [
    (0,    Vector((0.0, 0.0, 0.0))),
    (915,  Vector((0.0, 0.0, 0.0))),
    (950,  Vector((0.0, 0.0, 1.45))),
    (970,  Vector((0.0, 0.0, 1.35))),
    (1593, Vector((0.0, 0.0, 1.35))),
    (1650, Vector((0.0, 0.0, 0.15))),
    (1679, Vector((0.0, 0.0, 0.0))),
]
set_kfs(grp_spout, "location", spout_z_kfs)

# F. Subtle Continuous Floating Drift of Termos Root (Zero dead freeze!)
root_rot_kfs = [
    (0,    Euler((0.0, 0.0, math.radians(0.0)))),
    (450,  Euler((0.0, 0.0, math.radians(4.0)))),
    (900,  Euler((0.0, 0.0, math.radians(8.0)))),
    (1350, Euler((0.0, 0.0, math.radians(12.0)))),
    (1679, Euler((0.0, 0.0, math.radians(0.0)))),
]
set_kfs(root, "rotation_euler", root_rot_kfs)


# Save animated master blend file
bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND)
print(f"Master Animated Blend saved: {OUTPUT_BLEND}")


# ------------------------------------------------------------------------------
# 3. EXPORT FRAME-BY-FRAME 3D ANCHOR COORDINATES (JSON)
# ------------------------------------------------------------------------------
from bpy_extras.object_utils import world_to_camera_view

anchor_names = [
    "ANCHOR_HERO_TITLE",
    "ANCHOR_CAP_LID",
    "ANCHOR_SILICONE_STOPPER",
    "ANCHOR_MOUTHPIECE_SPOUT",
    "ANCHOR_OUTER_SHELL_ICEGRAY",
    "ANCHOR_VACUUM_GAP_2MM",
    "ANCHOR_COPPER_GOLD_MIRROR",
    "ANCHOR_INNER_STEEL_SUS304",
    "ANCHOR_HOT_LIQUID_CORE",
]
anchor_objs = {name: bpy.data.objects.get(name) for name in anchor_names if bpy.data.objects.get(name)}

anim_anchors = {}
print("Exporting anchor tracking data across 1680 frames...")
for f in range(0, 1680, 2):  # Every 2 frames for smooth interpolation
    scene.frame_set(f)
    frame_data = {}
    for aname, aobj in anchor_objs.items():
        mat_world = aobj.matrix_world
        co_3d = mat_world.to_translation()
        co_2d = world_to_camera_view(scene, cam, co_3d)
        frame_data[aname] = {
            "x_px": round(co_2d.x * 1080),
            "y_px": round((1.0 - co_2d.y) * 1920),
            "depth": round(co_2d.z, 2),
            "visible": bool(0.0 <= co_2d.x <= 1.0 and 0.0 <= co_2d.y <= 1.0 and co_2d.z > 0)
        }
    anim_anchors[str(f)] = frame_data

with open(ANCHORS_OUTPUT, "w", encoding="utf-8") as f:
    json.dump(anim_anchors, f)
print(f"Tracking anchors exported: {ANCHORS_OUTPUT}")
