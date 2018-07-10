import os, string, sys

import copy
from collections import deque
import heapq
from itertools import permutations

# appends padding spaces if the number is smaller than the largest value
# e.g. if the largest val=1245, 1 will be represented as '1   '
def format_num(n, maxSpaces):
    strNum = str(n)
    return strNum + ' ' * (maxSpaces - len(strNum))

class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]

# Just a wrapper over python dict to preserve things
# like height, width; also a pretty printing function provided
class Grid:
    def __init__(self, w, h, d):
        self.width = w
        self.height = h
        self.d = d
        self.walls = self.find_walls()
        self.weights = {}

    def cost(self, a, b):
        return self.weights.get(b, 1)

    def in_bounds(self, p):
        (x, y) = p
        return 0 <= x < self.width and 0 <= y < self.height

    def is_wall(self, p):
        return p not in self.walls

    def passable(self, p):
        return p not in self.walls

    def find_walls(self):
        walls = []
        for key in self.d:
            if self.d[key] == -1:
                walls.append(key)
        return walls

    def neighbors(self, p):
        (x, y) = p
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        results = filter(self.in_bounds, results)
        results = filter(self.is_wall, results)
        return results
    
    # pretty print the grid using the number formatter
    def pretty_print_grid(self):
        nSpaces = len(str(max(self.d.values()))) + 1
        strDelim = '|' + ('-' + (nSpaces * ' ')) * self.width + '|'
        print strDelim
        for y in range(self.height):
            print '|' + ' '.join([format_num(self.d[(x, y)], nSpaces) for x in range(self.width)]) + '|'
        print strDelim

# The grid is basically a dictionary. We can treat this as a graph where each node has 4 neighbors.
# Each neighbor contributes an in-edge as well as an out-edge.
# You might want to use this to construct you solution
class Graph:
    def __init__(self, grid):
        self.grid = grid
    
    def vertices(self):
        return self.grid.keys()
    
    def adj(self, (x, y)):
        return [u for u in [(x+1, y), (x, y-1), (x-1, y), (x, y+1)] if u in self.grid.d.keys()]
    
    # put the value val for vertex u
    def putVal(self, u, val):
        self.grid.d[u] = val
    
    def getVal(self, u):
        return self.grid.d[u]

# Takes the grid and the points as arguments and returns a list of paths
# The grid represents the entire chip
# Each path represents the wire used to connect components represented by points
# Each path connects a pair of points in the points array; avoiding obstacles and other paths
# while minimizing the total path length required to connect all points
# If the points cannot be connected the function returns None
# def build_edges

# def a_star(graph, source, dest):
#     dist = {vertex: (graph.grid.height * graph.grid.width) for vertex in graph.vertices()}
#     parents = {vertext: None for vertext in graph.vertices()}
#     dist[source] = 0
#     q = graph.vertices().copy()
#     adj = {vertex: set() for vertex in graph.vertices()}
#     for
def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star(graph, start, goal):
    border = PriorityQueue()
    border.put(start, 0)
    parentVertex = {}
    totalCost = {}
    parentVertex[start] = None
    totalCost[start] = 0

    while not border.empty():
        current = border.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = totalCost[current] + graph.cost(current, next)
            if next not in totalCost or new_cost < totalCost[next]:
                totalCost[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                if next == goal:
                    border.put(next, priority)
                    parentVertex[next] = current
                elif graph.d[next] == 0:
                    border.put(next, priority)
                    parentVertex[next] = current

    return parentVertex

def reconstruct_path(parentVertex, start, goal):
    current = goal
    path = [current]
    while current != start:
        try:
            current = parentVertex[current]
        except KeyError:
            return None
        path.append(current)
    path.reverse()
    return path

def walk_path_update(grid, path):
    for x in path:
        if grid.d[x] == 0:
            grid.d[x] = -1
    grid.walls = grid.find_walls()

# def find_paths(grid, points):
#     result = []
#     for x,y in points:
#         print x,y
#         parentVertex = a_star(grid, x, y)
#         path = reconstruct_path(parentVertex, x, y)
#         walk_path_update(grid, path)
#         result.append(path)
            
#     return result

def try_points(grid, points):
    result = []
    for x,y in points:
        parentVertex = a_star(grid, x, y)
        path = reconstruct_path(parentVertex, x, y)
        if path:
            walk_path_update(grid, path)
            result.append(path)
        else:
            return None
    return result

def find_paths(grid, points):
    muts = permutations(points)
    for points in muts:
        attempt = try_points(grid, points)
        if attempt:
            return attempt
    return None
        
# check that the paths do not cross each other, or the obstacles; returns False if any path does so
def check_correctness(paths, obstacles):
    s = set()
    for path in paths:
        for (x, y) in path:
            if (x, y) in s: return False
            for o in obstacles:
                if (o[0] <= x <= o[2]) and (o[1] <= y <= o[3]):
                    return False
            s.add((x, y))
    return True

def main():
    # read all the chip related info from the input file
    with open(sys.argv[1]) as f:
        # first two lines are grid height and width 
        h = int(f.readline())
        w = int(f.readline())
        
        # third line is the number of obstacles; following numObst lines are the obstacle co-ordinates
        numObst = int(f.readline())
        obstacles = []
        for n in range(numObst):
            line = f.readline()
            obstacles.append([int(x) for x in line.split()])
        
        # read the number of points and their co-ordinates
        numPoints = int(f.readline())
        points = []
        for n in range(numPoints):
            line = f.readline()
            pts = [int(x) for x in line.split()]
            points.append(((pts[0], pts[1]), (pts[2], pts[3])))
    grid = dict(((x, y), 0) for x in range(w) for y in range(h))
    # lay out the obstacles
    for o in obstacles:
        for x in range(o[0], o[2] + 1):
            for y in range(o[1], o[3] + 1):
                grid[(x, y)] = -1
    
    cnt = 1 # route count
    for (s, d) in points:
        grid[s] = cnt
        grid[d] = cnt
        cnt += 1
    
    numPaths = cnt - 1
    g = Grid(w, h, grid)
    # print reconstruct_path(parentVertex, (13,11), (11,10))
    # parentVertex, totalCost = a_star(g, 15, 7)
        
    g.pretty_print_grid()
    print points
    
    paths = find_paths(g, points)
    if paths is None:
        print "Cannot connect all the points!"
    else:
        # check the correctness
        if not check_correctness(paths, obstacles):
            raise ("Incorrect solution, some path cross each other or the obstacles!")
        print "Paths:"
        totLength = 0
        for p in paths:
            print p
            totLength += len(p)
        print "Total Length: " + str(totLength)
    
if __name__ == "__main__":
    main()