import numpy as np
import matplotlib.pyplot as plt
import random
from typing import List

MIN_X = 0
MAX_X = 7
MIN_Y = 0
MAX_Y = 7

# class Polygon:
#     def __init__(self, vertices):
#         self.vertices = []
#         for i in range(len(vertices)):
#             self.vertices.append(Point(vertices[i][0], vertices[i][1]))
#         self.edges = []
#         for i in range(len(self.vertices)):
#             self.edges.append(Edge(self.vertices[i], self.vertices[(i+1)%len(self.vertices)]))
            
#         vert_sort(self.vertices)
#         for v in self.vertices:
#             v.print()
#         for e in self.edges:
#             e.print()
            
#     def get_med(self):
#         median = (self.vertices[len(self.vertices) - 1].y + self.vertices[0].y) / 2.0
#         med_point = self.vertices[0]
#         for v in range(1, len(self.vertices)): 
#             if abs(med_point.y - median) > abs(self.vertices[v].y - median):
#                 med_point = self.vertices[v]
#         return Edge(Point(MIN_X, med_point.y), Point(MAX_X, med_point.y))
    
#     def get_upper_bound(self):
#         return Edge(Point(MIN_X, self.vertices[len(self.vertices) - 1].y), Point(MAX_X, self.vertices[len(self.vertices) - 1].y))
    
#     def get_lower_bound(self):
#         return Edge(Point(MIN_X, self.vertices[0].y), Point(MAX_X, self.vertices[0].y))
    
#     def get_right_bound(self):
#         right_bound = self.vertices[0]
#         for v in range(1, len(self.vertices)): 
#             if v.x >= right_bound.x:
#                 right_bound = v
#         return Edge(Point(right_bound.x, MIN_Y), Point(right_bound.x, MAX_Y))
#     def get_left_bound(self):
#         left_bound = self.vertices[0]
#         for v in range(1, len(self.vertices)): 
#             if v.x < left_bound.x:
#                 left_bound = v
#         return Edge(Point(left_bound.x, MIN_Y), Point(left_bound.x, MAX_Y))
            
                

class Point:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        
    def print(self):
        print("[", self.x, ", ", self.y, "]")
        
    def is_below(self, point):
        if point.y <= self.y:
            return True
        return False
        
class Edge:
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end
        if self.start.y > self.end.y:
            self.start, self.end = self.end, self.start
    
    def print(self):
        print("\n")
        self.start.print()
        print(" -> ")
        self.end.print()
        
    def is_not_above(self, point: Point):
        if point.y <= self.end.y:
            return True
        return False
    def is_not_below(self, point: Point):
        if point.y >= self.start.y:
            return True
        return False
    

class Leaf:
    def __init__(self, left, right, split_edge: Edge) -> None:
        self.left = left
        self.right = right
        self.split_edge = split_edge
    
    def display(self):
        print("LEFT -> ")
        self.left.display()
        print("RIGHT -> ")
        self.right.display()
    
class Root:
    def __init__(self, lower: Leaf, upper: Leaf) -> None:
        self.lower = lower
        self.upper = upper
        
    def display(self):
        print("LOWER -> ")
        self.lower.display()
        print("UPPER -> ")
        self.upper.display()

class Tree:
    def __init__(self, root: Root) -> None:
        self.root = root
    
    def display(self):
        print("ROOT -> ")
        self.root.display()

class Trapezoid:
    def __init__(self, edges: List[Edge]) -> None:
        self.edges = edges
    
    def display(self):
        print("TRAPEZOID : ")
        for e in self.edges:
            e.print()      
       
def get_med(vertices):
        median = (vertices[len(vertices) - 1].y + vertices[0].y) / 2.0
        med_point = vertices[0]
        for v in range(1, len(vertices)): 
            if abs(med_point.y - median) > abs(vertices[v].y - median):
                med_point = vertices[v]
        return Edge(Point(MIN_X, med_point.y), Point(MAX_X, med_point.y)) 
    
def get_upper_edge(vertices: List[Point]):
    return Edge(Point(MIN_X, vertices[len(vertices)-1].y), Point(MAX_X, vertices[len(vertices)-1].y))

def get_lower_edge(vertices: List[Point]):
    return Edge(Point(MIN_X, vertices[0].y), Point(MAX_X, vertices[0].y))
    
def get_right_edge(vertices: List[Point]):
    right_bound = vertices[0]
    for v in vertices: 
        if v.x >= right_bound.x:
            right_bound = v
    return Edge(Point(right_bound.x, MIN_Y), Point(right_bound.x, MAX_Y))
