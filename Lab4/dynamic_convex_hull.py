import copy
import random
from typing import List
import matplotlib.pyplot as plt
import numpy

from enum import Enum

MIN_X = 0
MAX_X = 7
MIN_Y = 0
MAX_Y = 7

class DynamicConvexHull:
    def __init__(self):
        self.upper_convex_hull = UpperConvexHull()
        self.lower_convex_hull = LowerConvexHull()

    def insert(self, new_point):
        self.upper_convex_hull.insert(new_point)
        self.lower_convex_hull.insert(new_point)

    def delete(self, to_delete_point):
        self.upper_convex_hull.delete(to_delete_point)
        self.lower_convex_hull.delete(to_delete_point)

    def plot(self, figure, ax):
        self.upper_convex_hull.plot(figure, ax)
        return self.lower_convex_hull.plot(figure, ax)
    
    def print(self):
        print("UPPER:")
        self.upper_convex_hull.print()
        print("LOWER:")
        self.lower_convex_hull.print()


class UpperConvexHull:
    def __init__(self):
        self.bst = ConvexHullTree()

    def insert(self, insert_point):
        self.bst.insert(insert_point)

    def delete(self, delete_point):
        self.bst.delete(delete_point)

    def plot(self, figure, axes):
        return self.bst.plot(figure, axes)
    
    def print(self):
        self.bst.print()


class LowerConvexHull:
    def __init__(self):
        self.bst = ConvexHullTree()

    def insert(self, insert_point):
        to_insert = copy.deepcopy(insert_point)
        to_insert.y *= -1

        self.bst.insert(to_insert)

    def delete(self, delete_point):
        to_delete = copy.deepcopy(delete_point)
        to_delete.y *= -1

        self.bst.delete(to_delete)

    def plot(self, figure, axes):
        return self.bst.plot(figure, axes, lower=True)
    
    def print(self):
        self.bst.print()


class Point:
    i = 0

    def __init__(self, x_, y_):
        self.x = x_
        self.y = y_
        self.id = Node.i
        Node.i += 1

    def __repr__(self):
        return str(f"({self.x}; {self.y})")

    def __lt__(self, other):
        return self.x < other.x or (self.x == other.x and self.y < other.y)


class NodeData:
    def __init__(self, key=None):
        self.left_most_right: Node = None
        self.left_most_right_point: Point = key
        self.points_array = []
        self.separating_index = 0
        self.convex_hull = []
        self.graph_hull = []
        self.convex_hull.append(key)

    def __lt__(self, other):
        return self.left_most_right_point < other.left_most_right_point

    def __repr__(self):
        return str(f"[lMax={self.left_most_right_point}; convex_hull={self.convex_hull}; sep_ind={self.separating_index}")


class NodeColor(Enum):
    RED = 1
    BLACK = 2


class Classification(Enum):
    CONVEX = 1
    CONCAVE = 2 
    SUPPORTING = 3 
    ERROR = -1

