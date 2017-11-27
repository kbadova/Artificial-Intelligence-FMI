import argparse
import itertools
import random

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
python knapsack_problem.py -M 165 -N 165 -file test_data.txt

    or
python knapsack_problem.py -M 5 -N 3 -items "[(3, 2), (1, 5), (2, 3)]"

1) генерирам всички възможни раници, такива че max тегло вътре е < M
2) пре1смятам фитнес фунцкията - извежда макс цена от всички items
3) sort по  фитнес фунцкията
3) режа най-слабите 20§
4) кръстосвам останалите докато не получа първоначалния брoй в популацията
5) мутирам 5% от децата децата


и това докато не получа 3 еднакви поколения с една  и съша макс цена(финтнес фънк)
"""

# Държи резултатите от фитнес функцията
fitness_values = []
initial_items = []


def take(n, iterable):
    "Return first n items of the iterable as a list"
    return list(itertools.islice(iterable, n))


def get_all_combinations(any_list):
    return itertools.chain.from_iterable(
        itertools.combinations(any_list, i + 1)
        for i in range(len(any_list)))


def calculate_items_weight(sack):
    return sum(int(item[0]) for item in sack)


def calculate_items_price(sack):
    return sum(int(item[1]) for item in sack)


def generate_population(max_weight, items_number, items):
    items_to_select = items_number + round(items_number / 2) - 1
    all_sack_combinations = list(take(items_to_select, get_all_combinations(items)))
    all_sacks = [sack for sack in all_sack_combinations if calculate_items_weight(sack) <= max_weight]

    return all_sacks


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


def generate_child(p1, p2):
    born_child = []
    children_combinations = itertools.combinations(p1 + p2, 2)
    born_child = [child for child in children_combinations if child != p1 and child != p2]

    if len(born_child) == 0:
        return False
    return born_child[0]


# Проверява дали сакът-дете не надминавам максималната допустимост на раницата M
def is_valid_child(child, max_weight, new_generation):
    return calculate_items_weight(child) <= max_weight and child not in new_generation


def crossover_population(best_population, removed_items, max_weight):
    new_generation = []
    new_children_count = 0

    while new_children_count < removed_items:
        parents = random.sample(best_population, 2)
        parent1 = parents[0]
        parent2 = parents[1]

        child = generate_child(parent1, parent2)
        if child is False:
            continue

        if is_valid_child(child, max_weight, new_generation):
            new_children_count += 1
            new_generation.append(child)

    return new_generation + parents


# Взима дете от новото поколение и го swap-ва с randomly избран item от първоначалните items
def mutate_children(new_generation, removed_items):
    mutate_children_count = round(removed_items * 0.05)

    if mutate_children_count == 0:
        return new_generation

    mutate_children = 0
    while mutate_children <= mutate_children_count:
        random_child_to_remove = random.choice(new_generation)
        new_generation.remove(random_child_to_remove)

        random_child_to_append = random.choice(initial_items)
        new_generation.append(random_child_to_append)

        mutate_children += 1

    return new_generation


def check_best_value(best_value):
    return fitness_values.count(best_value) >= 3


def evolution_cycle(max_weight, items_number, population):

    fitness_value = calculate_fitness_func(population)

    global fitness_values
    fitness_values.append(fitness_value)

    print(fitness_value)

    population.sort(key=lambda r: calculate_items_price(r))

    population.reverse()

    # Премахва 20% от сортираната популацията -> т.е. реже 20§ най-евтини раници
    best_population, removed_items = remove_20_percent_of_population(population, items_number)

    # Връща новите деца и  родителите им
    new_generation = crossover_population(best_population, removed_items, max_weight)

    # Връща поколението с мутирани деца, ако можем да мутираме
    generaton_with_mutations = mutate_children(new_generation, removed_items)

    if not check_best_value(fitness_value):
        evolution_cycle(max_weight, items_number, generaton_with_mutations)
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

    global initial_items
    initial_items = items

    population = generate_population(max_weight, items_number, items)
    evolution_cycle(max_weight, items_number, population)


if __name__ == "__main__":
    knapsack_problem()
