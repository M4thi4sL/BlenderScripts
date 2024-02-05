import bpy
from bpy.props import StringProperty


class OBJECT_OT_RemoveUnwantedVertexGroups(bpy.types.Operator):
    bl_idname = "object.remove_unwanted_vertexgroups"
    bl_label = "Keep Selected Vertex Groups"
    bl_options = {"REGISTER", "UNDO"}

    keep_vertex_groups: bpy.props.StringProperty(
        name="Keep Vertex Groups",
        description="Enter the names of vertex groups to keep, separated by ||",
        default="head.x || hair_scale",
    )

    def execute(self, context):
        # Get the selected objects
        selected_objects = bpy.context.selected_objects

        # Split the input string into a list of vertex group names
        keep_list = [name.strip() for name in self.keep_vertex_groups.split("||")]

        # Iterate over each selected object
        for obj in selected_objects:
            if obj.type == "MESH":
                # Remove vertex groups that are not in the keep_vertex_groups list
                for vertex_group in obj.vertex_groups[:]:
                    if vertex_group.name not in keep_list:
                        obj.vertex_groups.remove(vertex_group)

        return {"FINISHED"}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


def register():
    bpy.utils.register_class(OBJECT_OT_RemoveUnwantedVertexGroups)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_RemoveUnwantedVertexGroups)


register()
bpy.ops.object.remove_unwanted_vertexgroups("INVOKE_DEFAULT")