class Node:
    i = 0

    def __init__(self, data):
        self.data: NodeData = data
        self.parent: Node = None
        self.left: Node = None
        self.right: Node = None
        self.color = NodeColor.RED
        self.id = Node.i
        Node.i += 1

    def __lt__(self, other):
        return self.data < other.data

    def __repr__(self):
        return str(f"{self.id}: {self.data}")
    
    def print(self, tabs):
        print(f"{tabs}Node {self}")
        if self.left and (self.left.id != 0 and self.left.id != 1):
            print(f"{tabs}left -> ")
            self.left.print(tabs+"\t")
        if self.right and (self.right.id != 0 and self.right.id != 1):
            print(f"{tabs}right -> ")
            self.right.print(tabs+"\t")

    def plot(self, figure, axes, TNULL, lower=False):
        if self is None or self == TNULL:
            return figure, axes

        if self.left == TNULL:
            point_x, point_y = self.data.left_most_right_point.x, self.data.left_most_right_point.y
            point_id = self.data.left_most_right_point.id
            if lower:
                point_y *= -1
            axes.scatter([point_x], [point_y], color="red")
            axes.annotate(f"({point_id}); ({point_x}; {point_y})", (point_x, point_y),
                          xytext=(point_x - 0.01, point_y + 0.01))
            return figure, axes

        chain = self.data.graph_hull
        if self.parent == TNULL:
            chain = self.data.points_array
        color = numpy.random.rand(3, )

        for i in range(1, len(chain)):
            if lower:
                axes.plot([chain[i - 1].x, chain[i].x], [-1 * chain[i - 1].y, -1 * chain[i].y], color=color)
            else:
                axes.plot([chain[i - 1].x, chain[i].x], [chain[i - 1].y, chain[i].y], color=color)

        if self.left != TNULL:
            self.left.data.graph_hull = chain[:self.data.separating_index + 1] + self.left.data.points_array

        if self.right != TNULL:
            self.right.data.graph_hull = self.right.data.points_array + chain[self.data.separating_index + 1:]

        self.left.plot(figure, axes, TNULL, lower)
        return self.right.plot(figure, axes, TNULL, lower)

    def graph_viz(self, TNULL, string_mutable):
        if self is None or self == TNULL:
            return

        string_mutable[0] += f"\"{self}\""

        if self.color == NodeColor.RED:
            string_mutable[0] += " [color = \"red\"]"
        string_mutable[0] += "\n"

        if self.left != TNULL:
            string_mutable[0] += f"\"{self}\" -> \"{self.left}\" [label = \"left\"]\n"
        if self.right != TNULL:
            string_mutable[0] += f"\"{self}\" -> \"{self.right}\" [label = \"right\"]\n"

        self.left.graph_viz(TNULL, string_mutable)
        self.right.graph_viz(TNULL, string_mutable)


    
