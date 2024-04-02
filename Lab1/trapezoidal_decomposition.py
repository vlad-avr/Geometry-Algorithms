import numpy as np
import matplotlib.pyplot as plt
import random
from typing import List

MIN_X = 0
MAX_X = 7
MIN_Y = 0
MAX_Y = 7
      

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
        
    # def starts_below(self, point: Point):
    #     if point.y >= self.start.y:
    #         return True
    #     return False
    # def ends_above(self, point: Point):
    #     if point.y <= self.end.y:
    #         return True
    #     return False
    

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
        plt.show()

class Trapezoid:
    def __init__(self, edges: List[Edge]) -> None:
        self.edges = edges
    
    def display(self):
        print("\nTRAPEZOID")
        for e in self.edges:
            e.print()
        plot_trapezoid(self.edges)
        #plt.show()
       
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


def decompose_root(edges: List[Edge], vertices: List[Point], lower_edge: Edge, upper_edge: Edge, right_edge: Edge, left_edge: Edge):
    med = get_med(vertices)
    lower = []
    upper = []
    lower_v = []
    upper_v = []
    for e in edges:
        if e.start.y < med.start.y:
            lower.append(e)
        if e.end.y > med.start.y:
            upper.append(e)
    for v in vertices:
        if v.is_below(med.start):
            lower_v.append(v)
        else:
            upper_v.append(v)
    return Root(decompose_leaves(lower, lower_v, lower_edge, med, right_edge, left_edge), decompose_leaves(upper, upper_v, med, upper_edge, right_edge, left_edge))

def decompose_leaves(edges: List[Edge], vertices: List[Point], lower_edge: Edge, upper_edge: Edge, right_edge: Edge, left_edge: Edge):
    split_edge = None
    inner_point = False
    for e in edges:
        if e.start.y <= lower_edge.start.y and e.end.y >= upper_edge.start.y:
            split_edge = e
            break
        if ((e.start.y > lower_edge.start.y and e.start.y < upper_edge.start.y) or (e.end.y > lower_edge.start.y and e.end.y < upper_edge.start.y)):
            inner_point = True
    if split_edge == None:
        if(inner_point == False):
            return Trapezoid([lower_edge, left_edge, upper_edge, right_edge])
        else:
            return decompose_root(edges, vertices, lower_edge, upper_edge, right_edge, left_edge)
    right_edges = []
    right_verts = []
    left_edges = []
    left_verts = []
    for e in edges:
        if e == split_edge:
            continue
        if e.start.x < split_edge.start.x or e.start.x < split_edge.end.x or e.end.x < split_edge.start.x or e.end.x < split_edge.end.x:
            left_edges.append(e)
            if(e.start.y >= lower_edge.start.y and e.start.y <= upper_edge.start.y and not right_verts.__contains__(e.start)):
                left_verts.append(e.start)
            if(e.end.y >= lower_edge.start.y and e.end.y <= upper_edge.start.y and not right_verts.__contains__(e.end)):
                left_verts.append(e.end)
        if e.start.x > split_edge.start.x or e.start.x > split_edge.end.x or e.end.x > split_edge.start.x or e.end.x > split_edge.end.x:
            right_edges.append(e)
            if(e.start.y >= lower_edge.start.y and e.start.y <= upper_edge.start.y and not right_verts.__contains__(e.start)):
                right_verts.append(e.start)
            if(e.end.y >= lower_edge.start.y and e.end.y <= upper_edge.start.y and not right_verts.__contains__(e.end)):
                right_verts.append(e.end)
    return Leaf(right = decompose_leaves(edges=right_edges, vertices=right_verts, lower_edge=lower_edge, upper_edge=upper_edge, left_edge=split_edge, right_edge=right_edge), left = decompose_leaves(edges=left_edges, vertices=left_verts, lower_edge=lower_edge, upper_edge=upper_edge, left_edge=left_edge, right_edge=split_edge), split_edge=split_edge)
    
def plot_plane(vertices, points):
    x = [v.x for v in vertices]
    y = [v.y for v in vertices]
    plt.plot(x + [x[0]], y + [y[0]], 'b-') 
    for point in points:
        plt.scatter(point[0], point[1], color="red", label="Point")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Polygon')
    plt.grid(True)
    plt.xlim(MIN_X-1, MAX_X)
    plt.ylim(MIN_Y-1, MAX_Y)
    #plt.show()


def plot_trapezoid(edges: List[Edge]):
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Polygon')
    plt.xlim(MIN_X-1, MAX_X)
    plt.ylim(MIN_Y-1, MAX_Y)
    plt.grid(True)
    for e in edges:
        plt.plot([e.start.x, e.end.x], [e.start.y, e.end.y], linestyle='-')

def vert_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j].y > key.y:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    
        

# vertices = [Point(0, 1.5), Point(1, 3.5), Point(3.5, 4), Point(5, 2), Point(2.5, 0)]
# edges = [Edge(vertices[0], vertices[1]), Edge(vertices[1], vertices[2]), Edge(vertices[2], vertices[3]), Edge(vertices[3], vertices[4]), Edge(vertices[4], vertices[0])]
vertices = [Point(0, 1.5), Point(1, 3.5), Point(3.5, 4), Point(5, 2), Point(2.5, 0)]
edges = [Edge(vertices[0], vertices[1]), Edge(vertices[1], vertices[2]), Edge(vertices[2], vertices[3]), Edge(vertices[3], vertices[4]), Edge(vertices[3], vertices[1]), Edge(vertices[4], vertices[0])]

points = []
for i in range(5):
    point = np.array([random.uniform(0, 6), random.uniform(0,3)])  # Point to test
    points.append(point)
plot_plane(vertices, points)
vert_sort(vertices)
tree = Tree(decompose_root(edges, vertices, get_lower_edge(vertices), get_upper_edge(vertices), get_right_edge(vertices), get_left_edge(vertices)))
tree.display()