import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import random

def plot_subdivision(subdivision, points):
    patches = []
    for poly in subdivision:
        polygon = Polygon(poly, closed=True, edgecolor='black', facecolor='none')
        patches.append(polygon)
    fig, ax = plt.subplots()
    p = PatchCollection(patches, match_original=True)
    ax.add_collection(p)
    ax.autoscale_view()
    ax.set_aspect('equal', adjustable='box')
    for point in points:
        plt.scatter(point[0], point[1], color="red", label="Point")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()

def trapezoidal_decomposition(subdivision, point):
    for poly in subdivision:
        vertices = np.array(poly)
        v0, v1, v2 = vertices
        b0 = np.cross(v1 - v0, point - v0) >= 0
        b1 = np.cross(v2 - v1, point - v1) >= 0
        b2 = np.cross(v0 - v2, point - v2) >= 0
        if b0 and b1 and b2:
            return True
    return False

def check_all_points(points, subdivision):
    for point in points:
        if trapezoidal_decomposition(subdivision, point):
            print("The point [" , point[0] , " , " , point[1] , "] is inside the subdivision.")
        else:
            print("The point [" , point[0] , " , " , point[1] , "] is outside the subdivision.")






# Example input: a simple subdivision with two triangles
subdivision = [[[0, 0], [1, 1], [2, 0]], [[1, 1], [2, 2], [2, 0]]]
points = []
for i in range(10):
    point = np.array([random.uniform(0, 3), random.uniform(0,3)])  # Point to test
    points.append(point)

# Plot the subdivision
plot_subdivision(subdivision, points)
check_all_points(points, subdivision)