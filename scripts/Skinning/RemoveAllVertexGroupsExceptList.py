import bpy

keep_vertex_groups = ['head.x', 'hair_scale']

# Get the selected objects
selected_objects = bpy.context.selected_objects

# Iterate over each selected object
for obj in selected_objects:
    if obj.type == 'MESH':
        # Remove vertex groups that are not in the keep_vertex_groups list
        for vertex_group in obj.vertex_groups[:]:
            if vertex_group.name not in keep_vertex_groups:
                obj.vertex_groups.remove(vertex_group)
