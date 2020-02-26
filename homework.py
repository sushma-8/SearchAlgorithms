import heapq
from collections import deque
from itertools import count


def find_bfs_path(prev, target):
    output_path = []
    temp = target
    while temp is not None:
        output_path.insert(0, ','.join(map(str, list(temp)[::-1])))
        temp = prev[tuple(temp)]
    return output_path


def find_ucs_path(prev, target):
    output_path = []
    temp = target
    while temp is not None:
        output_path.insert(0, ','.join(map(str, list(temp)[::-1])))
        temp = prev[tuple(temp)][0]
    return output_path


def is_valid_neighbor(neighbor, z, current_xy):
    if 0 <= neighbor[0] < map_row and 0 <= neighbor[1] < map_column and abs(z[neighbor[0]][neighbor[1]] - z[current_xy[0]][current_xy[1]]) <= elevation:
        return True
    return False


def BreadthFirstSearch(target, land_xy, z):
    open_queue = deque([land_xy])
    prev = {tuple(land_xy): None}
    n_value = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]

    while open_queue:
        current_xy = open_queue.popleft()
        if current_xy == target:
            return find_bfs_path(prev, target)

        for i in range(len(n_value)):
            neighbor = [current_xy[0] + n_value[i][0], current_xy[1] + n_value[i][1]]
            if is_valid_neighbor(neighbor, z, current_xy) and tuple(neighbor) not in prev:
                open_queue.append(neighbor)
                prev[tuple(neighbor)] = current_xy

    return ["FAIL"]


def UniformCostSearch(target, land_xy, z):
    tiebreaker = count()
    open_queue = [(0, next(tiebreaker), land_xy)]

    prev = {tuple(land_xy): [None, 0, 1]}
    n_value = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]

    while open_queue:
        cost, temp, current_xy = heapq.heappop(open_queue)
        if prev[tuple(current_xy)][2] == 0:
            continue

        if current_xy == target:
            return find_ucs_path(prev, target)

        for i in range(len(n_value)):
            neighbor = [current_xy[0] + n_value[i][0], current_xy[1] + n_value[i][1]]

            if i > 3:
                add_cost = 14
            else:
                add_cost = 10
            if is_valid_neighbor(neighbor, z, current_xy):
                if tuple(neighbor) in prev and prev[tuple(neighbor)][1] > (cost + add_cost) and prev[tuple(neighbor)][2] == 1:
                    heapq.heappush(open_queue, (cost + add_cost, next(tiebreaker), neighbor))
                    prev[tuple(neighbor)] = [current_xy, cost + add_cost, 1]

                elif tuple(neighbor) not in prev:
                    heapq.heappush(open_queue, (cost + add_cost, next(tiebreaker), neighbor))
                    prev[tuple(neighbor)] = [current_xy, cost + add_cost, 1]

            prev[tuple(current_xy)][2] = 0

    return ["FAIL"]


def AStar(target, land_xy, z):
    tiebreaker = count()
    open_queue = [(0, 0, 0, next(tiebreaker), land_xy)]
    prev = {}
    x = abs(target[0] - land_xy[0])
    y = abs(target[1] - land_xy[1])
    h = 14 * min(x, y) + 10 * (max(x, y) - min(x, y))
    prev[tuple(land_xy)] = [None, h, 1]
    n_value = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]

    while open_queue:
        cost1, temp, gn, tb, current_xy = heapq.heappop(open_queue)
        if prev[tuple(current_xy)][2] == 0:
            continue

        if current_xy == target:
            return find_ucs_path(prev, target)

        for i in range(len(n_value)):
            neighbor = [current_xy[0] + n_value[i][0], current_xy[1] + n_value[i][1]]
            if i > 3:
                add_cost = 14
            else:
                add_cost = 10

            if 0 <= neighbor[0] < map_row and 0 <= neighbor[1] < map_column:
                diff = abs(z[neighbor[0]][neighbor[1]] - z[current_xy[0]][current_xy[1]])
                if diff > elevation:
                    continue
                g = gn + add_cost + diff
                x = abs(target[0] - neighbor[0])
                y = abs(target[1] - neighbor[1])
                h = 14 * min(x, y) + 10 * (max(x, y) - min(x, y))
                if tuple(neighbor) in prev and prev[tuple(neighbor)][1] > (g + h) and prev[tuple(neighbor)][2] == 1:
                    heapq.heappush(open_queue, (g + h, h, g, next(tiebreaker), neighbor))
                    prev[tuple(neighbor)] = [current_xy, g + h, 1]
                elif tuple(neighbor) not in prev:
                    heapq.heappush(open_queue, (g + h, h, g, next(tiebreaker), neighbor))
                    prev[tuple(neighbor)] = [current_xy, g + h, 1]

        prev[tuple(current_xy)][2] = 0

    return ["FAIL"]


if __name__ == '__main__':
    global map_column
    global map_row
    global elevation
    with open('input44.txt', 'r') as fp:
        algorithm = fp.readline().strip()
        line = fp.readline().split()
        map_column = int(line[0])
        map_row = int(line[1])

        land_xy = fp.readline().split()[::-1]
        land_xy = list(map(int, land_xy))

        elevation = int(fp.readline())
        target_num = int(fp.readline())

        target_xy = []
        for i in range(target_num):
            line = fp.readline().split()[::-1]
            target_xy.append(list(map(int, line)))
        z = []
        for i in range(map_row):
            z.append([])
            line = fp.readline().strip().split()
            z[i] = (map(int, line))
        path = []

        for target in target_xy:

            if algorithm == "BFS":
                path.append(BreadthFirstSearch(target, land_xy, z))
            elif algorithm == "UCS":
                path.append(UniformCostSearch(target, land_xy, z))
            elif algorithm == "A*":
                path.append(AStar(target, land_xy, z))

        fp.close()

        with open('output.txt', 'w+') as fp:
            fp.write('\n'.join([' '.join(item) for item in path]))
        fp.close()
