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
    # Create a list of all the nodes, without an empty string before it
    allNodes = topology[0][1:] 
    
    # Create a list that will hold only the values to each node, without an empty string before it
    # This will be a list of lists
    allValues = [0 for q in range(len(allNodes))] 

    # Create a list to hold all of the nodes' neighbors
    # This will be a list of lists
    nodesNeighbors = ["" for c in range(len(allNodes))]

    # For loop that will iterate the number of nodes there are
    # Starts at 1 becuase it makes it a little bit easier here in the beginning since
    # there is the node it refers to on each row
    # It would be tricky to do j + 1 instead since it could land on an Index out of Range error
    for j in range(1, len(allNodes) + 1): # 6 iterations for topology-1

        # Create a list of the node's values to each of its neighbors
        values = topology[j][1:]

        # Variable that counts how many neighbors the node has
        neighborsNum = len(values) - values.count("9999") - 1

        # So now I know how many neighbors a node has, but I do not know who they are
        # I want a list with an X number of empty strings; X is the number of neighbors I know I have
        # neighbors = ["" for z in range(neighbors)] does that for me easily.

        neighbors = ["" for z in range(neighborsNum)]

        # then go through values list and get the index of the values that arent 0 or 9999
        # Add allNodes[index of number that is not 0 or 9999] to neighbors list.
        # Then add that neighbors list to the nodesNeighbors list of lists.
        # So for topology-1, u: v, w, x values are not 0 or 9999, so get their indexes of 1, 2, and 3
        # and add to neighbors[0] = allNodes[1], 
        # neighbors[1] = allNodes [2], neighbors[2] = allNodes[3]
        # At the end, neighbors for node u will be: ["v", "w", "x"]

        # k variable will keep track of where to put the neighbor node in neighbor list
        k = 0

        # valIndex will keep track of where the neighbor node is to give it to allNodes to put it in neighbor list
        valIndex = 0

        # Create a list of all the values for that node, so that it can be added to allValues list of lists
        myValues = [0 for w in range(len(allNodes))]
        
        # val should be an integer, but the way it is stored in the list, it is a string
        # so for the if statements, val needs to made an integer for the condition statements
        for val in values:

            # Add the value to the list myValues to keep all this node neighbor's values
            myValues[valIndex] = int(val)

            # If a value is not 0 and 9999, it is a neighbor, so add it to the neighbor list and increment k
            if (int(val) != 0 and int(val) != 9999):
                neighbors[k] = allNodes[valIndex]
                k = k + 1

            # Since val can be any number, this variable is needed to keep count of the loop's iterations
            valIndex = valIndex + 1

        # Add the node neighbor's values to the list, making it a list of lists
        # So allValues[0] is a list of all the neighbors' values of the first node
        # And int(allValues[0][0]) is an integer of the first value of the first node, which should be 0
        # For topology-1, this is a list that holds 6 lists that each hold 6 values
        # Make sure to make them integers before using them for if statements and such
        allValues[j - 1] = myValues

        # Add the node's neighbors to this list that will keep them, making it a list of lists
        # So nodesNeighbors[0] is a list of all the neighbors of the first node
        # And nodesNeighbors[0][0] is a string of the first neighbor of the first node.
        nodesNeighbors[j - 1] = neighbors

        # now what I want to do is go through each singular node and its neighbors
        # for u, it has 3 neighbors. Then calculate DV for u to u, u to v, u to w, u to x
        # so I probably want 2 nested for loops, or a funciton, the outside go through the node
        # the inside through its neighbors. A function might be needed since recursion might have to be used.
        # for instance, from u to z, if u goes to w, w then has to go to x or y which are neighbors of z
        # I can use the outside loop from j = 1 to len(allNodes) + 1 as the outside loop, but I
        # would not have access to the other nodes' neighbors.

        # need help making a function for this, I am struggling putting anything into code at this point.       
        
            

    str1 = ""
    # print statement at the end
    # will need to add another {} for the DV found
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
