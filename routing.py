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
        print("Shortest path tree for node {}:".format(src))
        return src
    else:
        print("This node is not found in the topology.\n")
        src = getSrc(nodes)
        return src


### MAIN ###
# check for proper input args
if (len(sys.argv) < 2):
    print("Correct Usage:\npython routing.py <filename.csv>")
else:
    # convert the csv input to a topology matrix
    topology = createMatrix(sys.argv[1])
    # get the source node
    src = getSrc(topology[0])