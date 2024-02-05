import bpy


class OBJECT_OT_SelectByMaterialName(bpy.types.Operator):
    bl_idname = "object.select_by_material_name"
    bl_label = "Select Objects by Material Name"
    bl_options = {"REGISTER", "UNDO"}

    material_name: bpy.props.StringProperty(
        name="Material Name",
        default="",
        description="Enter the material name you want to select",
    )

    def execute(self, context):
        # Deselect all objects
        bpy.ops.object.select_all(action="DESELECT")

        # Iterate through all objects in the scene
        for obj in bpy.context.scene.objects:
            # Check if the object is a mesh
            if obj.type == "MESH":
                # Iterate through all the materials assigned to the mesh
                for material_slot in obj.material_slots:
                    # Check if the material name matches the one we are looking for
                    if material_slot.material.name == self.material_name:
                        # Select the object
                        obj.select_set(True)
                        break

        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(OBJECT_OT_SelectByMaterialName)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_SelectByMaterialName)


register()
bpy.ops.object.select_by_material_name("INVOKE_DEFAULT")
