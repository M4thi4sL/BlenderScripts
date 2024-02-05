import bpy

mats = bpy.data.materials
objs = bpy.data.objects

for obj in objs:
    for slt in obj.material_slots:
        part = slt.name.rpartition(".")
        if part[2].isnumeric() and part[0] in mats:
            slt.material = mats.get(part[0])

for obj in objs:
    for slt in obj.material_slots:
        if slt.name == "Material":
            print("Purging:" + str(obj) + " from scene")
            bpy.data.objects.remove(obj, do_unlink=True)

bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
