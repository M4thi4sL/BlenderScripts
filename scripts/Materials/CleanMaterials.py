import bpy

# define objects
mats = bpy.data.materials
objs = bpy.data.objects


# loop over the objects
for obj in objs:
    # loop over all the slots
    for slot in obj.material_slots:
        # splitt he slotname based on character  '_'
        part = slot.name.rpartition("_")
        if part[2].isnumeric() and part[0] in mats:
            print("splitting")
            slot.material = mats.get(part[0])

# Purge unused materials from blend file
bpy.ops.outliner.orphans_purge()
