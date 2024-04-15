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
    def __init__(self, point: Point, up, down) -> None:
        self.point = point
        self.up = up
        self.down = down
        
class LRNode:
    def __init__(self, point: Point, left, right) -> None:
        self.point = point
        self.left = left
        self.right = right
        
        
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
    
points = gen_points(8)
plot_points(points)
plt.show()
