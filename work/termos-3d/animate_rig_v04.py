"""
Universal 3D Animation Rig & Dynamic Camera Choreography (v0.4)
================================================================
Implements the 8-Part Cinematic Camera Choreography & Speed Ramping Rubric:
- Shot 01: The Horizon Hook (0.0s - 5.3s, frames 0-159)
- Shot 02: The Whip-Punch (5.3s - 15.2s, frames 160-456)
- Shot 03: The Micro-Dolly (15.2s - 20.4s, frames 457-612)
- Shot 04: The Orbit Slice & Active Radiation Bounce (20.4s - 30.5s, frames 613-915)
- Shot 05: The Dynamic Dutch Action (30.5s - 38.9s, frames 916-1167)
- Shot 06: The Telemetry Anchor Lock (38.9s - 53.1s, frames 1168-1593)
- Shot 07: The Snap-Out Recoil Loop (53.1s - 56.0s, frames 1594-1679)
"""

import bpy
import math
import os
import json
import time
from mathutils import Vector, Euler

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
INPUT_BLEND = os.path.join(ROOT, "outputs", "termos-03-master-semi-realis-v0.3.blend")
OUTPUT_BLEND = os.path.join(ROOT, "outputs", "termos-03-animated-semi-realis-v0.4.blend")
FRAMES_DIR = os.path.join(ROOT, "work", "termos-3d", "anim_frames_v04")
ANCHORS_OUTPUT = os.path.join(ROOT, "outputs", "termos-05-anim-anchors-v0.4.json")

os.makedirs(FRAMES_DIR, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=INPUT_BLEND)
scene = bpy.context.scene

# Scene configuration: 30 fps, 1680 frames (0 to 1679) = 55.967s matching audio master 55.968s
scene.render.fps = 30
scene.frame_start = 0
scene.frame_end = 1679

# Render settings: Blender EEVEE Next with raytracing & fast GI
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

# Render filepath
scene.render.filepath = os.path.join(FRAMES_DIR, "frame_")
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.use_overwrite = True
scene.render.use_placeholder = False

# Fetch objects
cam = bpy.data.objects.get("CAM_SemiReal_Master")
cam_target = bpy.data.objects.get("GEO_Camera_Focus_Target")
root = bpy.data.objects.get("GEO_TERMOS_ROOT")
grp_cap = bpy.data.objects.get("GRP_CAP_ASSEMBLY")
grp_collar = bpy.data.objects.get("GRP_CAP_COLLAR")
grp_stopper = bpy.data.objects.get("GRP_SILICONE_STOPPER_SSS")
grp_spout = bpy.data.objects.get("GRP_MOUTHPIECE_SPOUT")
grp_door = bpy.data.objects.get("GRP_OUTER_SHELL_RIGHT")
grp_arrows = bpy.data.objects.get("GRP_THERMAL_BOUNCE_ARROWS")
mat_arrow = bpy.data.materials.get("MAT_Thermal_Radiation_Arrow")

if not cam_target:
    cam_target = bpy.data.objects.new("GEO_Camera_Focus_Target", None)
    cam_target.empty_display_type = 'SPHERE'
    cam_target.empty_display_size = 0.5
    cam_target.location = (0.0, 0.0, 10.5)
    scene.collection.objects.link(cam_target)

# Ensure Camera Track-To Constraint is always active!
cam.constraints.clear()
tt = cam.constraints.new(type='TRACK_TO')
tt.target = cam_target
tt.track_axis = 'TRACK_NEGATIVE_Z'
tt.up_axis = 'UP_Y'

# Clean existing animation data
for obj in [cam, cam_target, root, grp_cap, grp_collar, grp_stopper, grp_spout, grp_door, grp_arrows]:
    if obj and obj.animation_data:
        obj.animation_data_clear()


def set_kfs(obj, data_path, kfs):
    for f, val in kfs:
        setattr(obj, data_path, val)
        obj.keyframe_insert(data_path=data_path, frame=f)


# ------------------------------------------------------------------------------
# 1. 8-PART CINEMATIC CAMERA CHOREOGRAPHY & SPEED RAMPING
# ------------------------------------------------------------------------------

