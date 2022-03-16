
LINE = 0
COL = 1
directions = [[-1, 0], [0, 1], [0, -1], [1, 0]]


def find_way(starting_point, plan):
    for direction in directions:  # Путь существует и единственнен
        next_point = step(starting_point, direction)
        find, path = walk(next_point, direction, plan, starting_point, set(), starting_point)
        if find:
            return path
    return


def step(point, direction):
    return [point[LINE] + direction[LINE], point[COL] + direction[COL]]


def point_num(point, hor_size):
    return point[LINE] * hor_size + point[COL]


def equal_point(point, point_2):
    return point[LINE] == point_2[LINE] and point[COL] == point_2[COL]


def walk(point, current_direction, plan, starting_point, visited, prev_point):
    point_id = point_num(point, len(plan[0]))
    if point[LINE] < 0 or point[COL] < 0 or point[LINE] >= len(plan) or point[COL] >= len(plan[0]) or (point_id in visited):  # Вышли за границу
        return False, []
    nul = plan[point[LINE]][point[COL]] is not None  # Проверяем, в рабочей ли мы клетке
    visited.add(point_id)
    if not nul:  # Если точка оказалась нерабочей, то просто идем дальше
        if point[LINE] == starting_point[LINE] and point[COL] == starting_point[COL]:  # Вернулись в исходную позицию
            # print("find")
            return True, []
        next_point = step(point, current_direction)
        find, path = walk(next_point, current_direction, plan, starting_point, visited, point)
        if find:
            return find, path
        visited.remove(point_id)
    else:
        for direction in directions:
            next_point = step(point, direction)
            if equal_point(next_point, prev_point):
                continue
            find, path = walk(next_point, direction, plan, starting_point, visited, point)
            if not equal_point(direction, current_direction):  # Можем применить к направлениям, тк по сути это точки
                path.append(point)
            if find:
                return find, path
        visited.remove(point_id)

    return False, []


def find_min(way, plan):
    # print(way[0])
    min_elem = plan[way[0][LINE]][way[0][COL]]
    point = [way[0][LINE], way[0][COL]]
    for elem in way:
        if elem[2] == '-':
            if plan[elem[LINE]][elem[COL]] < min_elem:
                point = [elem[LINE], elem[COL]]
                min_elem = plan[elem[LINE]][elem[COL]]
    return min_elem, point


def change_plan(plan, start_point):
    way = find_way(start_point, plan)
    minus = True
    for i in range(len(way)):
        if minus:
            way[i].append("-")
        else:
            way[i].append("+")
        minus = not minus
    print("Ломаная пути\n", way)
    minimum, min_point = find_min(way, plan)
    plan[start_point[LINE]][start_point[COL]] = minimum
    for elem in way:
        if elem[2] == '-' and elem[LINE] == min_point[LINE] and elem[COL] == min_point[COL]:
            plan[elem[LINE]][elem[COL]] = None
        elif elem[2] == "-":
            plan[elem[LINE]][elem[COL]] -= minimum
        else:
            plan[elem[LINE]][elem[COL]] += minimum
    return plan
