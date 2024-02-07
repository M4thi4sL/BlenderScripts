import bpy

# Get the selected object
selected_obj = bpy.context.active_object

# Add a Mirror modifier
mirror_modifier = selected_obj.modifiers.new(name="Mirror", type="MIRROR")

# Apply the modifier to see the mirrored result
bpy.ops.object.modifier_apply(modifier=mirror_modifier.name)

# Check existing vertex groups for mirrored naming convention
for vgroup in selected_obj.vertex_groups:
    if vgroup.name.endswith(".l"):
        # Get the mirrored vertex group name
        mirrored_name = vgroup.name[:-2] + ".r"

        # Check if the mirrored vertex group already exists
        if mirrored_name not in [vg.name for vg in selected_obj.vertex_groups]:
            # Duplicate the vertex group and rename it
            selected_obj.vertex_groups.new(name=mirrored_name)
            print(f"Created mirrored vertex group: {mirrored_name}")
    elif vgroup.name.endswith(".r"):
        # Get the mirrored vertex group name
        mirrored_name = vgroup.name[:-2] + ".l"

        # Check if the mirrored vertex group already exists
        if mirrored_name not in [vg.name for vg in selected_obj.vertex_groups]:
            # Duplicate the vertex group and rename it
            selected_obj.vertex_groups.new(name=mirrored_name)
            print(f"Created mirrored vertex group: {mirrored_name}")

print("Mirror modifier and mirrored vertex groups added successfully.")
