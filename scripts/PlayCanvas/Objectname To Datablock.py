import bpy

# Get the selected objects
selected_objects = bpy.context.selected_objects

# Loop through each selected object and set datablock mesh name to object name
for obj in selected_objects:
    if obj.type == 'MESH' and obj.data:
        obj.data.name = obj.name
