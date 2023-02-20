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
    print("Shortest path tree for node {}:".format(src))

    print("Costs of the least-cost paths for node {}:".format(src))

# distance vector routing with Bellman-Ford equation
def dv(topology,src):
    srcIndex = topology[0][1:].index(str(src))
    nodes = topology[0][1 + srcIndex:]
    str1 = ""
    for node in range(len(nodes)):
        str1 += "Distance vector for node {}:".format(nodes[node])
        values = topology[node + srcIndex + 1][1:]
        for val in range(len(values)):
            str1 += " {}".format(values[val])
        str1 += "\n"
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
    dv(topology,src)
