import bpy
import random
from bpy.types import Operator
from bpy.props import BoolProperty, IntProperty

from enum import Enum, auto
from math import sqrt

# Global variable
global SCENE_SCALE


class PRIMITIVES(Enum):
    CUBE = auto()
    UV_SPHERE = auto()
    CYLINDER = auto()
    CONE = auto()
    ICO_SPHERE = auto()
    TORUS = auto()
    MONKEY = auto()


class OBJECT_OT_CreateTestScene(Operator):
    bl_idname = "object.create_test_scene"
    bl_label = "Create Test Scene"
    bl_options = {"REGISTER", "UNDO"}

    use_random_rotation: BoolProperty(
        name="Random Rotation",
        default=True,
        description="Add random rotation to each object",
    )

    use_random_height: BoolProperty(
        name="Random Height Offset",
        default=True,
        description="Add random height offset to each object",
    )
    num_objects: IntProperty(
        name="Object Count",
        default=20,
        min=1,
        description="Number of items.",
    )

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        layout.prop(self, "num_objects")
        layout.prop(self, "use_random_rotation")
        layout.prop(self, "use_random_height")

    def execute(self, context):
        # Clear existing mesh objects
        bpy.ops.object.select_all(action="DESELECT")
        bpy.ops.object.select_by_type(type="MESH")
        bpy.ops.object.delete()

        # Calculate rows and items per row
        num_rows = int(sqrt(self.num_objects))
        items_per_row = num_rows if num_rows > 0 else 1

        # Create objects with random primitives, random rotation, and random height offset
        for i in range(self.num_objects):
            row_index = i // items_per_row
            col_index = i % items_per_row
            x_offset = col_index * 4 * SCENE_SCALE
            y_offset = row_index * 4 * SCENE_SCALE
            location = (x_offset, y_offset, 0)

            # Random rotation
            if self.use_random_rotation:
                rotation = (
                    random.uniform(0, 2 * 3.14159),
                    random.uniform(0, 2 * 3.14159),
                    random.uniform(0, 2 * 3.14159),
                )
            else:
                rotation = (0, 0, 0)

            # Randomly select a primitive
            primitive = random.choice(list(PRIMITIVES))

            if primitive == PRIMITIVES.CUBE:
                bpy.ops.mesh.primitive_cube_add(
                    size=2 * SCENE_SCALE, location=location, rotation=rotation
                )
            elif primitive == PRIMITIVES.UV_SPHERE:
                bpy.ops.mesh.primitive_uv_sphere_add(
                    radius=1 * SCENE_SCALE, location=location, rotation=rotation
                )
            elif primitive == PRIMITIVES.CYLINDER:
                bpy.ops.mesh.primitive_cylinder_add(
                    radius=1 * SCENE_SCALE,
                    depth=2 * SCENE_SCALE,
                    location=location,
                    rotation=rotation,
                )
            elif primitive == PRIMITIVES.CONE:
                bpy.ops.mesh.primitive_cone_add(
                    vertices=8,
                    radius1=1 * SCENE_SCALE,
                    depth=2 * SCENE_SCALE,
                    location=location,
                    rotation=rotation,
                )
            elif primitive == PRIMITIVES.ICO_SPHERE:
                bpy.ops.mesh.primitive_ico_sphere_add(
                    radius=1 * SCENE_SCALE, location=location, rotation=rotation
                )
            elif primitive == PRIMITIVES.TORUS:
                bpy.ops.mesh.primitive_torus_add(
                    major_radius=1 * SCENE_SCALE,
                    minor_radius=0.5 * SCENE_SCALE,
                    location=location,
                    rotation=rotation,
                )
            elif primitive == PRIMITIVES.MONKEY:
                bpy.ops.mesh.primitive_monkey_add(
                    size=2 * SCENE_SCALE, location=location, rotation=rotation
                )

            # Random height offset
            if self.use_random_height:
                bpy.context.active_object.location.z += random.uniform(
                    0, 2 * SCENE_SCALE
                )

        return {"FINISHED"}

    def get_SCENE_SCALE_factor(self):
        scale_length = bpy.context.scene.unit_settings.scale_length
        if scale_length == 1.0:
            return 1.0
        else:
            return 100.0


def register():
    bpy.utils.register_class(OBJECT_OT_CreateTestScene)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_CreateTestScene)


register()
bpy.ops.object.create_test_scene("INVOKE_DEFAULT")
