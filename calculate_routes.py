import queue

import mlrose

# numbers are products
# C indicates aisle
# W indicates wall
MAX_X = 10
MAX_Y = 10

super_matrix = [["0", 'C', "2", "3", "4", "5", "6", "7", "8", 'W'],
                ["10", 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', "11"],
                ["12", 'C', 'W', 'W', 'W', 'W', 'W', 'W', 'C', "13"],
                ["14", 'C', 'C', 'C', 'C', 'C', 'C', 'C', 'C', "15"],
                ['W', "16", 'C', "17", 'W', "18", 'C', 'C', 'C', "19"],
                ['W', "20", 'C', "21", 'W', "22", 'C', 'W', 'W', 'W'],
                ['W', "23", 'C', "24", 'W', "26", 'C', "27", "28", "29"],
                ['W', "30", 'C', "31", 'W', "32", 'C', 'C', 'C', 'C'],
                ["33", 'C', 'C', 'C', 'C', 'C', 'C', "34", "35", "36"],
                ['W', "37", 'C', "38", 'W', "39", 'C', 'W', 'W', 'W']]


# shopping_list=["0","2","8", "19", "25", "36","35","33"]
# shopping_list = ["0","10", "18", "5", "17", "6", "7", "24", "21", "11","37"] #min=29 for now
# shopping_list = ["10", "14", "20", "17", "18", "19", "11", "6", "4", "0", "33"]
# shopping_list = ["0", "25", "20", "26", "36", "15", "31", "34", "29", "19", "33", "3", "8", "23", "28"]
# shopping_list= ["0" , "37"]


def print_helper(matrix, route=[], shopping_list=[]):
    CEND = '\033[0m'
    CREDBG = '\033[41m'
    CGREENBG2 = '\033[102m'
    CBLUEBG = '\33[44m'
    CYELLOWBG = '\33[43m'
    CGREYBG = '\33[100m'

    for i, arr in enumerate(matrix):
        to_print = ""
        for j, item in enumerate(arr):
            if item == 'W':
                to_print += (CREDBG + str(item))
            elif item == 'C' and (i, j) not in route:
                to_print += CGREYBG + str(item)
            elif item == 'C' and (i, j) in route:
                to_print += CGREENBG2 + str(item)
            elif item in shopping_list:
                to_print += CYELLOWBG + "P" + CEND
            else:
                to_print += CBLUEBG + "P" + CEND
            to_print += CEND
        print(to_print)


def find_item_coor(item, matrix):
    for i, row in enumerate(matrix):
        for j, elem in enumerate(row):
            if elem == item:
                return (i, j)
    return False


def calc_distance_between_all_list(matrix, items):
    new_items = sorted(items)
    distances_list = []
    routes_list = []
    for t, item in enumerate(new_items):
        curr_dict, curr_route_dict = calc_distance_between_item_to_rest(find_item_coor(item, matrix), matrix,
                                                                        new_items[t:])
        for key in curr_dict:
            distances_list.append((item, key, curr_dict[key]))
            routes_list.append((item, key, curr_route_dict[key]))
    return distances_list, routes_list


def calc_distance_between_item_to_rest(source_coor, matrix, items):
    modified_matrix = [row[:] for row in matrix]
    distance_dict = {}
    route_dict = {}
    steps_queue = queue.Queue()
    steps_queue.put(source_coor)
    modified_matrix[source_coor[0]][source_coor[1]] = 0  # distance to myself is 0
    while not steps_queue.empty():
        curr_coor = steps_queue.get()

        try_reaching_to_an_item(curr_coor, modified_matrix, distance_dict, route_dict, items)

        # Trying to step right
        if can_move_right(curr_coor, modified_matrix):
            right_coor = (curr_coor[0], curr_coor[1] + 1)
            steps_queue.put(right_coor)
            update_distance(curr_coor, right_coor, modified_matrix)

        # Trying to step left
        if can_move_left(curr_coor, modified_matrix):
            left_coor = (curr_coor[0], curr_coor[1] - 1)
            steps_queue.put(left_coor)
            update_distance(curr_coor, left_coor, modified_matrix)

        # Trying to step up
        if can_move_up(curr_coor, modified_matrix):
            up_coor = (curr_coor[0] - 1, curr_coor[1])
            steps_queue.put(up_coor)
            update_distance(curr_coor, up_coor, modified_matrix)

        # Trying to step down
        if can_move_down(curr_coor, modified_matrix):
            down_coor = (curr_coor[0] + 1, curr_coor[1])
            steps_queue.put(down_coor)
            update_distance(curr_coor, down_coor, modified_matrix)

    return distance_dict, route_dict


def update_distance(curr_coor, new_coor, modified_matrix):
    modified_matrix[new_coor[0]][new_coor[1]] = modified_matrix[curr_coor[0]][curr_coor[1]] + 1


def try_reaching_to_an_item(coor, matrix, distance_dict, route_dict, items):
    curr_distance = matrix[coor[0]][coor[1]]
    item_on_right = check_for_item((coor[0], coor[1] + 1), matrix)
    item_on_left = check_for_item((coor[0], coor[1] - 1), matrix)
    item_on_up = check_for_item((coor[0] - 1, coor[1]), matrix)
    item_on_down = check_for_item((coor[0] + 1, coor[1]), matrix)
    neighbors = [item_on_right, item_on_left, item_on_up, item_on_down]
    for item in neighbors:
        if item and item in items:
            if item not in distance_dict:
                distance_dict[item] = curr_distance
                route_dict[item] = find_route_to_source(coor, matrix)
    return


def find_route_to_source(coor, matrix):
    # soruce is where matrix[x][y]==0
    curr = coor
    path_lst = [curr]
    while matrix[curr[0]][curr[1]] != 0:
        if can_move_for_calc_route(curr, (curr[0], curr[1] + 1), matrix):
            curr = (curr[0], curr[1] + 1)
            path_lst.append(curr)
            continue
        if can_move_for_calc_route(curr, (curr[0], curr[1] - 1), matrix):
            curr = (curr[0], curr[1] - 1)
            path_lst.append(curr)
            continue
        if can_move_for_calc_route(curr, (curr[0] + 1, curr[1]), matrix):
            curr = (curr[0] + 1, curr[1])
            path_lst.append(curr)
            continue
        if can_move_for_calc_route(curr, (curr[0] - 1, curr[1]), matrix):
            curr = (curr[0] - 1, curr[1])
            path_lst.append(curr)
            continue

    return path_lst[::-1]


def can_move_right(coor, matrix):
    right_coor = (coor[0], coor[1] + 1)
    return can_move(right_coor, matrix)


def can_move_left(coor, matrix):
    left_coor = (coor[0], coor[1] - 1)
    return can_move(left_coor, matrix)


def can_move_up(coor, matrix):
    up_coor = (coor[0] - 1, coor[1])
    return can_move(up_coor, matrix)


def can_move_down(coor, matrix):
    down_coor = (coor[0] + 1, coor[1])
    return can_move(down_coor, matrix)


def bound_check(coor):
    if coor[0] >= MAX_X or coor[0] < 0:
        return False
    if coor[1] >= MAX_Y or coor[1] < 0:
        return False
    return True


def can_move(coor, matrix):
    return bound_check(coor) and matrix[coor[0]][coor[1]] == 'C'


def can_move_for_calc_route(source_coor, move_to_coor, matrix):
    return bound_check(move_to_coor) and isinstance(matrix[move_to_coor[0]][move_to_coor[1]], int) and \
           matrix[source_coor[0]][source_coor[1]] - matrix[move_to_coor[0]][move_to_coor[1]] == 1


def check_for_item(coor, matrix):
    if bound_check(coor):
        if type(matrix[coor[0]][coor[1]]) == type("string"):
            if matrix[coor[0]][coor[1]] != 'C' and matrix[coor[0]][coor[1]] != 'W':
                return matrix[coor[0]][coor[1]]
    return False


def input_converter(list_of_triplets):
    i = 0
    input_dict = {}
    new_input = []
    for (a, b, d) in sorted(list_of_triplets):
        if a not in input_dict:
            input_dict[a] = i
            i += 1
        if b not in input_dict:
            input_dict[b] = i
            i += 1
    for (a, b, d) in sorted(list_of_triplets):
        new_input.append((input_dict[a], input_dict[b], d if d > 0 else 1))
    return new_input, input_dict


def items_coor(super_matrix, shopping_list):
    coor_lst = []
    for i, row in enumerate(super_matrix):
        for j, item in enumerate(row):
            if item in shopping_list:
                coor_lst.append((i, j))
    return coor_lst


def calculate_route(super_matrix, shopping_list):
    shopping_list.append("0")  # go through enterance
    bfs, routes = calc_distance_between_all_list(super_matrix, shopping_list)
    bfs = sorted(bfs)
    (new_input, input_converter_dict) = input_converter(bfs)

    # Initialize fitness function object using dist_list
    fitness_dists = mlrose.TravellingSales(distances=new_input)
    # Define optimization problem object
    problem_fit = mlrose.TSPOpt(length=len(shopping_list), fitness_fn=fitness_dists, maximize=False)
    # Solve problem using the genetic algorithm
    # best_state, best_fitness = mlrose.genetic_alg(problem_fit, random_state = 2)
    best_state, best_fitness = mlrose.genetic_alg(problem_fit, mutation_prob=0.2,
                                                  max_attempts=200, pop_size=200, random_state=0)

    output_converter_dict = dict((v, k) for k, v in input_converter_dict.items())
    final_result = [output_converter_dict[x] for x in best_state]
    register_index = final_result.index("0")
    final_result = final_result[register_index:] + final_result[:register_index]
    final_route = []

    for (k, v) in zip(final_result, final_result[1:] + final_result[:1]):
        for (x, y, z) in routes:
            if k == x and v == y :
                final_route += z
            elif k == y and v == x:
                final_route += z[::-1]


    return final_route, items_coor(super_matrix, shopping_list)
