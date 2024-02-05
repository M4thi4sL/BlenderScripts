import bpy

# Loop through all selected objects
for obj in bpy.context.selected_objects:
    # Make sure the object has a valid data block
    if obj.type == "MESH" and obj.data:
        # Clear all materials from the object
        obj.data.materials.clear()
