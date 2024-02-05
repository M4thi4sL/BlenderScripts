import bpy
import math
from bpy.props import FloatProperty, BoolProperty
from bpy.types import Operator


class ArrangeObjectsOperator(Operator):
    bl_idname = "object.arrange_objects"
    bl_label = "Arrange Objects"
    
    additional_space: FloatProperty(
        name="Additional Space",
        description="Additional space between objects",
        default=100.0,
        min=0.0,
        unit='LENGTH'
    )
    
    clear_rotation: BoolProperty(
        name="Clear Rotation",
        description="Clear rotation information of the objects",
        default=False
    )
    
    @classmethod
    def poll(cls, context):
        return True
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        
        layout.prop(self, "additional_space")
        layout.prop(self, "clear_rotation")
    
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        # Get the selected objects
        selected_objects = context.selected_objects
    
        # Check if there are no selected objects
        if len(selected_objects) < 1:
            self.report({'WARNING'}, "No objects selected. Operator canceled.")
            return {'CANCELLED'}
    
        # Get the first object as the reference point
        reference_object = selected_objects[0]
    
        # Get the bounding box dimensions of the reference object
        reference_bbox = reference_object.bound_box
    
        # Get the max and min coordinates of the bounding box
        x_min, y_min, z_min = reference_bbox[0]
        x_max, y_max, z_max = reference_bbox[6]
    
        # Get the distance between the min and max coordinates
        distance = abs(x_max - x_min)
    
        # Number of objects in a row
        num_obj_in_row = math.ceil(math.sqrt(len(selected_objects)))
    
        # Initial position
        start_pos = [0, 0, 0]
    
        # Loop through the remaining selected objects
        for i, obj in enumerate(selected_objects):
            # Clear the location
            obj.location = (0, 0, 0)
    
            # Clear the rotation if specified
            if self.clear_rotation:
                obj.rotation_euler = (0, 0, 0)
    
            # Move the object along the X axis
            obj.location.x = start_pos[0] + (distance + self.additional_space) * (i % num_obj_in_row)
            obj.location.y = start_pos[1] + (distance + self.additional_space) * (i // num_obj_in_row)
    
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ArrangeObjectsOperator)


def unregister():
    bpy.utils.unregister_class(ArrangeObjectsOperator)



register()

# Prompt the user with the operator
bpy.ops.object.arrange_objects('INVOKE_DEFAULT')
