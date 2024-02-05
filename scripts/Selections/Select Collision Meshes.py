import bpy


class OBJECT_OT_SelectCollisionMeshes(bpy.types.Operator):
    bl_idname = "object.select_collision_meshes"
    bl_label = "Select Collision Meshes"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        # Clear the current selection
        bpy.ops.object.select_all(action="DESELECT")

        # List to keep track of found collision meshes
        collision_meshes = []

        # Iterate through all objects in the scene
        for obj in bpy.data.objects:
            # Check if the object is a mesh and its name contains 'UBX' or 'UCX'
            if obj.type == "MESH" and ("UBX" in obj.name or "UCX" in obj.name):
                # Select the object
                obj.select_set(True)
                collision_meshes.append(obj.name)

        # Update the viewport to reflect the selection
        if bpy.context.selected_objects:
            bpy.context.view_layer.objects.active = bpy.context.selected_objects[-1]
        else:
            # If no collision meshes are found, report a message
            self.report({"INFO"}, "No collision meshes found in the scene.")
            return {"CANCELLED"}

        return {"FINISHED"}


# Register the operator
def register():
    bpy.utils.register_class(OBJECT_OT_SelectCollisionMeshes)


# Unregister the operator
def unregister():
    bpy.utils.unregister_class(OBJECT_OT_SelectCollisionMeshes)


# Run the script
register()
bpy.ops.object.select_collision_meshes()
