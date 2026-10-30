import bpy
import os

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
OUTPUT_BLEND = os.path.join(ROOT, "outputs", "termos-03-animated-semi-realis-v0.3.blend")
FRAMES_DIR = os.path.join(ROOT, "work", "termos-3d", "anim_frames")
os.makedirs(FRAMES_DIR, exist_ok=True)

bpy.ops.wm.open_mainfile(filepath=OUTPUT_BLEND)
scene = bpy.context.scene

scene.render.filepath = os.path.join(FRAMES_DIR, "frame_")
scene.render.image_settings.file_format = 'PNG'
scene.render.image_settings.color_mode = 'RGBA'
scene.render.use_overwrite = True
scene.render.use_placeholder = False

bpy.ops.wm.save_as_mainfile(filepath=OUTPUT_BLEND)
print("Updated render filepath to:", scene.render.filepath)
