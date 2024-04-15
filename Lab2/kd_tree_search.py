import matplotlib.pyplot as plt
import random
import math
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
        
class UDNode:
    def __init__(self, med: Edge, up, down) -> None:
        self.med = med
        self.up = up
        self.down = down
    
    def display(self, tabulation):
        plt.plot([self.med.start.x, self.med.end.x], [self.med.start.y, self.med.end.y], 'b-')
        res = "\n" + tabulation + "[UpDownNode(" + str(self.med.start.y) + ") -> Up : "
        res += self.up.display(tabulation + "\t")
        res += " , Down : "
        res += self.down.display(tabulation + "\t")
        res += "]"
        return res
        
class LRNode:
    def __init__(self, med: Edge, left, right) -> None:
        self.med = med
        self.left = left
        self.right = right
    
    def display(self, tabulation):
        plt.plot([self.med.start.x, self.med.end.x], [self.med.start.y, self.med.end.y], 'b-')
        res = "\n" + tabulation  + "[LeftRightNode(" + str(self.med.start.x) + ") -> Left : "
        res += self.left.display(tabulation + "\t")
        res += " , Right : "
        res += self.right.display(tabulation + "\t")
        res += "]"
        return res

class Leaf:
    def display(self):
        return "Leaf reached"
        
        
def sort_y(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j].y > key.y:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        
def sort_x(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j].x > key.x:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
        
        
def gen_points(num: int) -> List[Point]:
    points = []
    for i in range(num):
        points.append(Point(random.uniform(MIN_X, MAX_X), random.uniform(MIN_Y,MAX_Y)))
    return points

def plot_points(points: List[Point]):
    for point in points:
        plt.scatter(point.x, point.y, color="red", label="Point")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Polygon')
    plt.grid(True)
    plt.xlim(MIN_X-1, MAX_X+1)
    plt.ylim(MIN_Y-1, MAX_Y+1)
    
    
def make_lr_node(points: List[Point], left_bound: int, right_bound: int, lower_bound: int, upper_bound: int):
    if len(points) == 0:
        return Leaf
    sort_x(points)
    ind = math.floor(len(points)/2)
    med = Edge(Point(points[ind].x, lower_bound), Point(points[ind].x, upper_bound))
    l_points = []
    r_points = []
    for i in range(0, ind):
        l_points.append(points[i])
    for i in range(ind+1, len(points)):
        r_points.append(points[i])
    return LRNode(med=med,
                  left=make_ud_node(l_points, left_bound=left_bound, right_bound=med.start.x, lower_bound=lower_bound, upper_bound=upper_bound),
                  right=make_ud_node(r_points, left_bound=med.start.x, right_bound=right_bound, lower_bound=lower_bound, upper_bound=upper_bound))
    
def make_ud_node(points: List[Point], left_bound: int, right_bound: int, lower_bound: int, upper_bound: int):
    if len(points) == 0:
        return Leaf
    sort_y(points)
    ind = math.floor(len(points)/2)
    med = Edge(Point(left_bound, points[ind].y), Point(right_bound, points[ind].y))
    u_points = []
    d_points = []
    for i in range(0, ind):
        d_points.append(points[i])
    for i in range(ind+1, len(points)):
        u_points.append(points[i])
    return UDNode(med=med,
                    up=make_lr_node(u_points, lower_bound=med.start.y, upper_bound=upper_bound, left_bound=left_bound, right_bound=right_bound),
                    down=make_lr_node(d_points, lower_bound=lower_bound, upper_bound=med.start.y, right_bound=right_bound, left_bound=left_bound))
    
points = gen_points(8)
plot_points(points)
tree = make_lr_node(points, left_bound=MIN_X, right_bound=MAX_X, lower_bound=MIN_Y, upper_bound=MAX_Y)
print(tree.display("\t"))
plt.show()
