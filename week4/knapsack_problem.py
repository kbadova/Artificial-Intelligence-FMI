import argparse
import itertools
import random
from recursive_decorator import tail_call_optimized
from copy import deepcopy
parser = argparse.ArgumentParser(description='Solving knapsack problem.')
parser.add_argument('-M', type=int, required=True,
                    help='Max number of sack')
parser.add_argument('-N', type=int, required=True,
                    help='Number of items')
parser.add_argument('-items',
                    help='Items in format  weight and price -> (m=3, c=5)')
parser.add_argument('-file',
                    help='Items in format  weight and price -> (m=3, c=5)')
arguments = parser.parse_args()


"""
Example Input:
python knapsack_problem.py -M 5000 -N 201 -file test_data.txt
python knapsack_problem.py -M 165 -N 165 -file test_data2.txt

    or
python knapsack_problem.py -M 5 -N 3 -items "[(3, 2), (1, 5), (2, 3)]"

1) генерирам всички възможни раници, такива че max тегло вътре е < M
2) пресмятам фитнес фунцкията - извежда макс цена от всички items
3) sort по  фитнес фунцкията
3) режа най-слабите 20%
4) кръстосвам останалите докато не получа първоначалния брoй в популацията
5) мутирам 5% от децата децата


и това докато не получа 3 еднакви поколения с една  и съща макс цена(финтнес фънк)
"""

# Държи резултатите от фитнес функцията
fitness_values = []
initial_items = []


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))


def calculate_items_weight(sack):
    return sum(int(item[0]) for item in sack)


def calculate_items_price(sack):
    return sum(int(item[1]) for item in sack)


def calculate_fitness_func(population):
    max_value = 0

    for sack in population:
        price_of_sack = calculate_items_price(sack)
        if price_of_sack > max_value:
            max_value = price_of_sack

    return max_value


def remove_20_percent_of_population(sorted_population, items_number):
    # Пресмята броя раници (20% от общия брой), които трябва да махна
    items_number_to_remove = round(items_number * 0.2)
    return sorted_population[0: items_number - items_number_to_remove], items_number_to_remove


def generate_child(p1, p2, best_population):
    born_child = []
    children_combinations = itertools.combinations(set(p1 + p2), 2)

    born_child = [child for child in children_combinations if child != p1[0] and child != p2[0] and child not in best_population]
    if len(born_child) == 0:
        return []
    return born_child[0]


# Проверява дали сакът-дете не надминавам максималната допустимост на раницата M
def is_valid_child(child, max_weight, best_population):
    return calculate_items_weight(child) <= max_weight and child not in best_population


def select_non_existing_item_in_sack(new_generation):
    separate_items = [t[0] for t in initial_items]
    for i in range(len(separate_items)):
        if separate_items[i] not in [s[0] for s in new_generation] + [s[1] for s in new_generation if len(s) > 1]:
            return (separate_items[i], )

    return random.choice(initial_items)


def crossover_population(best_population, removed_items_count):
    new_children = []
    asd = deepcopy(best_population)
    while removed_items_count > 0 and len(asd) > 1:
        parents = random.sample(asd, 2)
        parent1 = parents[0]
        parent2 = parents[1]
        child = generate_child(parent1, parent2, asd)

        asd.remove(parent1)
        asd.remove(parent2)

        removed_items_count -= 1

        new_children.append(child)

    return new_children


# Взима дете от новото поколение и го swap-ва с randomly избран item от първоначалните items
def mutate_children(best_population, children, removed_items_count):
    mutate_children_count = round(removed_items_count * 0.05)

    while mutate_children_count > 0 and len(children) > 1:

        random_child_to_remove = random.choice(children)
        children.remove(random_child_to_remove)

        random_child_to_append = random.choice(initial_items)
        children.append(random_child_to_append)

        mutate_children_count -= 1

    return children


def check_best_value(best_value):
    best_value_counts = len(fitness_values)
    if best_value_counts >= 3:
        last_3_values = fitness_values[best_value_counts - 3:best_value_counts]
        return len(set(last_3_values)) == 1
    return False


@tail_call_optimized
def evolution_cycle(max_weight, items_number, population):
    fitness_value = calculate_fitness_func(population)

    global fitness_values
    fitness_values.append(fitness_value)

    print(fitness_value)

    population.sort(key=lambda r: calculate_items_price(r))

    population.reverse()

    # Махам 20% които са най-евтини
    best_population, removed_items_count = remove_20_percent_of_population(population, items_number)

    # Връща новите деца
    children = crossover_population(best_population, removed_items_count)

    # Връща поколението с мутирани деца, ако можем да мутираме
    mutated_children = mutate_children(best_population, children, removed_items_count)

    new_population = mutated_children + best_population

    if not check_best_value(fitness_value):
        return evolution_cycle(max_weight, items_number, new_population)
    return fitness_value


def knapsack_problem():
    max_weight = arguments.M
    if arguments.items:

        items_number = arguments.N
        items = eval(arguments.items)
    else:
        file = arguments.file
        items = []
        with open(file, 'r') as f:
            data = f.read().split('\n')
            for el in data:
                line = el.split(' ')
                item = (line[0], line[1])
                items.append(item)

        items_number = len(items)

    items = [(item, ) for item in items]
    global initial_items
    initial_items = items

    evolution_cycle(max_weight, items_number, items)


if __name__ == "__main__":
    knapsack_problem()
