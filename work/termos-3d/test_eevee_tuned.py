import bpy
import time
import os

BLEND = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style\outputs\termos-03-master-semi-realis-v0.3.blend"
OUT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style\work\test_eevee_tuned.png"

bpy.ops.wm.open_mainfile(filepath=BLEND)
scene = bpy.context.scene

scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 1080
scene.render.resolution_y = 1920
scene.render.resolution_percentage = 100

# EEVEE Next Raytracing & Shadow Settings
scene.eevee.use_raytracing = True
scene.eevee.use_fast_gi = True
scene.eevee.taa_render_samples = 4
scene.eevee.gi_diffuse_bounces = 3
scene.eevee.use_shadows = True

# Tone down exposure for EEVEE (since EEVEE direct lighting has no inverse-square falloff attenuation like Cycles bounces)
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.view_settings.exposure = -0.85

# Scale light energies for EEVEE
for light in bpy.data.lights:
    if "Backdrop" in light.name:
        light.energy = 650.0
    elif "Rim" in light.name:
        light.energy = 950.0
    elif "Key" in light.name:
        light.energy = 850.0
    elif "Fill" in light.name:
        light.energy = 450.0
    elif "Top" in light.name:
        light.energy = 550.0

scene.world.node_tree.nodes.get("Background").inputs["Strength"].default_value = 0.45

scene.render.filepath = OUT
t0 = time.time()
bpy.ops.render.render(write_still=True)
print("EEVEE TUNED RENDER TIME:", time.time() - t0)
