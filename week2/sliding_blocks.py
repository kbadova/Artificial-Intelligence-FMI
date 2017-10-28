from copy import deepcopy
#  Списък от пътища, до които съм минала до момента
paths = [[]]

# Децата, през които имам възможност да мина и които не съм обходила
children = []

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
def moveByChild(child):
    traversed.append(child)


def geneateChildrenMatrixes(matrix, zero_indexes):
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

        if matrix not in traversed:
            newMatrixes.append(newMatrix)

    return newMatrixes


# Дава изминатия път до матрицата
def pathToMatrix(matrix):

    for path in paths:
        for matrix_list in path:
            if matrix in matrix_list:
                return matrix_list.index(matrix)
    return 0


def calculateManhatansRoad(mother_matrix, child_matrix):
    result = []
    for row in mother_matrix:
        for column in row:
            x = row.index(column)
            y = mother_matrix.index(row)
            if mother_matrix[x][y] != child_matrix[x][y]:
                element_value = mother_matrix[x][y]
                child_indexes = getElementIndexesFromMatrix(child_matrix, element_value)
                X = x - child_indexes[0]
                Y = y - child_indexes[1]
                result.append(abs(X + Y))

    return sum(result)


def calculateFunction(mother_matrix, child_matrix):
    road_length = pathToMatrix(mother_matrix) + 1
    h = calculateManhatansRoad(mother_matrix, child_matrix)

    f = h + road_length
    return f


# Генерира възможните chidren състояния от текущото и за всяко дете, смята f от неего до крайната goal_matrix
def generateChildrenFromMatrixIndexes(matrix, zero_indexes):
    children_matrixes = geneateChildrenMatrixes(matrix, zero_indexes)  #  [A,B,C]

    result = []
    for matrix_child in children_matrixes:

        f = calculateFunction(matrix, matrix_child)  # [(A, f(A), (B, f(B), (C, f(C)]
        result.append((matrix_child, f))

    return result


def appendNewChildrenToPaths(state_children):
    # state_children = [(C, f(C)), (D, f(D))]
    newPath = deepcopy(getByMatrixes)
    # newPath = [(A, f(A)), (B, f(B))]
    for child in state_children:
        if newPath in paths:
            paths.remove(newPath)

        newPath.append(child)
        # newPath = [(A, f(A)), (B, f(B)), (C, f(C))]
        paths.append(newPath)


# Обхожда всички листове с матрици и взима най-евтината f от paths =  [[(A, 4), (B, 5), (C, 7)], [ (D, 2), (O, 10)]]
def getMostCheapChild():
    functions = [matrix[1] for el in paths for matrix in el if matrix[0] != initial_marrix]
    max_fn = max(functions)
    most_cheap_child = [matrix for el in paths for matrix in el if matrix[1] == max_fn]
    return most_cheap_child[0]


# paths =  [[(A, 4), (B, 5), (C, 7)], [ (D, 2), (O, 10)]]
def checkEveryPathHasFinished():
    for path in paths:
        last_matrix = path.last()
        if last_matrix[0] == goal_matrix:
            return True
    return False


def getElementIndexesFromMatrix(matrix, element):
    for row in matrix:
        for column in row:
            if matrix[matrix.index(row)][row.index(column)] == element:
                return (row.index(column), matrix.index(row))
    return "No 0 found"


# matrix: (matrix, f)
def slide_blocks(matrix):
    getByMatrixes.append(matrix)
    zero_indexes = getElementIndexesFromMatrix(matrix[0], 0)
    print(zero_indexes)

    # Децата от текущото състояние
    state_children = generateChildrenFromMatrixIndexes(matrix[0], zero_indexes)
    appendNewChildrenToPaths(state_children)

    # # Взима най-евтиното дете
    child = getMostCheapChild()

    import ipdb; ipdb.set_trace()  # breakpoint 951ba6a1 //
    # # Минаваме през него
    # moveByChild(child)

    # everyPathHasFinished = checkEveryPathHasFinished()
    # if not (everyPathHasFinished):
    #     slide_blocks(child)
    #     # printPosition
    # else:
    #     print("hahah")
    #     return "ssfdf"
    #     # return matrix_length


def sliding_blocks():
    function = calculateFunction(initial_marrix, goal_matrix)
    paths.append([(initial_marrix, function)])
    del paths[0]
    slide_blocks((initial_marrix, function))


if __name__ == "__main__":
    sliding_blocks()