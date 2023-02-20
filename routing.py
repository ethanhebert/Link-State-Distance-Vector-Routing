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
            break
    for i in range(len(nodes)):
        distances[nodes[i]] = int(topology[srcRow][i+1])
        previous[nodes[i]] = src
    # loop until every node's least-cost path is known (all in Nprime)
    while (len(nodes) != len(Nprime)):
        # currNode holds the next node with the shortest path
        minimum = 9999
        for node in nodes:
            if not(node in Nprime):
                if (distances[node] < minimum):
                    currNode = node
                    minimum = distances[currNode]
        Nprime.append(currNode)
        # update distances for all neighbors of currNode not in Nprime
        neighbors = []
        for i in range(len(topology[0])):
            if (topology[0][i] == currNode):
                currNodeRow = i
                break
        for i in range(len(topology[currNodeRow])):
            if (topology[currNodeRow][i] != '9999'):
                neighbors.append(topology[0][i])
        for i in range(len(nodes)):
            if not(nodes[i] in Nprime):
                if (nodes[i] in neighbors):
                    distances[nodes[i]] = min(distances[nodes[i]], 
                        distances[currNode] + int(topology[currNodeRow][i+1]))

    # print out the shortest path tree
    print("Shortest path tree for node {}:".format(src))

    # print out the least-cost paths (distances values)
    print("Costs of the least-cost paths for node {}:".format(src))
    output = ""
    for i in range(len(nodes)):
        output += nodes[i] + ":" + str(distances[nodes[i]])
        if (i != len(nodes)-1):
            output += ", "
    print(output)

# distance vector routing with Bellman-Ford equation
def dv(topology):
    str1 = ""

    allNodes = topology[0][1:]

    nodesNeighbors = ["" for c in range(len(allNodes))]

    for j in range(1, len(allNodes) + 1):
        allValues = topology[j][1:]
        neighborsNum = len(allValues) - allValues.count("9999") - 1

        # So now I know how many neighbors a node has, but I do not know who they are
        # I want a list with an X number of empty strings; X is the number of neighbors I know I have
        # neighbors = ["" for z in range(neighbors)] does that for me easily.

        neighbors = ["" for z in range(neighborsNum)]

        # then go through allValues list and get the index of the values that arent 0 or 9999
        # Add allNodes[allValues.index(number that is not 0 or 9999)] to neighbors list.
        # So for u: v, w, x values are not 0 or 9999, so get their indexes of 1, 2, and 3
        # and add to neighbors[0] = allNodes[1], 
        # neighbors[1] = allNodes [2], neighbors[2] = allNodes[3]
        # At the end, nodeNeighbors should be: ["v", "w", "x"]

        k = 0
        valIndex = 0
        
        for val in allValues:    
            if (int(val) != 0 and int(val) != 9999):
                neighbors[k] = allNodes[valIndex]
                k = k + 1
            if (k == neighborsNum):
                break
            valIndex = valIndex + 1
        nodesNeighbors[j - 1] = neighbors
        
    for node in range(len(allNodes)):
        str1 += "Distance vector for node {}:\n".format(allNodes[node])
        
    print(str1)

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
    dv(topology)