# Camera Location (X, Y, Z in cm)
# Incorporates Speed Ramping:
# - Shot 1 (0-160): The Horizon Hook. Low angle crane up as lid pops.
# - Shot 2 (160-456): The Whip-Punch! Fast push-in in 0.25s (160->190) + cushion hold on 2mm gap.
# - Shot 3 (457-612): The Micro-Dolly along deep vacuum wall.
# - Shot 4 (613-915): The Orbit Slice (rotates 38 deg around cutaway).
# - Shot 5 (916-1167): The Dynamic Dutch Action (high angle 45 deg macro).
# - Shot 6 (1168-1593): The Telemetry Anchor Lock (stable framing for metric card).
# - Shot 7 (1594-1679): The Snap-Out Recoil (fast pull out, loop back to frame 0).
cam_loc_kfs = [
    # Shot 1: The Horizon Hook
    (0,    Vector((14.0, -52.0, 7.5))),   # Low angle looking up
    (80,   Vector((15.0, -50.0, 11.5))),
    (111,  Vector((15.5, -46.0, 16.5))),  # Crane up to lid mouth
    (159,  Vector((16.0, -48.0, 15.0))),

    # Shot 2: The Whip-Punch (Fast whip 160->195, then cushion hold)
    (160,  Vector((16.0, -48.0, 15.0))),
    (195,  Vector((6.5,  -26.0, 11.2))),  # Aggressive Whip punch-in!
    (230,  Vector((7.0,  -27.5, 11.2))),  # Spring cushion settle
    (340,  Vector((7.5,  -28.5, 11.2))),  # Slow microscopic drift
    (456,  Vector((8.0,  -29.5, 11.2))),

    # Shot 3: The Micro-Dolly (Tracking down the vacuum gap)
    (457,  Vector((8.0,  -29.5, 11.2))),
    (540,  Vector((7.5,  -29.0, 13.8))),  # Track upward along vacuum channel
    (612,  Vector((6.0,  -34.0, 13.0))),

    # Shot 4: The Orbit Slice (Rotates 38 degrees around the cutaway to show depth)
    (613,  Vector((6.0,  -34.0, 13.0))),
    (730,  Vector((-16.0, -38.0, 11.5))), # Sweeping orbit revealing gold layer
    (820,  Vector((-22.0, -36.0, 10.5))), # Rich angle capturing dual rim lights
    (915,  Vector((-18.0, -38.0, 12.0))),

    # Shot 5: The Dynamic Dutch Action (High-angle 45 deg macro looking down at exploded neck)
    (916,  Vector((11.0, -28.0, 26.5))),  # High angle bird's eye macro
    (980,  Vector((12.5, -30.0, 27.5))),  # Settle as collar & stopper explode up
    (1080, Vector((14.0, -32.0, 28.0))),
    (1167, Vector((15.0, -34.0, 26.5))),

    # Shot 6: The Telemetry Anchor Lock (Steady zero-wobble framing for metric proof)
    (1168, Vector((18.0, -64.0, 15.5))),  # Fast snap to steady front-right
    (1296, Vector((18.0, -64.0, 15.5))),  # DEAD STEADY LOCK: Zero wobble
    (1450, Vector((18.0, -64.0, 15.5))),  # Perfectly still for reading
    (1593, Vector((18.0, -64.0, 15.5))),

    # Shot 7: The Snap-Out Recoil Loop (Fast pull out to frame 0 loop)
    (1594, Vector((18.0, -64.0, 15.5))),
    (1640, Vector((15.0, -56.0, 10.5))),
    (1679, Vector((14.0, -52.0, 7.5))),   # EXACT MATCH TO FRAME 0!
]
set_kfs(cam, "location", cam_loc_kfs)

