# -*- coding: utf-8 -*-
import collections
import time

product = []
users = []
maxWidth = 0
maxHeight = 0
warehouseMap = []
        
    
class Product:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
    def getID(self):
        return self.id
    def getPosition(self):
        return (self.x, self.y)
    
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.map = [[0]*width for i in range(height)]
        
    def addShelves(self, product):
        for p in product:
            (x, y) = p.getPosition()
            self.map[y][x] = 1
        

    
def initWarehouse():
    global product
    global maxWidth
    global maxHeight
    
    lines = []
    #with open('warehouse.txt','r') as f:
    with open('qvBox-warehouse-data-f21-v01.txt', 'r') as f:
        title = f.readline()
        lines = f.read().splitlines()
    for line in lines:
        info = line.split("\t")
        x = int(float(info[1]))
        maxWidth = x if x > maxWidth else maxWidth
        y = int(float(info[2]))
        maxHeight = y if y > maxHeight else maxHeight
        product.append(Product(info[0], x, y))
    map = [[0] * (maxWidth + 1) for i in range(maxHeight + 1)]
    for p in product:
        (x, y) = p.getPosition()
        map[y][x] = 1
    global  warehouseMap
    warehouseMap = map

def bfs(map, start, end):
    explored = []
    queue = [[start]]

    if start == end:
        # print("Same Node")
        return []

    while queue:
        path = queue.pop(0)
        node = path[-1]
        x, y = node

        if node not in explored:
            neighbours = findNeighbours(map, node)
            for neighbour in neighbours:
                new_path = list(path)
                new_path.append(neighbour)
                queue.append(new_path)
                if neighbour == end:
                    # print("Shortest path = ", *new_path)
                    return new_path
            explored.append(node)

    # print("Can't find any path between these two points")
    return []

def findNeighbours(map, location):
    neighbours = []
    h = len(map)
    w = len(map[0])
    x, y = location
    if x + 1 < w and map[y][x+1] != 1:
        neighbours.append((x+1, y))
    if x - 1 >= 0 and map[y][x-1] != 1:
        neighbours.append((x-1, y))

    if y + 1 < h and map[y+1][x] != 1:
        neighbours.append((x, y+1))

    if y - 1 >= 0 and map[y-1][x] != 1:
        neighbours.append((x, y-1))
    return neighbours


bfroutelist = []
def generateBfroutelist(node,productLocList,path):

    path.append(node)
    if (len(productLocList) + 1 == len(path)):
        bfroutelist.append(path[1:])
    else:
        for product in productLocList:
            if (product not in path):
                generateBfroutelist(product, productLocList, list(path))


def bfneighbours(bfroute, map) :
    neighbours = []
    for node in bfroute:
        neighbours.append(findNeighbours(map, node))
    return neighbours

bfroutes=[]
bfdict = {(0,0): {(0,0) : 0}
}

def bfonepath(node, neighbours, path, distance, end):
    path.append(node)

    # Calculate path length from current to last node
    if len(path) > 1:
        if (node in bfdict and path[-2] in bfdict[node]):
            distance += bfdict[node][path[-2]]
        elif (path[-2] in bfdict and node in bfdict[path[-2]]):
            distance += bfdict[path[-2]][node]
        else:
            length = len(bfs(warehouseMap, path[-2], node)) - 1
            distance += length
            bfdict[path[-2]] = {node: length}
        # distance += len(bfs(warehouseMap, path[-2], node)) - 1
    # If path contains all cities and is not a dead end,
    # add path from last to first city and return.
    if (len(neighbours) + 1 == len(path)):
        path.append(end)
        if (end in bfdict and path[-2] in bfdict[end]):
                distance += bfdict[end][path[-2]]
        elif (path[-2] in bfdict and end in bfdict[path[-2]]):
                distance += bfdict[path[-2]][end]
        else:
            length = len(bfs(warehouseMap, path[-2], end)) - 1
            distance += length
            bfdict[path[-2]] = {end: length}
        # distance += len(bfs(warehouseMap, path[-2], end)) - 1
        global bfroutes
        bfroutes.append([distance, path])
        bfroutes.sort()
        best = bfroutes[0]
        bfroutes = []
        bfroutes.append(best)
        return

    # Fork paths for all possible cities not yet used
    for neighbour in neighbours:
        i = 0
        for n in neighbour:
            if (n not in path) :
                i += 1
        if ( i== len(neighbour)):
            for n in neighbour:
                bfonepath(n, neighbours, list(path), distance, end)

def bfallpath(start, end, productLocList):
    productLocList1 = []
    for i in productLocList:
        if not i in productLocList1:
            productLocList1.append(i)
    generateBfroutelist(start, productLocList1, [])
    for route in bfroutelist:
        neighbour = bfneighbours(route, warehouseMap)
        bfonepath(start, neighbour, [], 0, end)
    shortestpath,shortestdistance = bfroutes[0]
    return shortestpath,shortestdistance
        
        
if __name__ == '__main__':
    time_start = time.time()
    productLocList=[]
    initWarehouse()
    warehouse = Map(maxWidth + 1, maxHeight + 1)
    warehouse.addShelves(product)

    h = warehouse.height
    w = warehouse.width
    
    for i in warehouse.map:
        print(i)
        print("\n")
    for p in product:
        if (p.getID() == '108335' or p.getID() == '391825' or p.getID() == '340367' or p.getID() == '286457' or p.getID() == '286457'):
        # or
        # p.getID() == '287261' or p.getID() == '76283' or p.getID() == '254489' or p.getID() == '258540' or p.getID() == '286457'):
            productLocList.append(p.getPosition())
    shortestdisctance,shortestpath = bfallpath((0,0), (0,0), productLocList)
    print(shortestpath)
    print(shortestdisctance)
    time_end = time.time()
    print('time cost', time_end - time_start, 's')
    
    
    # while True:
    #     try:
    #         find = 0
    #         id = input("\nEnter Product ID:")
    #         for i in product:
    #             if i.getID() == id:
    #                 print(i.getPosition())
    #                 find = 1
    #         if not find:
    #             print("product not found")
    #     except Exception as e:
    #         print(e)
                
