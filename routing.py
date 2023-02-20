# Ethan Hebert & Lucas Duran
# 2-24-23
# CSC-450
# Project - Link-State and Distance-Vector Routing

import sys

### FUNCTIONS ###
# convert the csv input to a topology matrix
def createMatrix(file):
    infile = open(file, "r")
    topology = []
    for line in infile:
        line = line.replace('\n', '')
        topology.append(line.split(','))
    infile.close()
    return topology

# get the source node, make sure it's one of the nodes in the topology
def getSrc(nodes):
    src = input("Please, provide the source node: ")
    if (src in nodes):
        return src
    else:
        print("This node is not found in the topology.\n")
        src = getSrc(nodes)
        return src

# link-state routing with Dijkstra's algorithm
def ls(topology,src):
    # initialization
    nodes = topology[0][1:]
    distances = {}
    previous = {}
    Nprime = [src]
    # get the distances to every neighbor of src
    # not a neighbor = 9999 (infinity)
    for i in range(len(topology[0])):
        if (topology[0][i] == src):
            srcRow = i
    for i in range(len(nodes)):
        distances[nodes[i]] = int(topology[srcRow][i+1])
        previous[nodes[i]] = src
    # loop until every node's least-cost path is known (all in Nprime)
    while (len(nodes) != len(Nprime)):
        # currNode holds the neighbor with the shortest path
        minimum = 9999
        for node in nodes:
            if not(node in Nprime):
                if (distances[node] < minimum):
                    currNode = node
                    minimum = distances[currNode]
        Nprime.append(currNode)
        break



    print("Shortest path tree for node {}:".format(src))

    print("Costs of the least-cost paths for node {}:".format(src))

# distance vector routing with Bellman-Ford equation
def dv(topology,src):
    srcIndex = topology[0][1:].index(str(src))
    nodes = topology[0][1 + srcIndex:]
    str1 = ""
    str2 = ""
    for node in range(len(nodes)):
        str1 += "Distance vector for node {}:".format(nodes[node])

        

        values = topology[node + srcIndex + 1][1:]
        for val in range(len(values)):
            str1 += " {}".format(values[val])

        allNodes = topology[0][1:]
        # Bellmand-Ford
        for j in range(1, len(allNodes)):
            allValues = topology[j][1:]
            neighbors = len(allValues) - allValues.count(9999) - 1

            # So now I know how many neighbors a node has, but I do not know who they are
            # I want a list with an X number of empty strings; X is the number of neighbors I know I have
            # nodeNeighbors = ["" for z in range(neighbors)] does that for me easily.

            nodeNeighbors = ["" for z in range(neighbors)]

            # then go through allValues list and get the index of the values that arent 0 or 9999
            # Add allNodes[allValues.index(number that is not 0 and 9999)] to nodeNeighbors list.
            # So for u: v, w, x values are not 0 or 9999, so get their indexes of 1, 2, and 3
            # and add to nodeNeighbors[0] = allNodes[1], 
            # nodeNeighbors[1] = allNodes [2], nodeNeighbors[2] = allNodes[3]
            # At the end, nodeNeighbors should be: ["v", "w", "x"]

            k = 0

            for val in allValues:
                if (val != 0 and val != 9999):
                    nodeNeighbors[k] = allNodes[allValues.index(val)]
                    k = k + 1


        #str2 += "Bellman-Ford for node    {}: {}\n".format(nodes[node], dist)

        str1 += "\n"
    print(str1)
    print()
    print(str2)

### MAIN ###
# check for proper input args
if (len(sys.argv) < 2):
    print("Correct Usage:\npython routing.py <filename.csv>")
else:
    # get the topology matrix
    topology = createMatrix(sys.argv[1])
    # get the source node
    src = getSrc(topology[0][1:])
    # link-state routing
    ls(topology,src)
    print()
    # distance vector routing
    dv(topology,src)
