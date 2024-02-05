import bpy

# Get the selected objects
selected_objects = bpy.context.selected_objects

# Loop through each selected object
for obj in selected_objects:
    # Check if the object has an Armature or rig modifier
    if obj.type == "MESH":
        armature_modifier = None

        # Iterate through the object's modifiers
        for modifier in obj.modifiers:
            if modifier.type == "ARMATURE":
                armature_modifier = modifier

        # Toggle the display in viewport for Armature modifier
        if armature_modifier:
            armature_modifier.show_viewport = not armature_modifier.show_viewport
