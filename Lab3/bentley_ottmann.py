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
        
    def __str__(self):
        return f"({self.x} , {self.y})"
    
class SegPoint:
    def __init__(self, point, segments) -> None:
        self.point = point
        self.seg = segments
    def __str__(self) -> str:
        seg_str = ""
        for s in self.seg:
            seg_str += str(s)
        return f"Segments {seg_str}\nPoint {self.point}"
        
class Segment:
    def __init__(self, start: Point, end: Point) -> None:
        self.start = start
        self.end = end
        if self.start.y < self.end.y:
            self.start, self.end = self.end, self.start
    
    def __str__(self):
        return f"({self.start} -> {self.end})"
    

def quicksort(points):
    def compare(point1, point2):
        if point1.y > point2.y or (point1.y == point2.y and point1.x < point2.x):
            return -1
        elif point1.y < point2.y or (point1.y == point2.y and point1.x > point2.x):
            return 1
        else:
            return 0
    
    def partition(arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if compare(arr[j].point, pivot.point) == -1:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1

    def quicksort_helper(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quicksort_helper(arr, low, pi - 1)
            quicksort_helper(arr, pi + 1, high)

    quicksort_helper(points, 0, len(points) - 1)
    

def find_intersect(seg1: Segment, seg2: Segment):
    x1, y1 = seg1.start.x, seg1.start.y 
    x2, y2 = seg1.end.x, seg1.end.y
    x3, y3 = seg2.start.x, seg2.start.y
    x4, y4 = seg2.end.x, seg2.end.y

    # Calculate slopes
    slope1 = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else float('inf')
    slope2 = (y4 - y3) / (x4 - x3) if x4 - x3 != 0 else float('inf')

    # Check if the segments are parallel
    if slope1 == slope2:
        return None  # No intersection

    # Calculate intersection point
    if slope1 == float('inf'):  # segment1 is vertical
        x = x1
        y = slope2 * (x - x3) + y3
    elif slope2 == float('inf'):  # segment2 is vertical
        x = x3
        y = slope1 * (x - x1) + y1
    else:
        x = ((slope1 * x1 - y1) - (slope2 * x3 - y3)) / (slope1 - slope2)
        y = slope1 * (x - x1) + y1

    # Check if intersection point is within both line segments
    if (min(x1, x2) <= x <= max(x1, x2)) and (min(x3, x4) <= x <= max(x3, x4)) and \
       (min(y1, y2) <= y <= max(y1, y2)) and (min(y3, y4) <= y <= max(y3, y4)):
        return Point(x, y)
    else:
        return None  # Intersection point lies outside one or both segments

    
def gen_segments(num: int):
    segments = []
    points = []
    for i in range(num):
        segments.append(Segment(Point(random.uniform(MIN_X, MAX_X), random.uniform(MIN_Y,MAX_Y)), Point(random.uniform(MIN_X, MAX_X), random.uniform(MIN_Y,MAX_Y))))
        points.append(SegPoint(segments[len(segments)-1].start, [segments[len(segments)-1]]))
        points.append(SegPoint(segments[len(segments)-1].end, [segments[len(segments)-1]]))
    quicksort(points)
    return segments, points

def plot_segments(segments: List[Segment]):
    for segment in segments:
        plt.scatter(segment.start.x, segment.start.y, color="green", s=8)
        plt.scatter(segment.end.x, segment.end.y, color="green", s=8)
        plt.plot([segment.start.x, segment.end.x], [segment.start.y, segment.end.y], "b-")
    plt.gca().set_aspect('equal', adjustable='box')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Segments')
    plt.grid(True)
    plt.xlim(MIN_X-1, MAX_X+1)
    plt.ylim(MIN_Y-1, MAX_Y+1)
    
def plane_sweep(segments, event_queue : List[SegPoint]):
    status_queue = []
    intersections = []
    while len(event_queue) > 0:
        event = event_queue[0]
        event_queue.remove(event_queue[0])
        seg = event.seg
        if len(seg) == 1:
            #Start or end
            if seg[0] in status_queue:
                ind = status_queue.index(seg[0])
                status_queue.remove(seg[0])
                if ind-1 >= 0 and ind != len(status_queue):
                    intersect = find_intersect(status_queue[ind-1], status_queue[ind])
                    if intersect:
                        if intersect not in intersections:
                            intersections.append(intersect)
                        segP = SegPoint(intersect, [status_queue[ind-1], status_queue[ind]])
                        if segP not in event_queue:
                            event_queue.append(segP)
                            quicksort(event_queue)
            else:
                if len(status_queue) == 0:
                    status_queue.append(seg[0])
                elif len(status_queue) == 1:
                    if seg[0] not in status_queue:
                        if status_queue[0].start.x < seg[0].start.x:
                            status_queue.append(seg[0])
                        else:
                            status_queue.insert(0, seg[0])
                        intersect = find_intersect(status_queue[0], status_queue[1])
                        if intersect:
                            if intersect not in intersections:
                                intersections.append(intersect)
                            segP = SegPoint(intersect, [status_queue[0], status_queue[1]])
                            if segP not in event_queue:
                                event_queue.append(segP)
                                quicksort(event_queue)
                else:
                    for i in range(1, len(status_queue)):
                        if status_queue[i-1].start.x <= seg[0].start.x and status_queue[i].start.x >= seg[0].start.x:
                            status_queue.insert(i, seg[0])
                            changed = False
                            intersect = find_intersect(status_queue[i], status_queue[i-1])
                            if intersect:
                                if intersect not in intersections:
                                    intersections.append(intersect)
                                segP = SegPoint(intersect, [status_queue[i], status_queue[i-1]])
                                if segP not in event_queue:
                                    event_queue.append(segP)
                                    changed = True
                            intersect = find_intersect(status_queue[i], status_queue[i+1])
                            if intersect:
                                if intersect not in intersections:
                                    intersections.append(intersect)
                                segP = SegPoint(intersect, [status_queue[i], status_queue[i+1]])
                                if segP not in event_queue:
                                    event_queue.append(segP)
                                    changed = True
                                if changed:
                                    quicksort(event_queue)
                            break 
                        elif i == len(status_queue)-1:
                            status_queue.append(seg[0])
                            intersect = find_intersect(status_queue[i], status_queue[i-1])
                            if intersect:
                                if intersect not in intersections:
                                    intersections.append(intersect)
                                segP = SegPoint(intersect, [status_queue[i], status_queue[i-1]])
                                if segP not in event_queue:
                                    event_queue.append(segP)
                                    quicksort(event_queue)
        else:
            #Intersection
            s1 = status_queue.index(seg[0])
            s2 = status_queue.index(seg[1])
            status_queue[s1], status_queue[s2] = status_queue[s2], status_queue[s1]
            # if event.point not in intersections:
            #     intersections.append(event.point)
        
        print("Statuses:")
        for s in status_queue:
            print(s)
        print("Events:")
        for e in event_queue:
            print(e)
        plot_segments(segments)
        plt.plot([MIN_X, MAX_X], [event.point.y, event.point.y], "r-")
        for intersection in intersections:
            plt.scatter(intersection.x, intersection.y, s=20, color="red")
        plt.show()
    return intersections
    
segments, points = gen_segments(5)
for point in points:
    print(point.point)
intersections = plane_sweep(segments, points)

plot_segments(segments)
for intersection in intersections:
    plt.scatter(intersection.x, intersection.y, s=20, color="red")
    