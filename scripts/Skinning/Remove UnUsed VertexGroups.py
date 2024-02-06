import bpy

ob = bpy.context.object
ob.update_from_editmode()

vgroup_used = {i: False for i, k in enumerate(ob.vertex_groups)}

for v in ob.data.vertices:
    for g in v.groups:
        if g.weight > 0.0:
            vgroup_used[g.group] = True

# Check mirrored vertex groups
for modifier in ob.modifiers:
    if modifier.type == "MIRROR":
        mirror_object = modifier.mirror_object
        if mirror_object:
            for vgroup in ob.vertex_groups:
                if vgroup.name.endswith(".L") or vgroup.name.endswith(".R"):
                    counterpart_name = vgroup.name[:-2] + (
                        ".R" if vgroup.name.endswith(".L") else ".L"
                    )
                    counterpart_index = ob.vertex_groups.find(counterpart_name)
                    if counterpart_index != -1:
                        vgroup_used[vgroup.index] = (
                            vgroup_used[vgroup.index] or vgroup_used[counterpart_index]
                        )

for i, used in sorted(vgroup_used.items(), reverse=True):
    if not used:
        print(f"Vertex Group '{ob.vertex_groups[i].name}' is unused.")
        ob.vertex_groups.remove(ob.vertex_groups[i])
    else:
        print(f"Vertex Group '{ob.vertex_groups[i].name}' is used.")
