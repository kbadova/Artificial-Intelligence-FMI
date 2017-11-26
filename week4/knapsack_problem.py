import argparse


parser = argparse.ArgumentParser(description='Solving knapsack problem.')
parser.add_argument('-M', type=int, required=True,
                    help='Max number of sack')
parser.add_argument('-N', type=int, required=True,
                    help='Number of items')
parser.add_argument('-items', type=list, required=True,
                    help='Items with weight and price')
arguments = parser.parse_args()


"""

1)  генерирам всички възможни раници, такува че max teglo вътре е < M
2) пресмятам фитнес фунцкията - извежда макс цена от всички items
3) sort по  фитнес фунцкията
3) режа най-слабите 20§
4) кръстосвам останалите докато не получа първоначалния борй в популацията
5) мутирам 5% от децата децата


и това докато не получа 3 еднакви поколения с една  и съша макс цена(финтнес фънк)
"""


def knapsack_problem():
   pass


if __name__ == "__main__":
    knapsack_problem()
