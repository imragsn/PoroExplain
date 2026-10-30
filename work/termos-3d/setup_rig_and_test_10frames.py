import bpy
import math
import os
import json
import time
from mathutils import Vector, Euler

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
BLEND_PATH = os.path.join(ROOT, "outputs", "termos-03-master-semi-realis-v0.3.blend")
TEST_DIR = os.path.join(ROOT, "work", "termos-3d", "test_anim_frames")
os.makedirs(TEST_DIR, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=BLEND_PATH)
scene = bpy.context.scene

# Configure EEVEE Next for smooth, fast, beautiful 3D animation
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100
scene.render.fps = 30
scene.frame_start = 0
scene.frame_end = 1679

scene.eevee.use_raytracing = True
scene.eevee.use_fast_gi = True
scene.eevee.taa_render_samples = 4
scene.eevee.use_shadows = True

scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure = 0.05

# Tune lights for vibrant semi-realistic studio look in EEVEE
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

scene.world.node_tree.nodes.get("Background").inputs["Strength"].default_value = 0.80

cam = bpy.data.objects.get("CAM_SemiReal_Master")
root = bpy.data.objects.get("GEO_TERMOS_ROOT")
grp_cap = bpy.data.objects.get("GRP_CAP_ASSEMBLY")
grp_collar = bpy.data.objects.get("GRP_CAP_COLLAR")
grp_stopper = bpy.data.objects.get("GRP_SILICONE_STOPPER_SSS")
grp_spout = bpy.data.objects.get("GRP_MOUTHPIECE_SPOUT")
grp_gasket = bpy.data.objects.get("GRP_SILICONE_GASKET")
grp_door = bpy.data.objects.get("GRP_OUTER_SHELL_RIGHT")
grp_arrows = bpy.data.objects.get("GRP_THERMAL_BOUNCE_ARROWS")
grp_particles = bpy.data.objects.get("GRP_VACUUM_PARTICLES")

print("All objects found:", [o.name for o in (cam, root, grp_cap, grp_collar, grp_stopper, grp_spout, grp_door)])

# Test render 5 frames (Frame 0, 100, 200, 300, 400)
t0 = time.time()
for f in [0, 100, 200, 300, 400]:
    scene.frame_set(f)
    scene.render.filepath = os.path.join(TEST_DIR, f"test_frame_{f:04d}.png")
    t_f = time.time()
    bpy.ops.render.render(write_still=True)
    print(f"Rendered Frame {f} in {time.time() - t_f:.2f}s")
total_time = time.time() - t0
print(f"5 frames rendered in {total_time:.2f}s (Average: {total_time/5:.2f}s per frame)")
