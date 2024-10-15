import bpy

def step_0_check_and_add_def_prefix():
    """Step 0: Check if bones have the 'DEF_' prefix, and if not, add it."""
    armature = bpy.context.active_object

    # Loop over all bones and check if the name starts with 'DEF_'
    for bone in armature.data.edit_bones:
        if not bone.name.startswith("DEF_"):
            # If the name doesn't start with 'DEF_', add the prefix
            bone.name = "DEF_" + bone.name
            print(f"Renamed bone to '{bone.name}' (added 'DEF_' prefix).")
        else:
            print(f"'{bone.name}' already has 'DEF_' prefix.")


def step_1_duplicate_bones():
    """Step 1: Duplicate the selected bones and replace 'DEF_' with 'CTRL_'."""
    if bpy.context.active_object and bpy.context.active_object.type == 'ARMATURE' and bpy.context.mode == 'EDIT_ARMATURE':
        armature = bpy.context.active_object

        # Store selected bones in edit mode
        selected_bones = [bone.name for bone in bpy.context.selected_editable_bones]

        # Check if any bones are selected
        if not selected_bones:
            print("No bones selected.")
            return

        print(f"Step 1: Selected bones: {selected_bones}")

        # Dictionary to store original bone -> CTRL bone mappings
        ctrl_bone_map = {}

        # Duplicate bones
        for bone_name in selected_bones:
            try:
                bone = armature.data.edit_bones[bone_name]

                # Replace 'DEF_' with 'CTRL_' in the name for the duplicate
                new_bone_name = bone_name.replace("DEF_", "CTRL_")

                # Duplicate the bone with the new name
                new_bone = armature.data.edit_bones.new(new_bone_name)
                new_bone.head = bone.head.copy()
                new_bone.tail = bone.tail.copy()
                new_bone.roll = bone.roll
                new_bone.use_connect = bone.use_connect
                new_bone.parent = bone.parent  # Maintain hierarchy

                # Store in map to maintain parent-child relationships later
                ctrl_bone_map[bone_name] = new_bone

                print(f"Duplicated bone '{bone_name}' to '{new_bone.name}'")

            except Exception as e:
                print(f"Error duplicating bone {bone_name}: {e}")

        # Maintain hierarchy of duplicated bones
        for bone_name, ctrl_bone in ctrl_bone_map.items():
            original_bone = armature.data.edit_bones[bone_name]
            if original_bone.parent:
                parent_name = original_bone.parent.name
                if parent_name in ctrl_bone_map:
                    ctrl_bone.parent = ctrl_bone_map[parent_name]
                    print(f"Parented '{ctrl_bone.name}' to '{ctrl_bone_map[parent_name].name}'")

    else:
        print("Please select an armature and make sure you are in Edit Mode.")


def step_2_add_ctrl_prefix():
    """Add 'CTRL_' prefix to the duplicated bones."""
    if bpy.context.active_object and bpy.context.active_object.type == 'ARMATURE' and bpy.context.mode == 'EDIT_ARMATURE':
        armature = bpy.context.active_object

        # Find duplicated bones and rename them
        for bone in armature.data.edit_bones:
            if bone.name.endswith("_DUPLICATE"):
                bone.name = "CTRL_" + bone.name.replace("_DUPLICATE", "")
                print(f"Renamed duplicate bone to '{bone.name}'")
    else:
        print("Please select an armature and make sure you are in Edit Mode.")


def step_3_switch_to_pose_mode():
    """Switch from Edit Mode to Pose Mode."""
    if bpy.context.active_object and bpy.context.active_object.type == 'ARMATURE' and bpy.context.mode == 'EDIT_ARMATURE':
        bpy.ops.object.mode_set(mode='POSE')
        print("Switched to Pose Mode.")
    else:
        print("Please select an armature and make sure you are in Edit Mode.")


