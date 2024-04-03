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
        
    def locate(self, p: Point):
        if is_not_right(p, self.split_edge):
            self.left.locate(p)
        else:
            self.right.locate(p)
    
    def display(self):
        res = "[LeftRightNode([" + str(self.split_edge.start.x) + "," + str(self.split_edge.start.y) + "],[" + str(self.split_edge.end.x) + "," + str(self.split_edge.end.y)  + "]) -> Left : "
        res += self.left.display()
        res += " , Right : "
        res += self.right.display()
        res += "]"
        return res
        
    
class Root:
    def __init__(self, lower: Leaf, upper: Leaf, med: int) -> None:
        self.lower = lower
        self.upper = upper
        self.med = med
        
    def locate(self, p: Point):
        if p.y >= self.med:
            self.upper.locate(p)
        else:
            self.lower.locate(p)
        
    def display(self):
        res = "[UpperLowerNode(" + str(self.med) + ") -> Upper : "
        res += self.upper.display()
        res += " , Lower : "
        res += self.lower.display()
        res += "]"
        return res
        

class Tree:
    def __init__(self, root: Root) -> None:
        self.root = root
        
    def locate(self, p: Point):
        self.root.locate(p)
    
    def display(self):
        res = "TREE:\n"
        res += self.root.display()
        print(res)
        plt.show()

class Trapezoid:
    def __init__(self, edges: List[Edge]) -> None:
        self.edges = edges
        
    def locate(self, p: Point):
        print("POINT:")
        p.print()
        print("FOUND IN TRAPEZOID:")
        for e in self.edges:
            e.print()
    
    def display(self):
        res = "[Trapezoid -> "
        for e in self.edges:
            res += "([" + str(e.start.x) + "," + str(e.start.y) + "],[" + str(e.end.x) + "," + str(e.end.y)  + "]) "
        plot_trapezoid(self.edges)
        return res
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

def is_left(p: Point, e: Edge):
    vec1 = Point(e.end.x - e.start.x, e.end.y - e.start.y)
    vec2 = Point(p.x - e.start.x, p.y - e.start.y)
    cross = vec1.x * vec2.y - vec1.y * vec2.x
    if cross > 0:
        return -1 #left
    elif cross < 0:
        return 1 #right
    else:
        return 0
def is_not_right(p: Point, e: Edge):
    res = is_left(p, e)
    if res == -1 or res == 0:
        return True
    else:
        return False

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
    return Root(decompose_leaves(lower, lower_v, lower_edge, med, right_edge, left_edge), decompose_leaves(upper, upper_v, med, upper_edge, right_edge, left_edge), med.start.y)

