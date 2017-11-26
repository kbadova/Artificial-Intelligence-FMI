import argparse
import itertools

# Example input: python knapsack_problem.py -M 5 -N 3 -items "[(3, 2), (1, 5), (2, 3)]"

parser = argparse.ArgumentParser(description='Solving knapsack problem.')
parser.add_argument('-M', type=int, required=True,
                    help='Max number of sack')
parser.add_argument('-N', type=int, required=True,
                    help='Number of items')
parser.add_argument('-items', required=True,
                    help='Items in format  weight and price -> (m=3, c=5)')
arguments = parser.parse_args()


"""

1)  генерирам всички възможни раници, такива че max тегло вътре е < M
2) пресмятам фитнес фунцкията - извежда макс цена от всички items
3) sort по  фитнес фунцкията
3) режа най-слабите 20§
4) кръстосвам останалите докато не получа първоначалния борй в популацията
5) мутирам 5% от децата децата


и това докато не получа 3 еднакви поколения с една  и съша макс цена(финтнес фънк)
"""


def get_all_combinations(any_list):
    return itertools.chain.from_iterable(
        itertools.combinations(any_list, i + 1)
        for i in range(len(any_list)))


def calculate_items_sum(sack):
    return sum(item[0] for item in sack)


def calculate_items_price(sack):
    return sum(item[1] for item in sack)


def generate_population(max_weight, items_number, items):
    all_sack_combinations = list(get_all_combinations(items))
    all_sacks = [sack for sack in all_sack_combinations if calculate_items_sum(sack) <= max_weight]
    return all_sacks


def calculate_fitness_func(population):
    max_value = 0
    for sack in population:
        price_of_sack = calculate_items_price(sack)
        if price_of_sack > max_value:
            max_value = price_of_sack

    return max_value


def evolution_cycle(max_weight, items_number, items):
    population = generate_population(max_weight, items_number, items)

    fitness_value = calculate_fitness_func(population)
    
    population.sort(key=lambda r: calculate_items_price(r))
    sorted_population = population.reverse()


def knapsack_problem():
   max_weight = arguments.M
   items_number = arguments.N
   items = eval(arguments.items)

   evolution_cycle(max_weight, items_number, items)


if __name__ == "__main__":
    knapsack_problem()
