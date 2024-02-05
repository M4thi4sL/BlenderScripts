import bpy
from bpy.props import FloatProperty, EnumProperty

# Define the ObjectSpacingOperator class
class ObjectSpacingOperator(bpy.types.Operator):
    bl_idname = "object.spacing_operator"
    bl_label = "Object spacing in a row"
    bl_description = "space the selected objects into a user-selected row "

    # Define the additional_space property
    additional_space: FloatProperty(
        name="Additional Space",
        description="Extra distance between objects (in meters)",
        default=200.0,
        min=0.0,
        unit='LENGTH'
    )

    # Define the axis property
    axis: EnumProperty(
        name="Axis",
        description="Axis along which objects are spaced",
        items=[
            ("X", "X", "X Axis"),
            ("Y", "Y", "Y Axis"),
            ("Z", "Z", "Z Axis")
        ],
        default="X"
    )

    def execute(self, context):
        # Get the selected objects
        selected_objects = bpy.context.selected_objects
        
        # Check if there are no selected objects
        if len(selected_objects) < 1:
            self.report({'WARNING'}, "No objects selected. Operator canceled.")
            return {'CANCELLED'}

        # Get the scene unit scale
        unit_scale = bpy.context.scene.unit_settings.scale_length

        # Convert additional_space to the scene unit
        additional_space_scaled = self.additional_space# * unit_scale

        # Get the axis index
        axis_index = {"X": 0, "Y": 1, "Z": 2}[self.axis]

        # Get the first object as the reference point
        reference_object = selected_objects[0]

        # Get the bounding box dimensions of the reference object
        reference_bbox = reference_object.bound_box

        # Get the max and min coordinates of the bounding box along the selected axis
        x_min, y_min, z_min = reference_bbox[0]
        x_max, y_max, z_max = reference_bbox[6]
        reference_min = (x_min, y_min, z_min)[axis_index]
        reference_max = (x_max, y_max, z_max)[axis_index]

        # Get the distance between the min and max coordinates along the selected axis
        distance = abs(reference_max - reference_min)

        # Loop through the remaining selected objects
        for obj in selected_objects[1:]:
            # Move the object along the selected axis
            obj.location[axis_index] += distance + additional_space_scaled
            # Update the distance for the next object
            distance += abs(reference_max - reference_min) + additional_space_scaled

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

# Register the operator
bpy.utils.register_class(ObjectSpacingOperator)

# Unregister the operator
def unregister():
    bpy.utils.unregister_class(ObjectSpacingOperator)

# test call
bpy.ops.object.spacing_operator('INVOKE_DEFAULT')