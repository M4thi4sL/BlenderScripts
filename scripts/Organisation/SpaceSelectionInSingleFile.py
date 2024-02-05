import bpy

# Get the selected objects
selected_objects = bpy.context.selected_objects

# Get the first object as the reference point
reference_object = selected_objects[0]

# Get the bounding box dimensions of the reference object
reference_bbox = reference_object.bound_box

# Get the max and min coordinates of the bounding box
x_min, y_min, z_min = reference_bbox[0]
x_max, y_max, z_max = reference_bbox[6]

# Get the distance between the min and max coordinates
distance = abs(x_max - x_min)

# Additional space to add between objects
additional_space = 0.5

# Loop through the remaining selected objects
for obj in selected_objects[1:]:
    # Move the object along the X axis
    obj.location.x += distance + additional_space
    # Update the distance for the next object
    distance += abs(x_max - x_min) + additional_space