# Camera Focus Target (Coordinates in cm)
target_kfs = [
    (0,    Vector((0.0, 0.0, 9.0))),      # Look at lower body
    (80,   Vector((0.0, 0.0, 12.0))),
    (111,  Vector((0.0, 0.0, 18.0))),     # Focus mouth & lid
    (159,  Vector((0.0, 0.0, 16.0))),

    (160,  Vector((0.0, 0.0, 16.0))),
    (195,  Vector((2.8, 0.0, 11.2))),     # Whip focus to 2mm vacuum gap!
    (230,  Vector((2.8, 0.0, 11.2))),
    (456,  Vector((2.8, 0.0, 11.2))),

    (457,  Vector((2.8, 0.0, 11.2))),
    (540,  Vector((2.8, 0.0, 14.0))),     # Follow vacuum channel up
    (612,  Vector((0.0, 0.0, 12.5))),

    (613,  Vector((0.0, 0.0, 12.5))),
    (730,  Vector((0.8, 0.0, 11.0))),     # Focus on copper/gold mirror
    (820,  Vector((1.2, 0.0, 10.0))),
    (915,  Vector((0.5, 0.0, 12.0))),

    (916,  Vector((0.0, 0.0, 19.5))),     # High angle focus down into neck
    (980,  Vector((0.0, 0.0, 19.5))),
    (1167, Vector((0.0, 0.0, 19.0))),

    (1168, Vector((-1.5, 0.0, 12.5))),    # Telemetry lock: shift target to right
    (1296, Vector((-1.5, 0.0, 12.5))),
    (1450, Vector((-1.5, 0.0, 12.5))),
    (1593, Vector((-1.5, 0.0, 12.5))),

    (1594, Vector((-1.5, 0.0, 12.5))),
    (1679, Vector((0.0, 0.0, 9.0))),      # EXACT MATCH TO FRAME 0!
]
set_kfs(cam_target, "location", target_kfs)

# Camera Focal Length (Zoom & Telephoto Macro)
lens_kfs = [
    (0,    55.0),
    (111,  68.0),
    (159,  55.0),
    (160,  55.0),
    (195,  88.0),   # Macro telephoto on vacuum gap!
    (230,  88.0),
    (456,  88.0),
    (457,  88.0),
    (540,  88.0),
    (612,  65.0),
    (730,  62.0),
    (915,  62.0),
    (916,  75.0),   # Close inspect on silicone stopper
    (1167, 75.0),
    (1168, 62.0),   # Clean wide framing for metric card
    (1593, 62.0),
    (1679, 55.0),   # MATCH FRAME 0!
]
for f, l in lens_kfs:
    cam.data.lens = l
    cam.data.keyframe_insert(data_path="lens", frame=f)


# ------------------------------------------------------------------------------
# 2. ACTIVE MECHANICAL DYNAMICS (THERMAL BOUNCE, EXPANSION, EXPLODED AXIS)
# ------------------------------------------------------------------------------

# A. Active Thermal Radiation Bounce Animation (Frames 613 to 915)
# In accordance with the Universal Systems Dynamics Matrix:
# The thermal bounce arrows MUST NOT remain static!
# They repeatedly expand, hit the copper/gold mirror, and bounce back into the core!
if grp_arrows:
    arrow_scale_kfs = [
        (0,    Vector((0.0, 0.0, 0.0))),
        (612,  Vector((0.0, 0.0, 0.0))),
    ]
    # Energetic oscillation cycle (every 24 frames = ~0.8s per wave)
    for cycle_f in range(613, 915, 24):
        arrow_scale_kfs.append((cycle_f,      Vector((0.35, 0.70, 0.35)))) # Compressed at core
        arrow_scale_kfs.append((cycle_f + 12, Vector((1.15, 1.05, 1.15)))) # Expanding hitting gold wall!
        arrow_scale_kfs.append((cycle_f + 20, Vector((0.85, 0.95, 0.85)))) # Bouncing back!
    arrow_scale_kfs.append((915,  Vector((0.0, 0.0, 0.0))))
    arrow_scale_kfs.append((1679, Vector((0.0, 0.0, 0.0))))
    set_kfs(grp_arrows, "scale", arrow_scale_kfs)

# B. Flip Lid Opening (Rotation X on rear hinge: 0 -> -36 deg -> 0)
cap_rot_kfs = [
    (0,    Euler((0.0, 0.0, 0.0))),
    (111,  Euler((0.0, 0.0, 0.0))),
    (145,  Euler((math.radians(-44.0), 0.0, 0.0))), # Dynamic spring overshoot!
    (160,  Euler((math.radians(-36.0), 0.0, 0.0))), # Settle open
    (1593, Euler((math.radians(-36.0), 0.0, 0.0))),
    (1645, Euler((math.radians(-2.0),  0.0, 0.0))), # Fast snap shut
    (1679, Euler((0.0, 0.0, 0.0))),                 # Snapped shut
]
set_kfs(grp_cap, "rotation_euler", cap_rot_kfs)

