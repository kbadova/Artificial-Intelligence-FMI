from copy import deepcopy
#  Списък от пътища, до които съм минала до момента
paths = [[]]

# Генерираните матрични състояния
childrenStates = []

# Състояния на матрицата, през които сме минали
traversed = []


#  СЪбира през какви матрици сме минали до момента
getByMatrixes = []


# initial_marrix = [[0, 7, 2],
#                   [1, 3, 4],
#                   [5, 6, 8]]

initial_marrix = [[1, 2, 3],
                  [4, 5, 6],
                  [0, 7, 8]]

goal_matrix = [[1, 2, 3],
               [4, 5, 6],
               [7, 8, 0]]


# Добавя матричното състояние за обходено
def traverseMatrix(child_matrix):
    traversed.append(child_matrix)


def geneate_children_matrixes(matrix, zero_indexes):
    # Еxclude traversed
    zero_x = zero_indexes[0]
    zero_y = zero_indexes[1]
    newIndexes = [(zero_x + 1, zero_y), (zero_x, zero_y + 1),
                  (zero_x - 1, zero_y), (zero_x, zero_y - 1)]
    validIndexes = [index for index in newIndexes if (index[0] >= 0 and index[0] <= 2 and index[1] >= 0 and index[1] <= 2)]

    newMatrixes = []
    for index_pair in validIndexes:
        matrixCopy = deepcopy(matrix)
        newMatrix = matrixCopy
        number = matrixCopy[index_pair[1]][index_pair[0]]
        newMatrix[index_pair[1]][index_pair[0]] = 0
        newMatrix[zero_y][zero_x] = number

        if newMatrix not in traversed or newMatrix not in childrenStates:
            childrenStates.append(newMatrix)
            newMatrixes.append(newMatrix)

    return newMatrixes


# Дава изминатия път до матрицата
def pathToMatrix(matrix):
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


def calculateFunction(mother_matrix, child_matrix):
    road_length = pathToMatrix(mother_matrix) + 1
    h = calculate_manhatans_road(mother_matrix, child_matrix)

    f = h + road_length
    return f


# Генерира възможните chidren състояния от текущото и за всяко дете, смята f от неего до крайната goal_matrix
def generate_children_from_matrix_indexes(matrix, zero_indexes):
    children_matrixes = geneate_children_matrixes(matrix, zero_indexes)  #  [A,B,C]
    result = []

    for matrix_child in children_matrixes:
        f = calculateFunction(matrix, matrix_child)  # [(A, f(A), (B, f(B), (C, f(C)]
        result.append((matrix_child, f))

    return result


def getMotherMatrixRoad(mother_matrix):
    for path in paths:
        if path[len(path) - 1][0] == mother_matrix[0]:
            return path
    return False


def appendNewChildrenToPaths(mother_matrix, state_children):
    # state_children = [(C, f(C)), (D, f(D))]
    # newPath = [(A, f(A)), (B, f(B))]
    currentRoad = getMotherMatrixRoad(mother_matrix)
    for child in state_children:
        newPath = deepcopy(currentRoad)
        if currentRoad is False:
            newPath = deepcopy(getByMatrixes)
        if newPath in paths:
            paths.remove(newPath)

        newPath.append(child)
        # newPath = [(A, f(A)), (B, f(B)), (C, f(C))]
        paths.append(newPath)


# Обхожда всички листове с матрици и взима най-евтината f от paths =  [[(A, 4), (B, 5), (C, 7)], [ (D, 2), (O, 10)]]
def getMostCheapChild():
    last_children_in_paths = [path[len(path) - 1] for path in paths]
    not_traversed_children = [el for el in last_children_in_paths if el[0] not in traversed]
    functions = [el[1] for el in not_traversed_children if el[0] != initial_marrix]
    if functions == []:
        return False
    max_fn = max(functions)
    most_cheap_child = [child for child in not_traversed_children if child[1] == max_fn]

    return most_cheap_child[0]


def get_element_by_indexes_from_matrix(matrix, element):
    for row in matrix:
        for column in row:
            if matrix[matrix.index(row)][row.index(column)] == element:
                return (row.index(column), matrix.index(row))
    return "No 0 found"


def check_goal_not_in_paths():
    for path in paths:
        if path[len(path) - 1][0] == goal_matrix:
            return True
    return False


def get_steps_to_goal():
    for path in paths:
        if path[len(path) - 1][0] == goal_matrix:
            return len(path) - 1
    return "No goal found"


# matrix: (matrix, f)
def slide_blocks(matrix):

    getByMatrixes.append(matrix)
    traverseMatrix(matrix[0])

    zero_indexes = get_element_by_indexes_from_matrix(matrix[0], 0)

    # Генерира децата от текущото състояние
    state_children = generate_children_from_matrix_indexes(matrix[0], zero_indexes)

    # Добавя децата към пътищата на родителите им
    appendNewChildrenToPaths(matrix, state_children)

    # # Взима най-евтиното дете
    child = getMostCheapChild()

    goal_not_in_paths = check_goal_not_in_paths()
    if goal_not_in_paths is False:
        return slide_blocks(child)

    print("Steps needed")
    print(get_steps_to_goal())


def sliding_blocks():
    function = calculateFunction(initial_marrix, goal_matrix)
    childrenStates.append(initial_marrix)
    paths.append([(initial_marrix, function)])
    del paths[0]

    slide_blocks((initial_marrix, function))


if __name__ == "__main__":
    sliding_blocks()
