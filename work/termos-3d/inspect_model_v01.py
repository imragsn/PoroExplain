import bpy
import json
import os
from mathutils import Vector

ROOT = r"C:\Users\lenovo\Documents\Codex\2026-10-29\gw-mau-reverse-enginering-sebuah-style"
OUT = os.path.join(ROOT, "work", "termos-3d", "model-metrics-v01.json")

excluded = {"validation_floor"}
objects = [o for o in bpy.context.scene.objects if o.type == "MESH" and o.name not in excluded]
corners = []
for obj in objects:
    corners.extend(obj.matrix_world @ Vector(corner) for corner in obj.bound_box)

mins = [min(v[i] for v in corners) for i in range(3)]
maxs = [max(v[i] for v in corners) for i in range(3)]
dims = [maxs[i] - mins[i] for i in range(3)]

payload = {
    "unit": "cm",
    "overall_bounds": {
        "width_x": round(dims[0], 4),
        "depth_y": round(dims[1], 4),
        "height_z": round(dims[2], 4),
        "min": [round(v, 4) for v in mins],
        "max": [round(v, 4) for v in maxs],
    },
    "official_approx_cm": {"width": 6.5, "depth": 7.0, "height": 21.5},
    "mesh_objects": sorted(o.name for o in objects),
}
with open(OUT, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)
print(json.dumps(payload, ensure_ascii=False))
