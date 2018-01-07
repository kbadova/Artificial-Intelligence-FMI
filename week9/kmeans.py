import argparse
import random
from numpy import mean
import matplotlib.pyplot as plt
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

counter = 0


def plot_kmeans():
    plt.clf()
    for centr in plot:
        centr_points = plot[centr]
        color = centroids_colors[centr]
        centr_coord = eval(centr)

        points_x = [p[0] for p in centr_points]
        points_y = [p[1] for p in centr_points]

        plt.scatter(points_x, points_y, marker=".", color=color, s=30)
        plt.scatter([centr_coord[0]], [centr_coord[1]], marker=".", color="black", s=360)

    global counter
    counter += 1
    plt.xlim(min_point, max_point)
    plt.ylim(min_point, max_point)

    # plt.show()
    plt.savefig("{}.png".format(counter), dpi=300)


def plot_initial_dataset():
    points_x = [p[0] for p in points]
    points_y = [p[1] for p in points]

    plt.scatter(points_x, points_y, marker=".", color="green", s=30)

    global counter
    counter += 1
    plt.xlim(min_point, max_point)
    plt.ylim(min_point, max_point)
    plt.savefig("{}.png".format(counter), dpi=300)  # the dpi setting has to play nicely with the chosen markersizes!


def plot_centroids():
    points_x = [p[0] for p in centroids]
    points_y = [p[1] for p in centroids]

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
    x_diff = centroid[0] - point[0]
    y_diff = centroid[1] - point[1]

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

        points_mean_x = mean([p[0] for p in centr_points])
        points_mean_y = mean([p[1] for p in centr_points])

        new_center = (round(float(points_mean_x), 2), round(float(points_mean_y), 2))

        if str(new_center) == centroid:
            the_same_centroids.append(centroid)
        else:
            old_center_color = centroids_colors[centroid]
            centroids_colors[str(new_center)] = old_center_color
            del centroids_colors[centroid]

        new_plot[str(new_center)] = plot[centroid]
        new_centroids.append(new_center)

    plot = new_plot
    centroids = new_centroids
    print(centroids)
    print(len(centroids))
    # Спирам ако всички центроиди не са се сменили
    return len(the_same_centroids) == k


def solve_kmeans(k):
    global iterations

    if iterations == MAX_ITETATIONS:
        return False

    has_result = False
    while has_result is False:
        attach_points_to_centroids()
        # plot_kmeans()

        has_result = recenter_clusters(k)
        iterations += 1
        print("Iteration")
        print(iterations)
        # plot_kmeans()

        if has_result is True:
            print("FINISH FINISH FINISH FINISH FINISH")
            # plot_kmeans()
            return True
        return solve_kmeans(k)


def kmeans():
    k = arguments.k
    dataset_file = arguments.dataset
    global points

    points = deque()

    with open(dataset_file, 'r') as f:
        lines = f.read().split('\n')
        for line in lines:
            if dataset_file == "unbalance.txt":
                coordinates = line.split(' ')
            else:
                coordinates = line.split('\t')

            point = (eval(coordinates[0]), eval(coordinates[1]))
            points.append(point)

    global min_point, max_point

    min_point = min(points)[0]
    max_point = max(points)[0]

    global MAX_ITETATIONS
    MAX_ITETATIONS = 30

    global iterations
    iterations = 0

    global centroids
    centroids = deque()

    global centroids_colors
    centroids_colors = {}

    global plot
    plot = {}

    # plot_initial_dataset()

    initialize_centroids(k)
    # plot_centroids()

    result = solve_kmeans(k)

    if result is False:
        print("RESTART RESTART RESTART RESTART RESTART")
        return kmeans()
    print("plot here")
    return plot_kmeans()


if __name__ == "__main__":
    kmeans()
