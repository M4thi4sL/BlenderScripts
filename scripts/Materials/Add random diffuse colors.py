import bpy
import random

# Function to set a random base color to a material
def set_random_base_color(material):
    # Generate random color values
    r = random.random()
    g = random.random()
    b = random.random()
    
    # Set the base color
    material.diffuse_color = (r, g, b, 1.0)

# Loop through selected objects
for obj in bpy.context.selected_objects:
    if obj.type == 'MESH':
        # Loop through materials of the object
        for slot in obj.material_slots:
            material = slot.material
            if material:
                set_random_base_color(material)