# C. Outer Shell Door (Location X: slides left 0 -> -1.70 cm -> 0)
door_loc_kfs = [
    (0,    Vector((0.0, 0.0, 0.0))),
    (160,  Vector((0.0, 0.0, 0.0))),
    (200,  Vector((-1.80, -0.35, 0.0))), # Fast whip overshoot slide!
    (220,  Vector((-1.70, -0.35, 0.0))), # Settle open
    (1593, Vector((-1.70, -0.35, 0.0))),
    (1645, Vector((-0.10, -0.05, 0.0))),
    (1679, Vector((0.0, 0.0, 0.0))),     # Closed seamless
]
set_kfs(grp_door, "location", door_loc_kfs)

# D. Axial Exploded Lid Collar (Location Z: 0 -> 6.20 cm -> 0)
collar_z_kfs = [
    (0,    Vector((0.0, 0.0, 0.0))),
    (915,  Vector((0.0, 0.0, 0.0))),
    (955,  Vector((0.0, 0.0, 6.45))), # Explode up with spring pop
    (975,  Vector((0.0, 0.0, 6.20))), # Settle
    (1593, Vector((0.0, 0.0, 6.20))),
    (1645, Vector((0.0, 0.0, 0.40))),
    (1679, Vector((0.0, 0.0, 0.0))),
]
set_kfs(grp_collar, "location", collar_z_kfs)

cap_z_kfs = [
    (0,    Vector((0.0, 3.15, 18.55))),
    (915,  Vector((0.0, 3.15, 18.55))),
    (955,  Vector((0.0, 3.15, 18.55 + 6.45))),
    (975,  Vector((0.0, 3.15, 18.55 + 6.20))),
    (1593, Vector((0.0, 3.15, 18.55 + 6.20))),
    (1645, Vector((0.0, 3.15, 18.55 + 0.40))),
    (1679, Vector((0.0, 3.15, 18.55))),
]
set_kfs(grp_cap, "location", cap_z_kfs)

# E. SSS Silicone Stopper (Location Z: 0 -> 3.65 cm -> 0)
stopper_z_kfs = [
    (0,    Vector((0.0, 0.0, 0.0))),
    (915,  Vector((0.0, 0.0, 0.0))),
    (950,  Vector((0.0, 0.0, 3.85))),
    (970,  Vector((0.0, 0.0, 3.65))),
    (1593, Vector((0.0, 0.0, 3.65))),
    (1645, Vector((0.0, 0.0, 0.25))),
    (1679, Vector((0.0, 0.0, 0.0))),
]
set_kfs(grp_stopper, "location", stopper_z_kfs)

# F. Mouthpiece Spout (Location Z: 0 -> 1.35 cm -> 0)
spout_z_kfs = [
    (0,    Vector((0.0, 0.0, 0.0))),
    (915,  Vector((0.0, 0.0, 0.0))),
    (945,  Vector((0.0, 0.0, 1.50))),
    (965,  Vector((0.0, 0.0, 1.35))),
    (1593, Vector((0.0, 0.0, 1.35))),
    (1645, Vector((0.0, 0.0, 0.10))),
    (1679, Vector((0.0, 0.0, 0.0))),
]
set_kfs(grp_spout, "location", spout_z_kfs)

# G. Termos Root floating drift (Continuous subtle life)
root_rot_kfs = [
    (0,    Euler((0.0, 0.0, math.radians(0.0)))),
    (450,  Euler((0.0, 0.0, math.radians(3.5)))),
    (900,  Euler((0.0, 0.0, math.radians(7.0)))),
    (1350, Euler((0.0, 0.0, math.radians(10.5)))),
    (1679, Euler((0.0, 0.0, math.radians(0.0)))),
]
set_kfs(root, "rotation_euler", root_rot_kfs)


# ------------------------------------------------------------------------------
# 3. EXPORT FRAME-BY-FRAME 3D TRACKING ANCHORS (v0.4)
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
print("Exporting updated anchor tracking data across 1680 frames (step=2)...")
for f in range(0, 1680, 2):
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

# Save master animated blend
bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND)
print(f"Master Animated Blend v0.4 saved: {OUTPUT_BLEND}")