def get_left_edge(vertices: List[Point]):
    left_bound = vertices[0]
    for v in vertices: 
        if v.x < left_bound.x:
            left_bound = v
    return Edge(Point(left_bound.x, MIN_Y), Point(left_bound.x, MAX_Y))
# def decompose(polygon: Polygon):
#     upper_edge = polygon.get_upper_bound()
#     lower_edge = polygon.get_lower_bound()
#     right_edge = polygon.get_right_bound()
#     left_edge = polygon.get_left_bound()
#     root = Root(polygon.get_med(), )
#     return Tree(root)

# def decompose_trapezoids(polygon):
#     return Leaf()

def decompose_root(edges: List[Edge], vertices: List[Point], lower_edge: Edge, upper_edge: Edge, right_edge: Edge, left_edge: Edge):
    med = get_med(vertices)
    lower = []
    upper = []
    lower_v = []
    upper_v = []
    for e in edges:
        if e.is_not_above(med.start):
            lower.append(e)
        if e.is_not_below(med.start):
            upper.append(e)
    for v in vertices:
        if v.is_below(med.start):
            lower_v.append(v)
        else:
            upper_v.append(v)
    print("MED")
    med.print()
    return Root(decompose_leaves(lower, lower_v, lower_edge, med, right_edge, left_edge), decompose_leaves(upper, upper_v, med, upper_edge, right_edge, left_edge))

def decompose_leaves(edges: List[Edge], vertices: List[Point], lower_edge: Edge, upper_edge: Edge, right_edge: Edge, left_edge: Edge):
    split_edge = None
    inner_point = False
    for e in edges:
        if e.is_not_above(lower_edge.start) and e.is_not_below(upper_edge.start):
            split_edge = e
            break
        if e.is_not_below(lower_edge.start) or e.is_not_above(upper_edge.start):
            print("FUCKER")
            e.print()
            inner_point = True
    if split_edge == None:
        if(inner_point == False):
            return Trapezoid(edges)
        else:
            return decompose_root(edges, vertices, lower_edge, upper_edge, right_edge, left_edge)
    print("SPLIT")
    split_edge.print()
    right_edges = []
    left_edges = []
    for e in edges:
        if e.start.x < split_edge.start.x or e.start.x < split_edge.end.x or e.end.x < split_edge.start.x or e.end.x < split_edge.end.x:
            right_edges.append(e)
        if e.start.x > split_edge.start.x or e.start.x > split_edge.end.x or e.end.x > split_edge.start.x or e.end.x > split_edge.end.x:
            left_edges.append(e)
    return Leaf(decompose_leaves(right_edges, vertices, lower_edge, upper_edge, split_edge, left_edge), decompose_leaves(left_edges, vertices, lower_edge, upper_edge, right_edge, split_edge))
    
def plot_plane(vertices, points):
    x = [v.x for v in vertices]
    y = [v.y for v in vertices]
    plt.plot(x + [x[0]], y + [y[0]], 'b-') 
    # for diag in diags:
    #     plt.plot([diag[0][0], diag[1][0]], [diag[0][1], diag[1][1]], 'b-')
    # patches = []
    # poly = rect
    # polygon = Polygon(poly, closed=True, edgecolor='black', facecolor='none')
    # patches.append(polygon)
    # fig, ax = plt.subplots()
    # p = PatchCollection(patches, match_original=True)
    # ax.add_collection(p)
    # ax.autoscale_view()
    # ax.set_aspect('equal', adjustable='box')
    for point in points:
        plt.scatter(point[0], point[1], color="red", label="Point")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Polygon with Diagonals')
    plt.grid(True)
    plt.axis('equal')
    plt.show()

def vert_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j].y > key.y:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    
        

vertices = [Point(0, 0), Point(0.5, 1), Point(1, 1.5), Point(2, 2), Point(2.5, 0.8), Point(3.2, 0.2)]
edges = [Edge(vertices[0], vertices[1]), Edge(vertices[1], vertices[2]), Edge(vertices[2], vertices[3]), Edge(vertices[3], vertices[4]), Edge(vertices[4], vertices[5]), Edge(vertices[5], vertices[1])]

# rect = [(0, 0), (0.5, 1), (1, 1.5), (2, 2), (2.5, 0.8), (3.2, 0.2)]
# diags = [(rect[0], rect[3])]
points = []
for i in range(5):
    point = np.array([random.uniform(0, 6), random.uniform(0,3)])  # Point to test
    points.append(point)
plot_plane(vertices, points)
vert_sort(vertices)
tree = Tree(decompose_root(edges, vertices, get_lower_edge(vertices), get_upper_edge(vertices), get_right_edge(vertices), get_left_edge(vertices)))
tree.display()
# polygon = Polygon(rect)
# polygon.get_med().print()