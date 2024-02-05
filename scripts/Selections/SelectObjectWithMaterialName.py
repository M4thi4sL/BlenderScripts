import bpy

# Set the material name you want to select
material_name = "MI_Asset.004"

# Deselect all objects
bpy.ops.object.select_all(action='DESELECT')

# Iterate through all objects in the scene
for obj in bpy.context.scene.objects:
    # Check if the object is a mesh
    if obj.type == 'MESH':
        # Iterate through all the materials assigned to the mesh
        for material_slot in obj.material_slots:
            # Check if the material name matches the one we are looking for
            if material_slot.material.name == material_name:
                # Select the object
                obj.select_set(True)
                break