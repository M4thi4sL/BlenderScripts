import bpy

# Get the selected objects
selected_objects = bpy.context.selected_objects

# Loop through each selected object
for obj in selected_objects:
    if obj.type == "MESH":
        # Get the modifiers on the object
        modifiers = obj.modifiers

        # Loop through each modifier
        for modifier in modifiers:
            # Apply the modifier
            bpy.context.view_layer.objects.active = obj
            bpy.ops.object.modifier_apply(modifier=modifier.name)
