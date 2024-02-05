import bpy

# Clear the current selection
bpy.ops.object.select_all(action='DESELECT')

# Iterate through all objects in the scene
for obj in bpy.data.objects:
    # Check if the object is a mesh and its name contains 'UBX' or 'UCX'
    if obj.type == 'MESH' and ('UBX' in obj.name or 'UCX' in obj.name):
        # Select the object
        obj.select_set(True)

# Update the viewport to reflect the selection
bpy.context.view_layer.objects.active = bpy.context.selected_objects[-1]
