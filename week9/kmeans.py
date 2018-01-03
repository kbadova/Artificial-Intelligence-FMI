import argparse
import random
import datetime
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
# Stores for each centroid his points
plot = {}

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
    colors = ['black', 'red', 'green', 'blue']
    plot_data = {}
    plots = []
    for centr in plot:

        centr_points = plot[centr]
        points_x = [p[0] for p in centr_points]
        points_y = [p[1] for p in centr_points]
        color = random.sample(colors, 1)[0]
        plot_data = {
            'x': points_x,
            'y': points_y,
            'mode': 'markers',
            'name': 'markers',
            'marker': dict(size=3, color=color)
        }
        colors.remove(color)

        centr = eval(centr)

        center_data = {
            'x': [centr[0]],
            'y': [centr[1]],
            'mode': 'markers',
            'name': 'markers',
            'marker': dict(size=3, color='white')
        }
        plots_scatter = go.Scatter(**plot_data)
        center_scatter = go.Scatter(**center_data)
        plots += [plots_scatter]
        plots += [center_scatter]

    py.iplot(plots, filename='{}'.format(str(datetime.datetime.now().date())))


def initialize_centroids(k):
    global centroids

    min_x_point = min(p[0] for p in points)
    max_x_point = max(p[0] for p in points)

    min_y_point = min(p[1] for p in points)
    max_y_point = max(p[1] for p in points)

    for i in range(k):
        centroid_x = random.uniform(float(min_x_point), float(max_x_point))
        centroid_y = random.uniform(float(min_y_point), float(max_y_point))

        centroids.append((round(centroid_x, 2), round(centroid_y, 2)))


def calculate_distance_to_centroid(point, centroid):
    '''
     Distance = sqrt(pow(x2−x1, 2)+ pow(y2−y1, 2))
    '''
    x_diff = float(centroid[0]) - float(point[0])
    y_diff = float(centroid[1]) - float(point[1])

    return (pow(x_diff, 2) + pow(y_diff, 2))**(1 / 2)


def get_smallest_distance_from_point_to_centroid(point):
    cetroids_distances = []
    for centroid in centroids:
        distance_to_centroid = calculate_distance_to_centroid(point, centroid)
        cetroids_distances.append((centroid, distance_to_centroid))

    return min(cetroids_distances, key=lambda c: c[1])


def attach_points_to_centroids():
    global plot

    for point in points:
        centroid, _ = get_smallest_distance_from_point_to_centroid(point)
        if str(centroid) not in plot:
            plot[str(centroid)] = [point]
        else:

            plot[str(centroid)] += [point]

    return plot


def recenter_clusters(k):
    the_same_centroids = []

    new_plot = {}
    new_centroids = deque()
    for centroid in plot:
        centr_points = plot[centroid]
        number_of_points = len(centr_points)
        points_mean_x = sum([float(p[0]) for p in centr_points]) / number_of_points
        points_mean_y = sum([float(p[1]) for p in centr_points]) / number_of_points
        new_center = (round(points_mean_x, 2), round(points_mean_y, 2))

        if str(new_center) == centroid:
            print("here")
            the_same_centroids.append(centroid)
        else:
            new_plot[str(new_center)] = centr_points

        new_centroids.append(new_center)

    global plot
    global centroids
    plot = new_plot
    centroids = new_centroids

    return len(the_same_centroids) == k


def solve_kmeans(k):
    has_result = False
    while has_result is False:
        attach_points_to_centroids()
        has_result = recenter_clusters(k)

        plot_kmeans()

        if has_result is True:
            print("finish")
            print("centroids")
            print(centroids)
            break
        print("centroids")
        print(centroids)
        return solve_kmeans(k)


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

    solve_kmeans(k)

    # plot_kmeans()


if __name__ == "__main__":
    kmeans()


# https://plot.ly/~badovakrasi/35/markers/#plot