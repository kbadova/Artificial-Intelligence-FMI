#  Списък от пътища, до които съм минала до момента
paths = []

# Децата, през които имам възможност да мина и които не съм обходила
children = []

# Състояния на матрицата, през които сме минали
traversed = []


# initial_marrix = [[0, 7, 2],
#                   [1, 3, 4],
#                   [5, 6, 8]]

initial_marrix = [[1, 2, 3],
                  [4, 5, 6],
                  [0, 7, 8]]

goal_matrix = [[0, 1, 2],
               [3, 4, 5],
               [6, 7, 8]]


# Добавя матричното състояние за обходено
def moveByChild(child):
    traversed.append(child)


def geneateChildrenMatrixes(current_indexes):
    # Еxclude traversed
    pass


def calculateFunction(matrixes):
    pass


# Генерира възможните chidren състояния от текущото и за всяко дете, смята f от неего до крайната goal_matrix
def generateChildrenFromState(square_value, current_indexes):
    children_matrixes = geneateChildrenMatrixes()  #  [A,B,C]
    result = calculateFunction(children_matrixes)  # [(A, f(A), (B, f(B), (C, f(C)]
    return result


def appendNewChildrenToPaths(state_children):
    # state_children = [(C, f(C)), (D, f(D))]
    newPath = getByMatrixes
    # newPath = [(A, f(A)), (B, f(B))]
    for child in state_children:
        newList = newPath.append(child)
        # newList = [(A, f(A)), (B, f(B)), (C, f(C))]
        paths.append(newList)
        paths.delete(newPath)


# Обхожда всички листове с матрици и взима най-евтината f от paths =  [[(A, 4), (B, 5), (C, 7)], [ (D, 2), (O, 10)]]
def getMostCheapChild():
    pass


#  СЪбира през какви матрици сме минали до момента
getByMatrixes = []


# paths =  [[(A, 4), (B, 5), (C, 7)], [ (D, 2), (O, 10)]]
def checkEveryPathHasFinished():
    for path in paths:
        last_matrix = path.last()
        if last_matrix[0] == goal_matrix:
            return True
    return False


# matrix: (matrix, f)
def slide_blocks(matrix):
    getByMatrixes.append(initial_marrix)
    zero_indexes = getZeroFromCurrentMatrix(matrix)

    # Децата от текущото състояние
    state_children = generateChildrenFromState(zero_indexes)

    appendNewChildrenToPaths(state_children)

    # Взима най-евтиното дете
    child = getMostCheapChild()

    # Минаваме през него
    moveByChild(child)

    everyPathHasFinished = checkEveryPathHasFinished()
    if not (everyPathHasFinished):
        slide_blocks(child)
        # printPosition
    else:
        print("hahah")
        return "ssfdf"
        # return matrix_length


def sliding_blocks():

    slide_blocks(initial_marrix)


if __name__ == "__main__":
    sliding_blocks()