def step_4_add_copy_transforms_constraint():
    """Step 4: Add 'Copy Transforms' constraint to original bones to follow their corresponding 'CTRL_' bones."""
    if bpy.context.active_object and bpy.context.active_object.type == 'ARMATURE' and bpy.context.mode == 'POSE':
        armature = bpy.context.active_object

        for pose_bone in armature.pose.bones:
            bone_name = pose_bone.name

            # Check if the bone is a 'DEF_' bone
            if bone_name.startswith("DEF_"):
                # Find the corresponding 'CTRL_' bone name by replacing 'DEF_' with 'CTRL_'
                ctrl_bone_name = bone_name.replace("DEF_", "CTRL_")

                # Check if the corresponding 'CTRL_' bone exists in pose bones
                if ctrl_bone_name in armature.pose.bones:
                    # Add a 'Copy Transforms' constraint
                    constraint = pose_bone.constraints.new('COPY_TRANSFORMS')
                    constraint.target = armature
                    constraint.subtarget = ctrl_bone_name
                    print(f"Added 'Copy Transforms' constraint on '{bone_name}', targeting '{ctrl_bone_name}'")

                else:
                    print(f"CTRL bone '{ctrl_bone_name}' not found for '{bone_name}'")
    else:
        print("Please select an armature and make sure you are in Pose Mode.")


def step_5_create_bone_collections_and_assign_colors():
    """Create bone collections 'DEF' and 'CTRL', assign bones, and set bone color themes based on naming conventions."""
    armature = bpy.context.active_object

    # Access the collections from the armature's data
    bone_collections = armature.data.collections

    # Create DEF bone collection for the original bones
    if "DEF" not in bone_collections:
        def_collection = bone_collections.new(name="DEF")
        print("Created 'DEF' bone collection.")
    else:
        def_collection = bone_collections["DEF"]

    # Create CTRL bone collection for the CTRL bones
    if "CTRL" not in bone_collections:
        ctrl_collection = bone_collections.new(name="CTRL")
        print("Created 'CTRL' bone collection.")
    else:
        ctrl_collection = bone_collections["CTRL"]

    # Assign bones to the appropriate collections and assign colors based on naming conventions
    for pose_bone in armature.pose.bones:
        bone_name = pose_bone.name
        armature_bone = armature.data.bones[bone_name]

        # Set the color only for CTRL bones, skip theme for original bones
        if bone_name.startswith("CTRL_"):
            # Determine the color theme based on the bone name
            if "root" in bone_name.lower() or "spine" in bone_name.lower():
                color_theme = 'THEME09'  # Root or spine-related bones
            elif ".l" in bone_name.lower():  # Left-side bones (.l or .L)
                color_theme = 'THEME04'
            elif ".r" in bone_name.lower():  # Right-side bones (.r or .R)
                color_theme = 'THEME03'
            else:
                color_theme = 'THEME07'  # General bones (neither left nor right)

            ctrl_collection.assign(armature_bone)  # Assign CTRL bones to the CTRL collection
            armature_bone.use_deform = False  # Mark CTRL bones as non-deform
            print(f"Assigned '{bone_name}' to 'CTRL' collection and marked as non-deform.")

            # Set the color theme for both Armature Bone and Pose Bone
            armature_bone.color.palette = color_theme  # Armature Bone color
            pose_bone.color.palette = color_theme      # Pose Bone color

        else:
            def_collection.assign(armature_bone)  # Assign original bones to the DEF collection
            print(f"Assigned '{bone_name}' to 'DEF' collection.")

    # Loop over all bones in the DEF collection and set pose_bone.color.palette = 'NONE'
    for bone in def_collection.bones:
        pose_bone = armature.pose.bones.get(bone.name)
        if pose_bone:
            pose_bone.color.palette = 'DEFAULT'  # Remove the color from the Pose Bone
            print(f"Set '{bone.name}' color to 'NONE' in DEF collection.")


# Step 0: Check and add 'DEF_' prefix if not present
step_0_check_and_add_def_prefix()

# Step 1: Duplicate bones in Edit Mode
step_1_duplicate_bones()

# Step 2: Add CTRL_ prefix to duplicated bones
step_2_add_ctrl_prefix()

# Step 3: Switch to Pose Mode
step_3_switch_to_pose_mode()

# Step 4: Add Copy Transforms constraint
step_4_add_copy_transforms_constraint()

# Step 5: Create DEF and CTRL bone collections and assign bones
step_5_create_bone_collections_and_assign_colors()