class ConvexHullTree:
    def __init__(self):
        self.TNULL = Node(NodeData())
        self.TNULL.color = NodeColor.BLACK
        self.TNULL.left = None
        self.TNULL.right = None
        self.root = self.TNULL

    def insert(self, key):
        node = Node(NodeData(key))
        node.parent = None
        node.data.left_most_right = node
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = NodeColor.RED

        x = self.root

        if x == self.TNULL:
            self.root = node
            return

        left_neighbour, right_neighbour = self.down(x, key)

        new_node_parent = Node(NodeData())
        node.parent = new_node_parent

        if left_neighbour is None:
            new_node_parent.left = node
            new_node_parent.right = right_neighbour

            new_node_parent.parent = right_neighbour.parent
            if right_neighbour.parent is None:
                self.root = new_node_parent
                new_node_parent.parent = self.TNULL
            else:
                right_neighbour.parent.left = new_node_parent

            right_neighbour.parent = new_node_parent

        elif right_neighbour is None:
            new_node_parent.right = node
            new_node_parent.left = left_neighbour

            new_node_parent.parent = left_neighbour.parent
            if left_neighbour.parent is None:
                self.root = new_node_parent
                new_node_parent.parent = self.TNULL
            else:
                left_neighbour.parent.right = new_node_parent

            left_neighbour.parent = new_node_parent

        elif self.find_brother(left_neighbour)[0] == right_neighbour:
            new_node_parent.left = left_neighbour
            new_node_parent.right = node

            new_node_parent.parent = left_neighbour.parent
            left_neighbour.parent.left = new_node_parent

            left_neighbour.parent = new_node_parent
        else:
            new_node_parent.left = node
            new_node_parent.right = right_neighbour

            new_node_parent.parent = right_neighbour.parent

            neighbour_side = self.node_side(right_neighbour)
            if neighbour_side == -1:
                right_neighbour.parent.left = new_node_parent
            else:
                right_neighbour.parent.right = new_node_parent

            right_neighbour.parent = new_node_parent

        self.up(node)

    def node_side(self, node):
        if node.parent.left == node:
            return -1
        elif node.parent.right == node:
            return 1
        else:
            return 0

    def down(self, current_node: Node, point: Point, left_neighbour: Node=None, right_neighbour: Node=None):
        if current_node.left == self.TNULL:
            if point.x <= current_node.data.left_most_right_point.x:
                right_neighbour = current_node
            else:
                left_neighbour = current_node
            return left_neighbour, right_neighbour

        left_queue = current_node.data.convex_hull[:current_node.data.separating_index + 1]
        right_queue = current_node.data.convex_hull[current_node.data.separating_index + 1:]

        left_son = current_node.left
        right_son = current_node.right

        if left_son.left != self.TNULL:
            left_son.data.convex_hull = left_queue + left_son.data.points_array

        if right_son.left != self.TNULL:
            right_son.data.convex_hull = right_son.data.points_array + right_queue

        if point.x <= current_node.data.left_most_right_point.x:
            right_neighbour = current_node
            current_node = current_node.left

        else:
            left_neighbour = current_node.data.left_most_right
            current_node = current_node.right

        return self.down(current_node, point, left_neighbour, right_neighbour)

    def up(self, current_node: Node):
        if current_node == self.get_root():
            current_node.data.points_array = current_node.data.convex_hull
            return

        current_brother, side = self.find_brother(current_node)

        q_1, q_2, q_3, q_4, j = [], [], [], [], 0
        if side == -1:
            q_1, q_2, q_3, q_4, j = merge_chains(current_brother.data.convex_hull, current_node.data.convex_hull)
        elif side == 1:
            q_1, q_2, q_3, q_4, j = merge_chains(current_node.data.convex_hull, current_brother.data.convex_hull)

        current_node.parent.left.data.points_array = q_2
        current_node.parent.right.data.points_array = q_3

        current_node.parent.data.convex_hull = q_1 + q_4
        current_node.parent.data.separating_index = j

        current_node.parent.data.left_most_right = self.find_left_most_right(current_node.parent)
        current_node.parent.data.left_most_right_point = current_node.parent.data.left_most_right.data.left_most_right_point

        self.up(current_node.parent)

    def find_brother(self, node: Node):
        if node.parent.left == node:
            return node.parent.right, 1
        elif node.parent.right == node:
            return node.parent.left, -1
        return self.TNULL

    def find_left_most_right(self, node: Node):
        current_node = node

        if current_node.left != self.TNULL:
            current_node = current_node.left

        while current_node.right != self.TNULL:
            current_node = current_node.right

        return current_node.data.left_most_right

    def get_root(self):
        return self.root

    def delete(self, data):
        node = Node(NodeData(data))
        node.parent = None
        node.data.left_most_right = node
        node.left = self.TNULL
        node.right = self.TNULL
        node.color = NodeColor.RED

        x = self.root

        _, to_delete_node = self.down(x, data)

        if to_delete_node is None or \
                (to_delete_node.data.left_most_right_point.x != data.x or
                 to_delete_node.data.left_most_right_point.y != data.y):
            print("There is no such point among added from set")
        elif to_delete_node == self.get_root():
            self.root = self.TNULL
        elif to_delete_node.parent.parent == self.TNULL:
            brother, _ = self.find_brother(to_delete_node)

            brother.data.points_array = brother.data.convex_hull

            self.root = brother
            brother.parent = self.TNULL
        else:
            node_parent = to_delete_node.parent
            brother, _ = self.find_brother(to_delete_node)

            side = self.node_side(node_parent)

            if side == -1:
                node_parent.parent.left = brother
            elif side == 1:
                node_parent.parent.right = brother

            brother.parent = node_parent.parent
            self.up(brother)

    def plot(self, fig, ax, lower=False):
        return self.get_root().plot(fig, ax, self.TNULL, lower=lower)
    
    def print(self):
        if not self.root:
            print("NO ROOT")
            return
        self.root.print("")

    def graph_viz(self):
        string = "digraph g {\n"
        wrapper = [string]

        self.get_root().graph_viz(self.TNULL, wrapper)

        return wrapper[0] + "}\n"


