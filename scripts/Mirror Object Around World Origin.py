import bpy

# Check if '_origin' empty already exists
origin_empty = bpy.data.objects.get("_origin")
if origin_empty is None:
    # Store the currently selected objects
    selected_objects_before = bpy.context.selected_objects.copy()

    # Create '_origin' empty at world origin
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=(0, 0, 0))
    origin_empty = bpy.context.object
    origin_empty.name = "_origin"

    # Deselect the empty
    origin_empty.select_set(False)

    # Restore the selection
    bpy.context.view_layer.objects.active = selected_objects_before[0]
    for obj in selected_objects_before:
        obj.select_set(True)
else:
    bpy.context.view_layer.objects.active = origin_empty

# Loop over selected objects and add mirror modifier
selected_objects = bpy.context.selected_objects
for obj in selected_objects:
    mirror_modifier = obj.modifiers.new(name="Mirror", type="MIRROR")
    mirror_modifier.use_axis[0] = True  # Enable mirroring on X axis
    mirror_modifier.use_mirror_vertex_groups = True
    mirror_modifier.mirror_object = origin_empty
