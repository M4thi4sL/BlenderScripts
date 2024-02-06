import bpy


def clean_material_names():
    # Get the selected objects
    selected_objects = bpy.context.selected_objects

    # Iterate through selected objects
    for obj in selected_objects:
        # Iterate through object's materials
        for slot in obj.material_slots:
            if slot.material is not None:
                # Clean material name
                slot.material.name = clean_name(slot.material.name)


def clean_name(name):
    # Split the name based on '.' separator
    parts = name.split(".")
    cleaned_parts = []
    # Iterate through parts and keep only those that don't match the pattern ".xxx" where xxx is numeric
    for part in parts:
        if not part.isdigit():
            cleaned_parts.append(part)
    # Join cleaned parts with '.' separator
    cleaned_name = ".".join(cleaned_parts)
    return cleaned_name


# Run the cleaning function
clean_material_names()
