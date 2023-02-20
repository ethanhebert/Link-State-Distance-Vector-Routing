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
    nodes = topology[0][1:]
    for node in range(len(nodes)):
        print("Distance vector for node {}: ".format(nodes[node]))

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