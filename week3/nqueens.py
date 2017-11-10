'''
1) create_matrix
    [['_', '_', '_', '_'],
     ['_', '_', '_', '_'],
     ['_', '_', '_', '_'],
     ['_', '_', '_', '_']]

2) initialize_matrix_with_queens
    random_list = cerate_random_list(from 0 to 3)
    i = 0
    for col in matrix:
        if i == random_list.length() - 1:
            break
        col[random_list[i]] = "{}queen".format(i + 1)
        i += 1

    example:
    random_list = [0, 3, 1, 2]
    matrrix = [['1queen', '_', '_', '_'],
               ['_', '_', '_', '2queen'],
               ['_', '3queen', '_', '_'],
               ['_', '_', '4queen, '_']]

3) get_queen_with_most_conflicts


    most_conflicted_queen = get_most_conflicted_queen(if queen is not traversed)
    traversed.append(most_conflicted_queen)
    //most_conflicted_queen == (0, 2)

4) get_queen_with_less_conflicts

    least_conflicted_queen = get_least_conflicted_queen()
    //most_conflicted_queen == (1, 3)

5) reverse_queens
    coppiedMatrix = deepcopy(matrix)
    newMatrix = deepcopy(matrix)
    newMatrix[0][2] = coppiedMatrix[1][3]
    newMatrix[1][3] = coppiedMatrix[0][2]

6) check for conflicts and reiterate

    if has_conflicts(newMartix):
        solve(newMartix)

    return newMatrix

3 ) MAX ITER
'''


def create_matrix(n):
    pass


def initialize_matrix_with_queens():
    pass


def get_most_conflicted_queen():
    pass


def get_least_conflicted_queen():
    pass


def reverse_queens():
    pass


def has_conflicts():
    pass


def solve(matrix):
    most_conflicted_queen = get_most_conflicted_queen()

    least_conflicted_queen = get_least_conflicted_queen()

    reversed_matrix = reverse_queens(most_conflicted_queen, least_conflicted_queen)

    if has_conflicts(reversed_matrix):
        solve(reversed_matrix)
    return reversed_matrix


def n_queens():
    n = 4
    matrix = create_matrix(n)

    matrix = initialize_matrix_with_queens(matrix, n)

    result = solve(matrix)

    print(result)


if __name__ == "__main__":
    n_queens()