def decompose_leaves(edges: List[Edge], vertices: List[Point], lower_edge: Edge, upper_edge: Edge, right_edge: Edge, left_edge: Edge):
    split_edge = None
    inner_point = False
    for e in edges:
        if e.start.y <= lower_edge.start.y and e.end.y >= upper_edge.start.y:
            split_edge = e
            break
        if (is_not_right(e.start, right_edge) and not is_not_right(e.start, left_edge) and e.start.y != upper_edge.start.y and e.start.y != lower_edge.start.y) or (is_not_right(e.end, right_edge) and not is_not_right(e.end, left_edge) and e.end.y != upper_edge.start.y and e.end.y != lower_edge.start.y):
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
        start_check = is_left(e.start, split_edge)
        end_check = is_left(e.end, split_edge)
        if start_check == -1:
            if not left_edges.__contains__(e):
                left_edges.append(e)
            if e.start.y >= lower_edge.start.y and e.start.y <= upper_edge.start.y and not left_verts.__contains__(e.start):
                left_verts.append(e.start)
        elif start_check == 1:
            if not right_edges.__contains__(e):
                right_edges.append(e)
            if e.start.y >= lower_edge.start.y and e.start.y <= upper_edge.start.y and not right_verts.__contains__(e.start):
                right_verts.append(e.start)
        
        if end_check == -1:
            if not left_edges.__contains__(e):
                left_edges.append(e)
            if e.end.y >= lower_edge.start.y and e.end.y <= upper_edge.start.y and not left_verts.__contains__(e.end):
                left_verts.append(e.end)
        elif start_check == 1:
            if not right_edges.__contains__(e):
                right_edges.append(e)
            if e.end.y >= lower_edge.start.y and e.end.y <= upper_edge.start.y and not right_verts.__contains__(e.end):
                right_verts.append(e.end)
        
        # if e.start.x < split_edge.start.x or e.start.x < split_edge.end.x or e.end.x < split_edge.start.x or e.end.x < split_edge.end.x:
        #     left_edges.append(e)
        #     if(e.start.y >= lower_edge.start.y and e.start.y <= upper_edge.start.y and not left_verts.__contains__(e.start)):
        #         left_verts.append(e.start)
        #     if(e.end.y >= lower_edge.start.y and e.end.y <= upper_edge.start.y and not left_verts.__contains__(e.end)):
        #         left_verts.append(e.end)
        # if e.start.x > split_edge.start.x or e.start.x > split_edge.end.x or e.end.x > split_edge.start.x or e.end.x > split_edge.end.x:
        #     right_edges.append(e)
        #     if(e.start.y >= lower_edge.start.y and e.start.y <= upper_edge.start.y and not right_verts.__contains__(e.start)):
        #         right_verts.append(e.start)
        #     if(e.end.y >= lower_edge.start.y and e.end.y <= upper_edge.start.y and not right_verts.__contains__(e.end)):
        #         right_verts.append(e.end)
    return Leaf(right = decompose_leaves(edges=right_edges, vertices=right_verts, lower_edge=lower_edge, upper_edge=upper_edge, left_edge=split_edge, right_edge=right_edge), left = decompose_leaves(edges=left_edges, vertices=left_verts, lower_edge=lower_edge, upper_edge=upper_edge, left_edge=left_edge, right_edge=split_edge), split_edge=split_edge)
    
def plot_plane(edges, points):
    for e in edges:
        plt.plot([e.start.x, e.end.x], [e.start.y, e.end.y], 'b-')
    for point in points:
        plt.scatter(point.x, point.y, color="red", label="Point")
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
    

def run():
   # vertices = [Point(0, 1.5), Point(1, 3.5), Point(3.5, 4), Point(5, 2), Point(2.5, 0)]
    # edges = [Edge(vertices[0], vertices[1]), Edge(vertices[1], vertices[2]), Edge(vertices[2], vertices[3]), Edge(vertices[3], vertices[4]), Edge(vertices[4], vertices[0])]
    vertices = [Point(0, 1.5), Point(1, 3.5), Point(3.5, 4), Point(5, 2), Point(2.5, 0)]
    edges = [Edge(vertices[0], vertices[1]), Edge(vertices[1], vertices[2]), Edge(vertices[2], vertices[3]), Edge(vertices[3], vertices[4]), Edge(vertices[3], vertices[1]), Edge(vertices[4], vertices[0])]
    # vertices = [Point(0, 0), Point(0.2, 3), Point(0.5, 2.5), Point(0.7, 2.8), Point(1, 2.3), Point(1.2, 2.7), Point(1.3, 0)]
    # edges = [Edge(vertices[0], vertices[1]), Edge(vertices[1], vertices[2]), Edge(vertices[2], vertices[3]), Edge(vertices[3], vertices[4]), Edge(vertices[4], vertices[5]), Edge(vertices[5], vertices[6]), Edge(vertices[6], vertices[0])]
    # vertices = [Point(0, 0), Point(2, 5), Point(3, 3), Point(5, 4), Point(6, 1)]
    # edges = [Edge(vertices[0], vertices[1]), Edge(vertices[1], vertices[2]), Edge(vertices[2], vertices[3]), Edge(vertices[3], vertices[4]), Edge(vertices[4], vertices[0])]
    points = []
    for i in range(5):
        point = Point(random.uniform(0, 6), random.uniform(0,3))  # Point to test
        points.append(point)
    plot_plane(edges, points)
    vert_sort(vertices)
    tree = Tree(decompose_root(edges, vertices, get_lower_edge(vertices), get_upper_edge(vertices), get_right_edge(vertices), get_left_edge(vertices)))
    for p in points:
        tree.locate(p)
    tree.display()     

run()
    