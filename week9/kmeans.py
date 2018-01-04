import argparse
import random
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


points = deque()
centroids = deque()
# Stores for each centroid his points
plot = {}

counter = 0
centroids_colors = {}


def plot_kmeans():
    # fig = plt.figure()
    # ax1 = fig.add_subplot(111)
    # for tick in ax1.xaxis.get_major_ticks():
    #     tick.label.set_fontsize(3)
    #     tick.label.set_rotation('vertical')

    # for tick in ax1.yaxis.get_major_ticks():
    #     tick.label.set_fontsize(3)

    for centr in plot:
        centr_points = plot[centr]
        color = centroids_colors[centr]
        centr_coord = eval(centr)

        points_x = [p[0] for p in centr_points]
        points_y = [p[1] for p in centr_points]

        plt.scatter(points_x, points_y, marker=".", color=color, s=30)
        plt.scatter([centr_coord[0]], centr_coord[1], marker=".", color=color, s=360)

    global counter
    counter += 1
    # plt.xlim(0, 5)
    # plt.ylim(0, 5)
    plt.savefig("{}.png".format(counter), dpi=300)  # the dpi setting has to play nicely with the chosen markersizes!


def initialize_centroids(k):
    global points
    global centroids
    global centroids_colors

    colors = ['yellow', 'red', 'green', 'blue', 'orange']

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
    global plot
    global centroids
    new_plot = {}
    new_centroids = deque()
    the_same_centroids = deque()

    for centroid in plot:
        centr_points = plot[centroid] + [eval(centroid)]
        number_of_points = len(centr_points)
        points_mean_x = sum([float(p[0]) for p in centr_points]) / number_of_points
        points_mean_y = sum([float(p[1]) for p in centr_points]) / number_of_points
        new_center = (round(points_mean_x, 2), round(points_mean_y, 2))

        if str(new_center) == centroid:
            print("here")
            the_same_centroids.append(centroid)
        else:
            new_plot[str(new_center)] = plot[centroid]

            old_center_color = centroids_colors[centroid]
            centroids_colors[str(new_center)] = old_center_color
            del centroids_colors[centroid]

        new_centroids.append(new_center)

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
            return
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


if __name__ == "__main__":
    kmeans()


# # https://plot.ly/~badovakrasi/35/markers/#plot
