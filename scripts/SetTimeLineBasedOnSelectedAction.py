import bpy

# Get the selected action
selected_action = bpy.context.object.animation_data.action

# Convert the frame range to integers
start_frame = round(selected_action.frame_range[0])
end_frame = round(selected_action.frame_range[1])

# Set the timeline range
bpy.context.scene.frame_start = start_frame
bpy.context.scene.frame_end = end_frame
