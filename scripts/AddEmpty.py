import bpy
import bmesh
from mathutils import Matrix

# Get the active mesh object
obj = bpy.context.active_object

# Ensure we're in object mode
bpy.ops.object.mode_set(mode='OBJECT')

# Get the selected faces from the mesh data
mesh = obj.data
bm = bmesh.new()
bm.from_mesh(mesh)

# Loop over all selected faces
for face in bm.faces:
    if face.select:
        # Calculate the center of the face in local space
        center = face.calc_center_median()
        normal = face.normal
        
        # Create a new empty at the center of the face
        empty = bpy.data.objects.new("Arrow", None)
        empty.empty_display_type = 'ARROWS'
        bpy.context.collection.objects.link(empty)
        
        # Set the empty location in world coordinates
        empty.location = obj.matrix_world @ center
        
        # Align the empty with the face normal, considering the object's transformations
        # Calculate the correct rotation for the empty using the face normal in world coordinates
        up = (obj.matrix_world.to_3x3() @ normal).normalized()
        empty.rotation_mode = 'QUATERNION'
        empty.rotation_quaternion = up.to_track_quat('Z', 'Y')
        
        # Parent the empty to the original object
        empty.parent = obj
        
        # Apply inverse parent transform to counter the object's transformations
        empty.matrix_parent_inverse = obj.matrix_world.inverted()

# Clean up
bm.free()

# Update the viewport
bpy.context.view_layer.update()
