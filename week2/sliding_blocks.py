import argparse
import sys
from copy import deepcopy
sys.setrecursionlimit(1800)

parser = argparse.ArgumentParser(description='Solving sliding blocks with Manhatan distance.')
parser.add_argument('-n', type=int, required=True,
                    help='Number of blocks')
parser.add_argument('-m', required=True,
                    help='Matrix')
arguments = parser.parse_args()

#  Списък от пътища, до които съм минала до момента
paths = [[]]

# Генерираните матрични състояния
childrenStates = []

# Състояния на матрицата, през които сме минали
traversed = []


#  СЪбира през какви матрици сме минали до момента
get_by_matrixes = []


roads = []
# up
# initial_matrix = [[1, 2, 3],
#                   [4, 5, 0],
#                   [7, 8, 6]]

# # right up left left
# initial_matrix = [[1, 2, 3],
#                   [5, 0, 6],
#                   [4, 7, 8]]

# # up left left
# initial_matrix = [[1, 2, 3],
#                   [0, 5, 6],
#                   [4, 7, 8]]

# left left
# initial_matrix = [[1, 2, 3],
#                   [4, 5, 6],
#                   [0, 7, 8]]

goal_matrix = [[1, 2, 3],
               [4, 5, 6],
               [7, 8, 0]]

# [[2, 3, 6], [1,5, 8], [4,7,0]] - 8 steps
# [[1, 3, 0], [4,5, 6], [7,8,2]] - 10 steps

"""
initial_matrix = [[7, 2, 3], [4,0, 5], [8,1,6]]
  -> 11 steps ok
 goal_matrix = [[1, 2, 3], [0, 4, 5], [7, 8, 6]]

 -> 10 steps ok
 goal_matrix = [[0, 2, 3], [1, 4, 5], [7, 8, 6]]

 -> 12 steps ok

 goal_matrix = [[1, 2, 3], [4, 0, 5], [7, 8, 6]]

 -> 13 steps ok
goal_matrix = [[1, 2, 3], [4, 5, 0], [7, 8, 6]]

 -> 14 steps ok
right
down
left
up
up
right
down
left
down
right
up
left
left
up
goal_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
"""

# initial_matrix = [[1, 7, 4], [6, 8, 3], [2, 5, 0]] -> steps
# initial_matrix = [[6, 5, 3], [2, 4, 8], [7, 0, 1]] -> ? steps


# Добавя матричното състояние за обходено
def traverse_matrix(child_matrix):
    traversed.append(child_matrix)


def geneate_children_matrixes(matrix, zero_indexes):
    # Еxclude traversed
    zero_x = zero_indexes[0]
    zero_y = zero_indexes[1]
    newIndexes = [(zero_x + 1, zero_y), (zero_x, zero_y + 1),
                  (zero_x - 1, zero_y), (zero_x, zero_y - 1)]
    valid_indexes = [index for index in newIndexes if (index[0] >= 0 and index[0] <= 2 and index[1] >= 0 and index[1] <= 2)]

    new_matrixes = []
    matrix_copy = str(matrix)
    for index_pair in valid_indexes:
        new_matrix = list(eval(matrix_copy))
        number = new_matrix[index_pair[1]][index_pair[0]]
        new_matrix[zero_y][zero_x] = number
        new_matrix[index_pair[1]][index_pair[0]] = 0

        if new_matrix not in traversed and new_matrix not in childrenStates:
            childrenStates.append(new_matrix)
            new_matrixes.append(new_matrix)

    return new_matrixes


# Дава изминатия път до матрицата
def path_to_matrix(matrix):
    global paths
    for path in paths:
        if path != [] and matrix == path[len(path) - 1][0]:
            return len(path) - 1
    return 0


def calculate_manhatans_road(mother_matrix, child_matrix):
    result = []
    for row in mother_matrix:
        for column in row:
            x = row.index(column)
            y = mother_matrix.index(row)
            if mother_matrix[x][y] != child_matrix[x][y]:
                element_value = mother_matrix[x][y]
                child_indexes = get_element_by_indexes_from_matrix(child_matrix, element_value)
                X = x - child_indexes[0]
                Y = y - child_indexes[1]
                result.append(abs(X + Y))

    return sum(result)


def calculate_function(mother_matrix, child_matrix):
    road_length = path_to_matrix(mother_matrix) + 1
    h = calculate_manhatans_road(mother_matrix, child_matrix)

    f = h + road_length
    return f


