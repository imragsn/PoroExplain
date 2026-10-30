
import bpy
import time

# Create simple scene with lathe mesh
bpy.ops.mesh.primitive_cylinder_add()
scene = bpy.context.scene
scene.render.engine = 'BLENDER_EEVEE'
scene.render.resolution_x = 540
scene.render.resolution_y = 960
scene.render.resolution_percentage = 100
scene.render.use_freestyle = True
scene.frame_start = 1
scene.frame_end = 5
scene.render.filepath = 'work/termos-3d/test_frame_'

t0 = time.time()
bpy.ops.render.render(animation=True)
print(f'Rendered 5 frames in {time.time()-t0:.2f}s')