def merge_chains(chain_1, chain_2):
    if len(chain_2) == 1:
        if len(chain_1) == 1:
            return chain_1, [], [], chain_2, 0

        if len(chain_1) == 2:
            if is_point_left(chain_1[0], chain_1[1], chain_2[0]):
                return chain_1[:1], chain_1[1:], [], chain_2, 0
            else:
                return chain_1, [], [], chain_2, 1

    if len(chain_1) == 1:
        if is_point_left(chain_2[0], chain_2[1], chain_1[0]):
            return chain_1, [], chain_2[:1], chain_2[1:], 0
        else:
            return chain_1, [], [], chain_2, 0

    index_1 = int((len(chain_1) - 1) / 2)
    index_2 = int((len(chain_2) - 1) / 2)

    temp_min_1 = 0
    temp_max_1 = len(chain_1) - 1

    temp_min_2 = 0
    temp_max_2 = len(chain_2) - 1

    extreme_left_1 = False
    extreme_right_1 = False

    extreme_left_2 = False
    extreme_right_2 = False

    while True:
        extreme_left_1 = False
        extreme_right_1 = False

        extreme_left_2 = False
        extreme_right_2 = False

        if index_1 == temp_min_1:
            extreme_left_1 = True
        if index_1 == temp_max_1:
            extreme_right_1 = True

        if index_2 == temp_min_2:
            extreme_left_2 = True
        if index_2 == temp_max_2:
            extreme_right_2 = True

        type_1 = Classification.ERROR
        type_2 = Classification.ERROR

        if extreme_left_1 and extreme_right_1:
            type_1 = Classification.SUPPORTING

        elif extreme_left_1:
            type_1 = define_point_type_left(Point(chain_1[index_1].x, chain_1[index_1].y - 1),
                                            chain_1[index_1],
                                            chain_1[index_1 + 1], chain_2[index_2])
        elif extreme_right_1:
            type_1 = define_point_type_left(chain_1[index_1 - 1], chain_1[index_1],
                                            Point(chain_1[index_1].x, chain_1[index_1].y - 1),
                                            chain_2[index_2])
        else:
            type_1 = define_point_type_left(chain_1[index_1 - 1], chain_1[index_1], chain_1[index_1 + 1],
                                            chain_2[index_2])

        if extreme_left_2 and extreme_right_2:
            type_2 = Classification.SUPPORTING

        elif extreme_left_2:
            type_2 = define_point_type_right(Point(chain_2[index_2].x, chain_2[index_2].y - 1),
                                             chain_2[index_2],
                                             chain_2[index_2 + 1], chain_1[index_1])
        elif extreme_right_2:
            type_2 = define_point_type_right(chain_2[index_2 - 1], chain_2[index_2],
                                             Point(chain_2[index_2].x, chain_2[index_2].y - 1),
                                             chain_1[index_1])
        else:
            type_2 = define_point_type_right(chain_2[index_2 - 1], chain_2[index_2], chain_2[index_2 + 1],
                                             chain_1[index_1])

        if type_1 == Classification.CONCAVE and type_2 == Classification.CONCAVE:
            check_result = concave_concave_case(chain_1[index_1], chain_1[index_1 + 1], chain_1[temp_max_1],
                                                chain_2[temp_min_2], chain_2[index_2 - 1], chain_2[index_2])
            if check_result == -1:
                temp_min_1 = index_1
                if temp_max_1 - index_1 != 1:
                    index_1 = int((index_1 + temp_max_1) / 2)
                else:
                    index_1 = temp_max_1
            elif check_result == 1:
                temp_max_2 = index_2
                index_2 = int((temp_min_2 + index_2) / 2)
            else:
                temp_min_1 = index_1
                if temp_max_1 - index_1 != 1:
                    index_1 = int((index_1 + temp_max_1) / 2)
                else:
                    index_1 = temp_max_1
                temp_max_2 = index_2
                index_2 = int((temp_min_2 + index_2) / 2)

        elif type_1 == Classification.CONCAVE and type_2 == Classification.SUPPORTING:
            temp_min_1 = index_1
            if temp_max_1 - index_1 != 1:
                index_1 = int((index_1 + temp_max_1) / 2)
            else:
                index_1 = temp_max_1

            temp_min_2 = index_2

        elif type_1 == Classification.CONCAVE and type_2 == Classification.CONVEX:
            temp_min_2 = index_2
            if temp_max_2 - index_2 != 1:
                index_2 = int((index_2 + temp_max_2) / 2)
            else:
                index_2 = temp_max_2

        elif type_1 == Classification.SUPPORTING and type_2 == Classification.CONCAVE:
            temp_max_1 = index_1

            temp_max_2 = index_2
            index_2 = int((temp_min_2 + index_2) / 2)

        elif type_1 == Classification.SUPPORTING and type_2 == Classification.SUPPORTING:
            break

        elif type_1 == Classification.SUPPORTING and type_2 == Classification.CONVEX:
            temp_max_1 = index_1

            temp_min_2 = index_2
            if temp_max_2 - index_2 != 1:
                index_2 = int((index_2 + temp_max_2) / 2)
            else:
                index_2 = temp_max_2

        elif type_1 == Classification.CONVEX and type_2 == Classification.CONCAVE:
            temp_max_1 = index_1
            index_1 = int((temp_min_1 + index_1) / 2)

        elif type_1 == Classification.CONVEX and type_2 == Classification.SUPPORTING:
            temp_max_1 = index_1
            index_1 = int((temp_min_1 + index_1) / 2)

            temp_min_2 = index_2

        elif type_1 == Classification.CONVEX and type_2 == Classification.CONVEX:
            temp_max_1 = index_1
            index_1 = int((temp_min_1 + index_1) / 2)

            temp_min_2 = index_2
            if temp_max_2 - index_2 != 1:
                index_2 = int((index_2 + temp_max_2) / 2)
            else:
                index_2 = temp_max_2

    return chain_1[:index_1 + 1], \
           chain_1[index_1 + 1:], \
           chain_2[:index_2], \
           chain_2[index_2:], \
           index_1