# Генерира възможните chidren състояния от текущото и за всяко дете, смята f от неего до крайната goal_matrix
def generate_children_from_matrix_indexes(matrix, zero_indexes):
    new_matrixes = []

    zero_x = zero_indexes[0]
    zero_y = zero_indexes[1]
    newIndexes = [(zero_x + 1, zero_y), (zero_x, zero_y + 1),
                  (zero_x - 1, zero_y), (zero_x, zero_y - 1)]
    valid_indexes = [index for index in newIndexes if (index[0] >= 0 and index[0] <= 2 and index[1] >= 0 and index[1] <= 2)]

    matrix_copy = str(matrix)
    for index_pair in valid_indexes:
        new_matrix = list(eval(matrix_copy))
        number = new_matrix[index_pair[1]][index_pair[0]]
        new_matrix[zero_y][zero_x] = number
        new_matrix[index_pair[1]][index_pair[0]] = 0

        # Еxclude traversed
        if new_matrix not in traversed and new_matrix not in childrenStates:
            f = calculate_function(matrix, new_matrix)  # [(A, f(A), (B, f(B), (C, f(C)]

            childrenStates.append(new_matrix)
            new_matrixes.append((new_matrix, f))

    return new_matrixes


def get_mother_matrix_road(mother_matrix):
    global paths
    for path in paths:
        if path[len(path) - 1][0] == mother_matrix[0]:
            return path
    return False


def append_new_children_to_paths(mother_matrix, state_children):
    # state_children = [(C, f(C)), (D, f(D))]
    # newPath = [(A, f(A)), (B, f(B))]
    global get_by_matrixes
    currentRoad = get_mother_matrix_road(mother_matrix)

    for child in state_children:
        t = tuple(currentRoad)
        tuplePath = t

        # newPath = [(A, f(A)), (B, f(B)), (C, f(C))]
        newPath = list(tuplePath)
        newPath.append(child)

        global paths
        paths.append(newPath)

        if child[0] == goal_matrix:
            print("heeehehehehehehhe solution")
            return True

    return False


# Обхожда всички листове с матрици и взима най-евтината f от paths =  [[(A, 4), (B, 5), (C, 7)], [ (D, 2), (O, 10)]]
def get_most_cheap_child():
    global paths
    last_children_in_paths = [path[len(path) - 1] for path in paths]

    not_traversed_children = [el for el in last_children_in_paths if el[0] not in traversed and str(el[0]) != str(initial_matrix)]

    functions = [el[1] for el in not_traversed_children]

    min_fn = min(functions)
    most_cheap_child = [child for child in not_traversed_children if child[1] == min_fn]

    return most_cheap_child[0]


def get_element_by_indexes_from_matrix(matrix, element):
    for row in matrix:
        for column in row:
            if matrix[matrix.index(row)][row.index(column)] == element:
                return (row.index(column), matrix.index(row))
    return "No 0 found"


def check_goal_not_in_paths():
    global paths
    for path in paths:
        if str(path[len(path) - 1][0]) == str(goal_matrix):
            print("GOAL FOUND")
            return True
    return False


def get_steps_to_goal():
    global paths
    for path in paths:
        if path[len(path) - 1][0] == goal_matrix:
            return (path, len(path) - 1)
    return "No goal found"


def print_ways():
    result_steps = get_steps_to_goal()
    result_path = result_steps[0]

    counter = 0
    for matrix in result_path:
        if counter < len(result_path) - 1:
            zero_indexes = get_element_by_indexes_from_matrix(matrix[0], 0)
            zero_x = zero_indexes[0]
            zero_y = zero_indexes[1]

            next_matrix = result_path[counter + 1]
            next_zero_indexes = get_element_by_indexes_from_matrix(next_matrix[0], 0)
            next_zero_x = next_zero_indexes[0]
            next_zero_y = next_zero_indexes[1]

            if (zero_x == next_zero_x and zero_y > next_zero_y):
                print("down")
            if (zero_x > next_zero_x and zero_y == next_zero_y):
                print("right")
            if (zero_x == next_zero_x and zero_y < next_zero_y):
                print("up")
            if (zero_x < next_zero_x and zero_y == next_zero_y):
                print("left")

            counter += 1

    print("Steps needed")
    print(result_steps[1])


def slide(matrix):
    get_by_matrixes.append(matrix)
    traverse_matrix(matrix[0])

    zero_indexes = get_element_by_indexes_from_matrix(matrix[0], 0)

    # Генерира децата от текущото състояние
    state_children = generate_children_from_matrix_indexes(matrix[0], zero_indexes)

    # Добавя децата към пътищата на родителите им
    has_found_solution = append_new_children_to_paths(matrix, state_children)
    return has_found_solution


# matrix: (matrix, f)
def slide_blocks(matrix):
    dd = check_goal_not_in_paths()
    has_found_solution = False
    while not dd:
        has_found_solution = slide(matrix)
        if has_found_solution:
            break
        else:
            # Взима най-евтиното дете
            matrix = get_most_cheap_child()
            print(matrix)

    return print_ways()


def sliding_blocks():
    global initial_matrix
    global paths

    number_of_blocks = arguments.n
    initial_matrix = arguments.m
    initial_matrix = eval(initial_matrix)
    if sum(len(x) for x in initial_matrix) != number_of_blocks + 1:
        raise "This is not {}-th matrix".format(number_of_blocks + 1)

    print("Initial matrix")
    print(initial_matrix)

    childrenStates.append(initial_matrix)
    paths.append([(initial_matrix, 0)])
    del paths[0]

    slide_blocks((initial_matrix, 0))


if __name__ == "__main__":
    sliding_blocks()
