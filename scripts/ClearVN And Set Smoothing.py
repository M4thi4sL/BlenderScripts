import bpy
import math

# Get the selected objects
selected_objects = bpy.context.selected_objects

# Loop through each selected object
for obj in selected_objects:
    # Check if the object has a mesh
    if obj.type == "MESH":
        # Set the object as the active object
        bpy.context.view_layer.objects.active = obj

        # Select the object and enter edit mode
        obj.select_set(True)
        bpy.ops.object.mode_set(mode="EDIT")

        # Clear custom split normals data
        bpy.ops.mesh.customdata_custom_splitnormals_clear()

        # Enable autosmooth and set the smoothing angle to 0.733038 radians
        bpy.context.object.data.use_auto_smooth = True
        bpy.context.object.data.auto_smooth_angle = math.radians(42)

        # Exit edit mode and deselect the object
        bpy.ops.object.mode_set(mode="OBJECT")
        obj.select_set(False)