def concave_concave_case(q1, q1_successor, max_left, min_right, q2_predecessor, q2):
    center_line_x = (max_left.x + min_right.x) / 2
    if get_intersection_point(q1, q1_successor, q2_predecessor, q2).x < center_line_x:
        return -1
    elif get_intersection_point(q1, q1_successor, q2_predecessor, q2).x > center_line_x:
        return 1
    else:
        return 0


def get_intersection_point(a, b, c, d):
    return Point(((a.x * b.y - a.y * b.x) * (c.x - d.x) - (a.x - b.x) * (c.x * d.y - c.y * d.x))
                 / ((a.x - b.x) * (c.y - d.y) - (a.y - b.y) * (c.x - d.x)),
                 ((a.x * b.y - a.y * b.x) * (c.y - d.y) - (a.y - b.y) * (c.x * d.y - c.y * d.x))
                 / ((a.x - b.x) * (c.y - d.y) - (a.y - b.y) * (c.x - d.x)))


def define_point_type_left(q1_pred: Point, q1: Point, q1_suc: Point, q2: Point):
    if is_point_left(q2, q1, q1_pred) and is_point_left(q2, q1, q1_suc):
        return Classification.SUPPORTING
    if is_point_left(q2, q1, q1_pred) and not is_point_left(q2, q1, q1_suc):
        return Classification.CONCAVE
    else:
        return Classification.CONVEX


def define_point_type_right(q2_pred: Point, q2: Point, q2_suc: Point, q1: Point):
    if not is_point_left(q1, q2, q2_pred) and not is_point_left(q1, q2, q2_suc):
        return Classification.SUPPORTING
    if is_point_left(q1, q2, q2_pred) and not is_point_left(q1, q2, q2_suc):
        return Classification.CONCAVE
    else:
        return Classification.CONVEX


def is_point_left(chain_point_1, chain_point_2, point):
    return ((chain_point_2.x - chain_point_1.x) * (point.y - chain_point_1.y) - (chain_point_2.y - chain_point_1.y) * (
            point.x - chain_point_1.x)) > 0

# points = [Point(-1, -1),
#               Point(0, 0),
#               Point(6, 10),
#               Point(3, 6),
#               Point(-5, -3),
#               Point(7, 7)]

def gen_points(precision, num):
    points = []
    for i in range(num):
        points.append(Point(round(random.uniform(MIN_X, MAX_X), precision), round(random.uniform(MIN_Y,MAX_Y), precision)))
    return points

# pointsDelete = [Point(5, -3),
#               Point(6, 10)]

dynamicConvexHull = DynamicConvexHull()
points = gen_points(3, 8)
for point in points:
    figure, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    axes.set_title("Add "+str(point))
    dynamicConvexHull.insert(point)
    dynamicConvexHull.plot(figure, axes)
    print(f"\nInserting {point}")
    dynamicConvexHull.print()
    plt.show()
points.reverse()

for point in points:
    figure, axes = plt.subplots(nrows=1, ncols=1, figsize=(10, 10))
    axes.set_title("Delete "+str(point))
    dynamicConvexHull.delete(point)
    dynamicConvexHull.plot(figure, axes)
    print(f"\nDeleting {point}")
    dynamicConvexHull.print()
    plt.show()