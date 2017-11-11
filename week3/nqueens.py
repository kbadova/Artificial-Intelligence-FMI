import random
from copy import deepcopy
'''
1) initialize_matrix_with_queens
    queen_indexes_per_row = [0, 3, 1, 2]
    matrrix = [['*', '_', '_', '_'],
               ['_', '_', '_', '*'],
               ['_', '*', '_', '_'],
               ['_', '_', '*, '_']]

2) calculate_conflicts
     връща списък с координматите на дадена матрица и колко кобфликта има тя -> [((1,2), 3), ((0,3), 2), ((2,1), 1)]

3) get_queen_with_most_and_least_conflicts
    Връща tuple с цариците, които има най-малко и най-много конфликти
    most_and_least_conflicted_queens = get_most_and_least_conflicted_queens(indexes_with_conflicts)
    # most_and_least_conflicted_queens == [((1,2), 0), ((3,0), 3)]

4) reverse_queens_indexes
    Reverse-ва матричните индекси, като на тази царица,
    която има най-много конфликти слага тази царица, която има най-малко

5) check for conflicts and reiterate

    if has_conflicts(newMartix):
        solve(newMartix)

    ако няма конфликти, строия матрицата и я връщам
'''


# Списък със съществуващи индекси
existing_qeen_indexes = []

# Списък с обходените елементи от текущия списък с индекси
traversed = []


def initialize_queen_indexes(n):
    queens_indexes = []
    global existing_qeen_indexes

    # [1, 2, 0]
    queen_indexes_per_row = random.sample(range(n), n)

    MAX_ITER = 3 * n
    iteration = 1
    while queen_indexes_per_row in existing_qeen_indexes:
        if iteration == MAX_ITER:
            return False
        queen_indexes_per_row = random.sample(range(n), n)

        iteration += 1

    existing_qeen_indexes.append(queen_indexes_per_row)

    for i in range(n):
        queens_indexes.append((i, queen_indexes_per_row[i]))

    # [(1, 1), (2, 2), (3, 0)]
    return queens_indexes


def get_most_and_least_conflicted_queens(n, indexes_with_conflicts):
    # Ако всички матрици имат равен брой конфликти, избираме на random някоя, която не е обходена
    if set([couple[1] for couple in indexes_with_conflicts]) == set([indexes_with_conflicts[0][1]]):
        not_traversed_indexes_with_conflicts = [q for q in indexes_with_conflicts if q[0] not in traversed]
        return random.sample(set(not_traversed_indexes_with_conflicts), 2)

    min_conflicted_queen = None
    max_conflicted_queen = None

    min_conflicts = len(indexes_with_conflicts)
    max_conflicts = 0
    # За да не бъде избрана една и съща матрица за с минимални и максимални конфликти,
    # отбелязвам тези, които са избрани за максимални и мимални
    chosen_queens = []

    for queen_with_conflicts in indexes_with_conflicts:
        queen = queen_with_conflicts[0]
        conflicts = queen_with_conflicts[1]

        if conflicts > max_conflicts and queen not in chosen_queens and queen not in traversed:
            max_conflicts = conflicts
            max_conflicted_queen = (queen, max_conflicts)

        if conflicts < min_conflicts and queen not in chosen_queens and queen not in traversed:
            min_conflicts = conflicts
            min_conflicted_queen = (queen, min_conflicts)

        chosen_queens.append(queen)
    return (min_conflicted_queen, max_conflicted_queen)


def reverse_queens_indexes(queens_indexes, most_conflicted_queen, least_conflicted_queen):
    reversed_indexes = deepcopy(queens_indexes)
    for i in range(len(queens_indexes)):
        if queens_indexes[i] == most_conflicted_queen[0]:
            reversed_indexes[i] = least_conflicted_queen[0]
        if queens_indexes[i] == least_conflicted_queen[0]:
            reversed_indexes[i] = most_conflicted_queen[0]

    return reversed_indexes


def has_conflicts(reversed_indexes):
    indexes_with_conflicts = calculate_conflicts(reversed_indexes)
    # indexes_with_conflicts e [[((1, 1), 1), ((0, 0), 1), ((2, 3), 1), ((3, 2), 1)]
    # Ако сумата от конфликтите е 0, значи няма конфликти

    return sum([queen_indexes[1] for queen_indexes in indexes_with_conflicts]) != 0


def calculate_conflicts(queens_indexes):
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

                if Y_QUEEN - X_QUEEN == NEXT_Y_QUEEN - NEXT_X_QUEEN\
                        or Y_QUEEN + X_QUEEN == NEXT_Y_QUEEN + NEXT_X_QUEEN:
                    conflicts += 1

        indexes_with_conflicts.append(((queen), conflicts))
    return indexes_with_conflicts


def buld_matrix(n, reversed_indexes):
    matrix = []

    for i in range(n):
        col = ['_', '_', '_', '_']
        el = [ind for ind in reversed_indexes if ind[1] == i][0]

        col[el[0]] = "*"
        matrix.append(col)

    return matrix




def solve(n, queens_indexes):
    # Aко сме обходили всички царици и не сме намирили решение, return False и рекурсивно викам пак n_queens
    if set(queens_indexes) == set(traversed):
        return False

    indexes_with_conflicts = calculate_conflicts(queens_indexes)

    most_and_least_conflicted_queens = get_most_and_least_conflicted_queens(n, indexes_with_conflicts)

    least_conflicted_queen = most_and_least_conflicted_queens[0]
    most_conflicted_queen = most_and_least_conflicted_queens[1]
    traversed.append(least_conflicted_queen[0])
    traversed.append(most_conflicted_queen[0])

    reversed_indexes = reverse_queens_indexes(queens_indexes, most_conflicted_queen, least_conflicted_queen)
    if reversed_indexes in existing_qeen_indexes:
        return False

    if has_conflicts(reversed_indexes):

        return solve(n, reversed_indexes)

    return buld_matrix(n, reversed_indexes)


def n_queens():
    global traversed
    traversed = []
    n = 4

    queens_indexes = initialize_queen_indexes(n)

    if queens_indexes is False:
        return n_queens()

    result = solve(n, queens_indexes)
    if result is False:
        return n_queens()

    if result is not False:
        print(result)


if __name__ == "__main__":
    n_queens()
