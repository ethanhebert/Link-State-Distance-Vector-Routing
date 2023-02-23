# Ethan Hebert & Lucas Duran
# 2-24-23
# CSC-450
# Project - Link-State and Distance-Vector Routing

# import library for taking user input args
import sys

### FUNCTIONS ###
# convert the csv input to a topology matrix
def createMatrix(file):
    infile = open(file, "r")
    topology = []
    for line in infile:
        # parse through commas in csv, insert into 2D matrix
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
                    oldCost = distances[nodes[i]]
                    newCost = distances[currNode] + int(topology[currNodeRow][i+1])
                    # here tracks previous nodes for shortest path tree
                    # oldCost is smaller, shortest path remains the same
                    if (oldCost <= newCost):
                        pass
                    # newCost is smaller, shortest path updates to the path to the 
                    # currNode plus the currNode
                    else:
                        distances[nodes[i]] = newCost
                        previous[nodes[i]] = previous[currNode] + currNode

    # print out the shortest path tree
    print("Shortest path tree for node {}:".format(src))
    output = ""
    for node in Nprime:
        if (node != src):
            output += previous[node] + node
            if (node != Nprime[len(Nprime)-1]):
                output += ", "
    print(output)

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
    # list of all nodes
    nodes = topology[0][1:]

    # initialization - compute distance vectors
    # nodesdvs is a 3D matrix holds every node's distance vectors for itself and all its neighbors
    nodesdvs = []
    for i in range(len(nodes)):
        # nodedvs holds this current node's distance vectors for itself and all its neighbors
        nodedvs = []
        for j in range(len(nodes)):
            # dv holds the current distance vector
            dv = []
            # if you are on the current selected node, this index stores this node's own distance vector
            if (topology[i+1][j+1] == '0'):
                for k in range(len(nodes)):
                    dv.append(int(topology[j+1][k+1]))
            # check if these 2 nodes are neighbors to add an infinity-filled distance vector for a neighbor
            elif (topology[i+1][j+1] != '9999'):
                for k in range(len(nodes)):
                    dv.append(9999)
            nodedvs.append(dv)
        nodesdvs.append(nodedvs)
    
    # neighbors is a 2D matrix holding bools saying if 2 nodes are neighbors or not
    neighbors = []
    for i in range(len(nodes)):
        # nodeNeighbors holds this current node's neighbors
        nodeNeighbors = []
        for j in range(len(nodes)):
            if (topology[i+1][j+1] != '0' and topology[i+1][j+1] != '9999'):
                nodeNeighbors.append(True)
            else:
                nodeNeighbors.append(False)
        neighbors.append(nodeNeighbors)

    # go thru every node and simulate "sending" a distance vector to all its neighbors
    # perform BF equation with these receieved distance vectors
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if (neighbors[i][j]):
                senddv(nodes,nodesdvs,neighbors,i,j)

    # print out each node's final distance vector
    for i in range(len(nodes)):
        dv = ""
        for j in range(len(nodes)):
            dv += str(nodesdvs[i][i][j]) + " "
        print("Distance vector for node {}: {}".format(nodes[i],dv))

# This is a recursively called function that sends distance vectors to nodes' neighbors
# and performs the BF equation to calculate the shortest routes
# s is for sender, r is for receiver
def senddv(nodes,nodesdvs,neighbors,s,r):
    # dvChange = bool to hold if a distance vector changed, if true recursive call w neighbors, if false stop here
    # sdv = sender distance vector, rdv = receiver distance vector
    # stor is the distance from sender to receiver
    dvChange = False
    sdv = nodesdvs[s][s]
    rdv = nodesdvs[r][r]
    stor = rdv[s]

    # update the receiver's dv for the sender's node with sdv
    nodesdvs[r][s] = sdv

    # Bellman-Ford equation on each value in receiving distance vector
    for i in range(len(rdv)):
        # updated smaller value
        if (sdv[i]+stor < rdv[i]):
            nodesdvs[r][r][i] = sdv[i]+stor
            dvChange = True

    # if receiver's distance vector changed, send to neighbors
    if (dvChange):
        for i in range(len(nodes)):
            if (neighbors[r][i]):
                senddv(nodes,nodesdvs,neighbors,r,i)

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