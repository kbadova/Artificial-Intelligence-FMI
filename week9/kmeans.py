import argparse
import random
from collections import deque
import plotly.plotly as py
import plotly.graph_objs as go
import numpy as np


parser = argparse.ArgumentParser(description='Solving kmenas.')
parser.add_argument('-k', type=int, required=True)
parser.add_argument('-dataset', type=str, required=True)
arguments = parser.parse_args()


'''
Steps to reproduce:
1) Set k centroids randomly in the grid
2) Foreach (x, y) point from the dataset:
  - find the nearest centroid of the nearest cluster
  - assign this point to the nearest cluster
3) Foreach cluster, recenter and find the new centroid
4) 2) and 3) until we dont have differences in clusters and centroids
'''


points = deque()
centroids = deque()



# Create random data with numpy

N = 100
random_x = np.linspace(0, 1, N)
random_y0 = np.random.randn(N) + 5
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N) - 5

# Create traces
trace0 = go.Scatter(
    x=random_x,
    y=random_y0,
    mode='markers',
    name='markers'
)


def plot_kmeans():
    centroids_x = [c[0] for c in centroids]
    centroids_y = [c[1] for c in centroids]

    points_x = [p[0] for p in points]
    points_y = [p[1] for p in points]

    plot_data = {
        'x': points_x,
        'y': points_y,
        'mode': 'markers',
        'name': 'markers'
    }

    plot = go.Scatter(**plot_data)

    py.iplot([plot], filename='scatter-mode')


def initialize_centroids(k):
    global points
    global centroids

    centroids = random.sample(points, k)
    points_without_centroids = set(points) - set(centroids)
    points = list(points_without_centroids)


def solve_kmeans():
    pass


def kmeans():
    k = arguments.k
    dataset_file = arguments.dataset
    global points

    with open(dataset_file, 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            coordinates = line.split('\t')
            point = (coordinates[0], coordinates[1])
            points.append(point)

    initialize_centroids(k)

    #plot = solve_kmeans()

    plot_kmeans(plot)

if __name__ == "__main__":
    kmeans()
