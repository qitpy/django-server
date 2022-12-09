from core.models import TodoCard


def separate_to_tasks_by_color_from_serialize_data(deserialize_data):
    """
    convert from list(TodoCard) to list TodoCards by color
    """
    task_sorted_by_pink = filter(
        lambda x: x['color'] == TodoCard.TodoCardColor.PINK,
        deserialize_data)
    task_sorted_by_orange = filter(
        lambda x: x['color'] == TodoCard.TodoCardColor.ORANGE,
        deserialize_data)
    task_sorted_by_blue = filter(
        lambda x: x['color'] == TodoCard.TodoCardColor.BLUE,
        deserialize_data)
    task_sorted_by_green = filter(
        lambda x: x['color'] == TodoCard.TodoCardColor.GREEN,
        deserialize_data)

    instance = {}
    instance['pink_task'] = list(task_sorted_by_pink)
    instance['orange_task'] = list(task_sorted_by_orange)
    instance['blue_task'] = list(task_sorted_by_blue)
    instance['green_task'] = list(task_sorted_by_green)

    return instance
