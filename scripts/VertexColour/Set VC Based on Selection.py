import bpy


def get_ordered_selection_objects():
    tagged_objects = []

    for o in bpy.data.objects:
        order_index = o.get("selection_order", -1)
        if order_index >= 0:
            tagged_objects.append((order_index, o))

    tagged_objects = sorted(tagged_objects, key=lambda item: item[0])

    return [o for i, o in tagged_objects]


def clear_order_flag(obj):
    try:
        del obj["selection_order"]
    except KeyError:
        pass


def update_selection_order():
    if not bpy.context.selected_objects:
        # Nothing selected. Clear any flagged objects and early out
        for o in bpy.data.objects:
            clear_order_flag(o)
        print("Selection is empty")
        return

    selection_order = get_ordered_selection_objects()

    idx = 0
    for o in selection_order:
        if not o.select_get():
            selection_order.remove(o)
            clear_order_flag(o)
        else:
            o["selection_order"] = idx
            idx += 1

    for o in bpy.context.selected_objects:
        if o not in selection_order:
            o["selection_order"] = len(selection_order)
            selection_order.append(o)

    print(f"Selection order: {selection_order}")


def set_vertex_colors_based_on_selection_order():
    # Get the ordered selection objects
    selected_objects = get_ordered_selection_objects()

    # Print the array size
    print("Array size:", len(selected_objects))

    # Calculate the maximum value for X based on the array size
    max_x = 1.0 / len(selected_objects)

    # Set the vertex color of each object based on its position in the array
    for i, obj in enumerate(selected_objects):
        # Calculate the value of X
        x = (i + 1) * max_x

        # Set the vertex color as grayscale
        obj.data.vertex_colors.new()
        color_layer = obj.data.vertex_colors.active
        for poly in obj.data.polygons:
            for loop_index in poly.loop_indices:
                loop_vert_index = obj.data.loops[loop_index].vertex_index
                color_layer.data[loop_index].color = (x, x, x, 1)  # Grayscale format (R=G=B=x, Alpha=1)


def selection_change_handler(scene):
    if bpy.context.mode != "OBJECT":
        return

    is_selection_update = False
    for u in bpy.context.view_layer.depsgraph.updates:
        if not u.is_updated_geometry and not u.is_updated_transform and not u.is_updated_shading:
            is_selection_update = True
            break

    if is_selection_update:
        update_selection_order()
        set_vertex_colors_based_on_selection_order()


def register():
    print('\033[2J')  # clear the terminal
    for o in bpy.data.objects:
        if o.get("selection_order", -1) >= 0:
            del o["selection_order"]

    bpy.app.handlers.depsgraph_update_post.append(selection_change_handler)


def unregister():
    for f in bpy.app.handlers.depsgraph_update_post:
        if f.__name__ == "selection_change_handler":
            bpy.app.handlers.depsgraph_update_post.remove(f)


if __name__ == "__main__":
    try:
        for f in bpy.app.handlers.depsgraph_update_post:
            if f.__name__ == "selection_change_handler":
                bpy.app.handlers.depsgraph_update_post.remove(f)

        register()
    except KeyboardInterrupt:
        unregister()
