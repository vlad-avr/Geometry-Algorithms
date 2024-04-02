import numpy as np
import matplotlib.pyplot as plt
import random

# def plot_subdivision(subdivision, points):
#     patches = []
#     poly = subdivision
#     polygon = Polygon(poly, closed=True, edgecolor='black', facecolor='none')
#     patches.append(polygon)
#     fig, ax = plt.subplots()
#     p = PatchCollection(patches, match_original=True)
#     ax.add_collection(p)
#     ax.autoscale_view()
#     ax.set_aspect('equal', adjustable='box')
#     for point in points:
#         plt.scatter(point[0], point[1], color="red", label="Point")
#     plt.gca().set_aspect('equal', adjustable='box')
#     plt.show()

# def check_all_points(points, subdivision):
#     for point in points:
#         if trapezoidal_decomposition(subdivision, point):
#             print("The point [" , point[0] , " , " , point[1] , "] is inside the subdivision.")
#         else:
#             print("The point [" , point[0] , " , " , point[1] , "] is outside the subdivision.")

# class Trapezoid:
#     def __init__(self, top_left, top_right, bottom_left, bottom_right):
#         self.top_left = top_left
#         self.top_right = top_right
#         self.bottom_left = bottom_left
#         self.bottom_right = bottom_right

# def trapezoidal_decomposition(subdivision, query_point):
#     # Perform simple linear search through trapezoids
#     for trapezoid in subdivision:
#         if (query_point[0] >= trapezoid.bottom_left[0] and
#             query_point[0] <= trapezoid.bottom_right[0] and
#             query_point[1] >= trapezoid.bottom_left[1] and
#             query_point[1] <= trapezoid.top_left[1]):
#             return trapezoid
#     return None

# # Example input: a simple subdivision with two trapezoids
# subdivision = [(0, 1), (3, 2), (1, 0), (2, 0), (1.5, 0.5), (3.5, 3)]

# points = []
# for i in range(10):
#     point = np.array([random.uniform(0, 6), random.uniform(0,3)])  # Point to test
#     points.append(point)

# # Plot the subdivision
# plot_subdivision(subdivision, points)
# check_all_points(points, subdivision)

def plot_plane(vertices, diags, points):
    x = [v[0] for v in vertices]
    y = [v[1] for v in vertices]
    plt.plot(x + [x[0]], y + [y[0]], 'b-') 
    for diag in diags:
        plt.plot([diag[0][0], diag[1][0]], [diag[0][1], diag[1][1]], 'b-')
    # patches = []
    # poly = rect
    # polygon = Polygon(poly, closed=True, edgecolor='black', facecolor='none')
    # patches.append(polygon)
    # fig, ax = plt.subplots()
    # p = PatchCollection(patches, match_original=True)
    # ax.add_collection(p)
    # ax.autoscale_view()
    # ax.set_aspect('equal', adjustable='box')
    # for point in points:
    #     plt.scatter(point[0], point[1], color="red", label="Point")
    # plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Polygon with Diagonals')
    plt.grid(True)
    plt.axis('equal')
    plt.show()
    

    
rect = [(0, 0), (0.5, 0.8), (1, 1.5), (2, 2), (2.5, 0.8), (3.2, 0.2)]
diags = [(rect[0], rect[3])]
points = []
for i in range(5):
    point = np.array([random.uniform(0, 6), random.uniform(0,3)])  # Point to test
    points.append(point)
plot_plane(rect, diags, points)