import random
import argparse
from copy import copy
from collections import deque

from ..tail_recursion.recursive_decorator import tail_call_optimized
parser = argparse.ArgumentParser(description='Solving n queens.')
parser.add_argument('-n', type=int, required=True,
                    help='Number of queens')
arguments = parser.parse_args()


'''
1) initialize_matrix_with_queens
    queen_indexes_per_row = [0, 3, 1, 2]
    matrrix = [['*', '_', '_', '_'],
               ['_', '_', '_', '*'],
               ['_', '*', '_', '_'],
               ['_', '_', '*, '_']]

2) calculate_conflicts
     връща списък с координматите на дадена матрица и колко конфликта има тя -> [((1,2), 3), ((0,3), 2), ((2,1), 1)]

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


expected queens_indexes for n = 4: [(0,1),(1,3),(2,0),(3,2)]
expected queens_indexes for n = 5: [(0,1),(1,3),(2,0),(3,2),(4,4)]
expected queens_indexes for n = 6: [(1, 2), (0, 4), (2, 0), (3, 5), (4, 3), (5, 1)],
                                   [(0, 1), (1, 3), (2, 5), (3, 0), (5, 4), (4, 2)],
                                   [(4, 5), (1, 0), (2, 4), (3, 1), (0, 3), (5, 2)],
                                   [(0, 4), (1, 2), (2, 0), (4, 3), (3, 5), (5, 1)]

'''


# Списък със съществуващи индекси
existing_qeen_indexes = deque()

# Списък с обходените елементи от текущия списък с индекси
traversed = deque()


def get_queens_indexes(queens_list, n):
    queens_indexes = deque()
    for i in range(n):
        queens_indexes.append((i, queens_list[i]))
    return queens_indexes


def initialize_queen_indexes(n):
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

    queens_indexes = get_queens_indexes(queen_indexes_per_row, n)

    # [(1, 1), (2, 2), (3, 0)], [1, 2, 0]
    return queens_indexes, queen_indexes_per_row


def get_most_and_least_conflicted_queens(n, indexes_with_conflicts):
    # Ако всички матрици имат равен брой конфликти, избираме на random някоя, която не е обходена
    if set([couple[1] for couple in indexes_with_conflicts]) == set([indexes_with_conflicts[0][1]]):
        not_traversed_indexes_with_conflicts = [q for q in indexes_with_conflicts if q[0] not in traversed]
        not_traversed_len = len(not_traversed_indexes_with_conflicts)
        if not_traversed_len == 0 or not_traversed_len == 1:
            return None, None
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


def reverse_queens_indexes(queens_indexes, indexes_list, most_conflicted_queen, least_conflicted_queen):
    reversed_indexes = copy(indexes_list)

    for i in range(len(queens_indexes)):
        if queens_indexes[i] == most_conflicted_queen[0]:
            reversed_indexes[i] = least_conflicted_queen[0][1]

        if queens_indexes[i] == least_conflicted_queen[0]:
            reversed_indexes[i] = most_conflicted_queen[0][1]

    return reversed_indexes


def has_conflicts(reversed_indexes):
    indexes_with_conflicts = calculate_conflicts(reversed_indexes)
    # indexes_with_conflicts e [[((1, 1), 1), ((0, 0), 1), ((2, 3), 1), ((3, 2), 1)]
    # Ако сумата от конфликтите е 0, значи няма конфликти

    return sum([queen_indexes[1] for queen_indexes in indexes_with_conflicts]) != 0


def calculate_conflicts(queens_indexes):
    indexes_with_conflicts = deque()

    for queen in queens_indexes:
        conflicts = 0
        list_with_queens_indexes = copy(queens_indexes)
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


def build_matrix(n, reversed_queens, has_still_conflicts):
    matrix = deque()
    for i in range(n):
        col = ['_'] * n
        el = [ind for ind in reversed_queens if ind[1] == i][0]
        col[el[0]] = "*"
        matrix.append(col)

    for col in matrix:
        print(",".join(str(x) for x in col))

    print(matrix)
    print("--------------------------------")


def solve(n, queens_indexes, indexes_list):
    # Aко сме обходили всички царици и не сме намирили решение, return False и рекурсивно викам пак n_queens
    if set(queens_indexes) == set(traversed):
        return False

    indexes_with_conflicts = calculate_conflicts(queens_indexes)

    most_and_least_conflicted_queens = get_most_and_least_conflicted_queens(n, indexes_with_conflicts)
    least_conflicted_queen = most_and_least_conflicted_queens[0]
    most_conflicted_queen = most_and_least_conflicted_queens[1]

    if most_conflicted_queen is None or least_conflicted_queen is None:
        return False

    traversed.append(least_conflicted_queen[0])
    traversed.append(most_conflicted_queen[0])

    reversed_indexes = reverse_queens_indexes(
        queens_indexes,
        indexes_list,
        most_conflicted_queen,
        least_conflicted_queen)

    reversed_queens = get_queens_indexes(reversed_indexes, n)
    if reversed_queens in existing_qeen_indexes:
        return False

    has_still_conflicts = has_conflicts(reversed_queens)

    if has_still_conflicts is True:
        return solve(n, reversed_queens, reversed_indexes)

    print("FOUNDDDDDDDDDDDDddddddddddddddddddddddd")
    return build_matrix(n, reversed_queens, has_still_conflicts)


@tail_call_optimized
def n_queens():
    global traversed
    traversed = deque()
    n = arguments.n

    queens_indexes, indexes_list = initialize_queen_indexes(n)

    if queens_indexes is False:
        return n_queens()

    result = solve(n, queens_indexes, indexes_list)
    if result is False:
        return n_queens()


if __name__ == "__main__":
    n_queens()


