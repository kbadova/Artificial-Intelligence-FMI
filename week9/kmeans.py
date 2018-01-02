import argparse
parser = argparse.ArgumentParser(description='Solving kmenas.')
parser.add_argument('-k', type=int, required=True)
parser.add_argument('-dataset', type=str, required=True)


'''
Steps to reproduce:
1) Set k centroids randomly in the grid
2) Foreach (x, y) point from the dataset:
  - find the nearest centroid of the nearest cluster
  - assign this point to the nearest cluster
3) Foreach cluster, recenter and find the new centroid
4) 2) and 3) until we dont have differences in clusters and centroids
'''

import plotly.plotly as py
import plotly.graph_objs as go

# Create random data with numpy
import numpy as np

N = 100
random_x = np.linspace(0, 1, N)
random_y0 = np.random.randn(N)+5
random_y1 = np.random.randn(N)
random_y2 = np.random.randn(N)-5

# Create traces
trace0 = go.Scatter(
    x = random_x,
    y = random_y0,
    mode = 'markers',
    name = 'markers'
)

data = [trace0]
py.iplot(data, filename='scatter-mode')