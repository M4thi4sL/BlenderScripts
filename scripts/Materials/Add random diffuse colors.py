import bpy
import random
from bpy.types import Operator


class OBJECT_OT_random_diffuse_colors(Operator):
    bl_idname = "object.random_diffuse_colors"
    bl_label = "Random Diffuse Colors"
    bl_options = {"REGISTER", "UNDO"}

    use_nodes: bpy.props.BoolProperty(
        name="Use Nodes",
        default=True,
        description="Enable 'Use Nodes' for the material",
    )
    create_new_material_slot: bpy.props.BoolProperty(
        name="Create New Material Slot",
        default=False,
        description="Create a new material slot for each object",
    )
    replace_first_material: bpy.props.BoolProperty(
        name="Replace First Material",
        default=False,
        description="Replace the first material in the object",
    )

    def execute(self, context):
        for ob in bpy.context.selected_objects:
            bpy.context.view_layer.objects.active = ob
            mat_len = len(ob.data.materials)

            r, g, b = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
            )
            hex_name = "#{0:02x}{1:02x}{2:02x}".format(r, g, b)

            if (
                mat_len
                and self.replace_first_material
                and not self.create_new_material_slot
            ):
                ob.active_material_index = 0
                mat = ob.active_material
                mat.name = hex_name
            else:
                mat = bpy.data.materials.new(name=hex_name)

            mat.diffuse_color = (r / 255, g / 255, b / 255, 1.0)

            if mat_len and not self.create_new_material_slot:
                ob.active_material_index = 0
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.object.material_slot_assign()
                bpy.ops.object.mode_set(mode="OBJECT")
                ob.data.materials[0] = mat
            else:
                ob.data.materials.append(mat)
                ob.active_material_index = mat_len
                bpy.ops.object.mode_set(mode="EDIT")
                bpy.ops.object.material_slot_assign()
                bpy.ops.object.mode_set(mode="OBJECT")

            mat.use_nodes = self.use_nodes

            if self.use_nodes:
                # Clear existing nodes
                for node in mat.node_tree.nodes:
                    mat.node_tree.nodes.remove(node)

                # Create Principled BSDF shader node
                principled_bsdf = mat.node_tree.nodes.new(
                    type="ShaderNodeBsdfPrincipled"
                )

                # Set the base color
                principled_bsdf.inputs["Base Color"].default_value = (
                    r / 255,
                    g / 255,
                    b / 255,
                    1.0,
                )

                # Create Material Output node
                material_output = mat.node_tree.nodes.new(
                    type="ShaderNodeOutputMaterial"
                )

                # Connect Principled BSDF to Material Output
                mat.node_tree.links.new(
                    principled_bsdf.outputs["BSDF"], material_output.inputs["Surface"]
                )
            else:
                # Set diffuse color for non-node setup
                mat.diffuse_color = (r / 255, g / 255, b / 255, 1.0)

        return {"FINISHED"}


def register():
    bpy.utils.register_class(OBJECT_OT_random_diffuse_colors)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_random_diffuse_colors)


register()
# test call
bpy.ops.object.random_diffuse_colors("INVOKE_DEFAULT")
