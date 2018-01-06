import argparse
import random
import matplotlib.pyplot as plt
from copy import deepcopy
from collections import deque

plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')

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

counter = 0
centroids_colors = {}


def plot_kmeans():
    plt.clf()
    for centr in plot:
        centr_points = plot[centr]
        color = centroids_colors[centr]
        centr_coord = eval(centr)

        points_x = [eval(p[0]) for p in centr_points]
        points_y = [eval(p[1]) for p in centr_points]

        plt.scatter(points_x, points_y, marker=".", color=color, s=30)
        plt.scatter([eval(centr_coord[0])], [eval(centr_coord[1])], marker=".", color="black", s=360)

    global counter
    counter += 1
    print(counter)
    plt.xlim(min_point, max_point)
    plt.ylim(min_point, max_point)

    # plt.show()
    plt.savefig("{}.png".format(counter), dpi=300)


def plot_initial_dataset():
    points_x = [eval(p[0]) for p in points]
    points_y = [eval(p[1]) for p in points]

    plt.scatter(points_x, points_y, marker=".", color="green", s=30)

    global counter
    counter += 1
    plt.xlim(min_point, max_point)
    plt.ylim(min_point, max_point)
    plt.savefig("{}.png".format(counter), dpi=300)  # the dpi setting has to play nicely with the chosen markersizes!


def plot_centroids():
    points_x = [eval(p[0]) for p in centroids]
    points_y = [eval(p[1]) for p in centroids]

    plt.scatter(points_x, points_y, marker=".", color="black", s=360)

    global counter
    counter += 1
    plt.xlim(min_point, max_point)
    plt.ylim(min_point, max_point)
    plt.savefig("{}.png".format(counter), dpi=300)


def initialize_centroids(k):
    global plot
    global points
    global centroids
    global centroids_colors

    colors = ['pink', 'red', 'green', 'blue', 'orange']

    centroids = random.sample(points, k)
    points_without_centroids = set(points) - set(centroids)
    points = list(points_without_centroids)

    for centr in centroids:
        color = random.sample(colors, 1)[0]
        colors.remove(color)
        centroids_colors[str(centr)] = color


def calculate_distance_to_centroid(point, centroid):
    '''
     Distance = sqrt(pow(x2−x1, 2)+ pow(y2−y1, 2))
    '''
    x_diff = eval(centroid[0]) - eval(point[0])
    y_diff = eval(centroid[1]) - eval(point[1])

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
    global plot
    global centroids
    new_plot = {}
    new_centroids = deque()
    the_same_centroids = deque()

    for centroid in plot:
        centr_points = plot[centroid] + [eval(centroid)]
        number_of_points = len(centr_points)

        points_mean_x = sum([eval(p[0]) for p in centr_points]) / number_of_points
        points_mean_y = sum([eval(p[1]) for p in centr_points]) / number_of_points

        new_center = (str(round(points_mean_x, 2)), str(round(points_mean_y, 2)))

        if str(new_center) == centroid:
            print("the same centroid")
            the_same_centroids.append(centroid)
        else:
            old_center_color = centroids_colors[centroid]
            centroids_colors[str(new_center)] = old_center_color
            del centroids_colors[centroid]

        new_plot[str(new_center)] = plot[centroid]
        new_centroids.append(new_center)

    plot = deepcopy(new_plot)
    centroids = new_centroids

    # Спирам ако всички центроиди не са се сменили
    return len(the_same_centroids) == k


def solve_kmeans(k):
    has_result = False
    while has_result is False:
        attach_points_to_centroids()
        plot_kmeans()

        has_result = recenter_clusters(k)
        plot_kmeans()

        if has_result is True:
            print("finish")
            return
        return solve_kmeans(k)


def kmeans():
    k = arguments.k
    dataset_file = arguments.dataset
    global points

    with open(dataset_file, 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            if dataset_file == "unbalance.txt":
                coordinates = line.split(' ')
            else:
                coordinates = line.split('\t')

            point = (coordinates[0], coordinates[1])
            points.append(point)

    global min_point, max_point

    min_point = eval(min(points)[0])
    max_point = eval(max(points)[0])

    plot_initial_dataset()

    initialize_centroids(k)
    plot_centroids()

    solve_kmeans(k)


if __name__ == "__main__":
    kmeans()
