import bpy

# only search on own object materials
mat_list = [x.material.name for x in bpy.context.object.material_slots]
remove_slots = []


# the following only works in object mode
bpy.ops.object.mode_set(mode="OBJECT")

for s in bpy.context.object.material_slots:
    if s.material.name[-3:].isnumeric():
        # the last 3 characters are numbers
        # that indicates it might be a duplicate of another material
        # but this is pure guesswork, so expect errors to happen!
        if s.material.name[:-4] in mat_list:

            # there is a material without the numeric extension so use it
            # this again is just guessing that we're having identical node trees here

            # get the material index of the 'clean' material
            index_clean = mat_list.index(s.material.name[:-4])
            index_wrong = mat_list.index(s.material.name)
            print(index_wrong, index_clean)

            # get the faces which are assigned to the 'wrong' material
            faces = [
                x
                for x in bpy.context.object.data.polygons
                if x.material_index == index_wrong
            ]

            for f in faces:
                f.material_index = index_clean

            remove_slots.append(s.name)

# now remove all empty material slots:
for s in remove_slots:

    if s in [x.name for x in bpy.context.object.material_slots]:
        print("removing slot %s" % s)
        bpy.context.object.active_material_index = [
            x.material.name for x in bpy.context.object.material_slots
        ].index(s)
        bpy.ops.object.material_slot_remove()
