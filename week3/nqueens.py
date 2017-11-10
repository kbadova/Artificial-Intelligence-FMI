import random
from copy import deepcopy
'''
1) initialize_matrix_with_queens
    random_list = cerate_random_list(from 0 to 3)
    i = 0
    for col in matrix:
        if i == random_list.length() - 1:
            break
        col[random_list[i]] = "{}queen".format(i + 1)
        i += 1

    example:
    random_list = [0, 3, 1, 2]
    matrrix = [['*', '_', '_', '_'],
               ['_', '_', '_', '*'],
               ['_', '*', '_', '_'],
               ['_', '_', '*, '_']]

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


# Списък с обходените матрични индекси
traversed_indexes = []


def initialize_matrix_with_n_queens(n):
    # [(1, 1), (2, 2), (3, 0)]
    queens_indexes = []

    # [1, 2, 0]
    queen_indexes_per_row = random.sample(range(n), n)

    while queen_indexes_per_row in traversed_indexes:
        queen_indexes_per_row = random.sample(range(n), n)

        traversed_indexes.append(queen_indexes_per_row)

    matrix = []
    for i in range(n):
        col = ['_', '_', '_', '_']
        col[queen_indexes_per_row[i]] = "*"
        matrix.append(col)
        queens_indexes.append((i, queen_indexes_per_row[i]))

    return matrix, queens_indexes


def get_most_conflicted_queen():
    pass


def get_least_conflicted_queen():
    pass


def reverse_queens():
    pass


def has_conflicts():
    pass


def initialize_conflicts(matrix, n, queens_indexes):
    indexes_with_conflicts = []
    
    for queen in queens_indexes:
        conflicts = 0
        list_with_queens_indexes = deepcopy(queens_indexes)
        list_with_queens_indexes.remove(queen)
        rest_queens = list_with_queens_indexes

        X_QUEEN = queen[0]
        Y_QUEEN = queen[1]

        if rest_queens:
            for nex_queen in rest_queens:
                NEXT_X_QUEEN = nex_queen[0]
                NEXT_Y_QUEEN = nex_queen[1]
                import ipdb; ipdb.set_trace()  # breakpoint 9f779389 //

                if abs(Y_QUEEN - X_QUEEN) == abs(NEXT_Y_QUEEN - NEXT_X_QUEEN):
                    conflicts += 1
                if Y_QUEEN + X_QUEEN == NEXT_Y_QUEEN + NEXT_X_QUEEN:
                    conflicts += 1

        indexes_with_conflicts.append(((queen), conflicts))
    # for i in range(n):
        # conflicts = 0

        # if i == 0:
        #     if queen_indexes_per_row[i] == 0:
        #         # [0* , 1 , 3, 2] да има царица в горния и долния  десен диагонал
        #         if queen_indexes_per_row[i] == queen_indexes_per_row[i + 1] - 1:
        #             conflicts += 1
        #     # [2*, 1, 0, 3] да има царица в горния и долния десен диагонал
        #     if queen_indexes_per_row[i] == queen_indexes_per_row[i + 1] + 1:
        #         conflicts += 1

        # if i == n - 1:
        #     if queen_indexes_per_row[i] == 0:
        #         # [3 , 2 , 1, *0] да има царица в горния и долния  ляв диагонал
        #         if queen_indexes_per_row[i] == queen_indexes_per_row[i - 1] + 1:
        #             conflicts += 1

        #     # [3, 0, 1, 2*] да има царица в горния и долния ляв диагонал
        #     if queen_indexes_per_row[i] == queen_indexes_per_row[i - 1] + 1:
        #         conflicts += 1
        # else:
        #     if queen_indexes_per_row[i] == queen_indexes_per_row[i + 1] + 1:  # да има царица в горния и долния десен диагонал
        #         conflicts += 1
        #     if queen_indexes_per_row[i] == queen_indexes_per_row[i - 1] - 1:  # да има царица в горния и долния ляв диагонал
        #         conflicts += 1

        # indexes_with_conflicts.append((i, conflicts))
    return indexes_with_conflicts


def solve(n):
    matrix, queens_indexes = initialize_matrix_with_n_queens(n)
    print("queens_indexes")
    print(queens_indexes)

    indexes_with_conflicts = initialize_conflicts(matrix, n, queens_indexes)
    print("indexes_with_conflicts")
    print(indexes_with_conflicts)

    # most_conflicted_queen = get_most_conflicted_queen(indexes_with_conflicts)

    # least_conflicted_queen = get_least_conflicted_queen(indexes_with_conflicts)

    # reversed_matrix = reverse_queens(most_conflicted_queen, least_conflicted_queen)

    # if has_conflicts(reversed_matrix):
    #     solve(n)
    # return reversed_matrix


def n_queens():
    n = 4

    result = solve(n)

    print(result)


if __name__ == "__main__":
    n_queens()
