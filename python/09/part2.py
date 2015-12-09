import operator 

# Helper function to add or update a key to the dictionary
def addDistance(key, info, dictionary):
    if key in dictionary:
        dictionary[key].update(info)
    else:
        dictionary[key] = info

# Reads the file and creates a dictionary (graph) with all the locations and distances
# the Graph looks like:
# {
#     'Dublin': {
#         'Belfast': 141,
#         'London': 464
#     },
#     'London': {
#         'Belfast': 518,
#         'Dublin': 464
#     },
#     'Belfast': {
#         'Dublin': 141,
#         'London': 518
#     }
# }
def createGraph():
    distances = {}
    with open('input.txt') as f:
        for line in f:
            # Remove all whitespaces and replace the = with 'to' so it's easier to split
            # this can probably be done with a regular expression like re.split('(=|to)') after removing white spaces
            line = line.strip().replace(" ", "").replace('=', 'to')
            # split each line into a list [place1, place2, distance]
            info = line.split("to")

            place1 = info[0]
            place2 = info[1]
            distance = int(info[2])

            # add both distances, from place 1 and from place 2 so it's easier to find later
            addDistance(place1, { place2 : distance }, distances)
            addDistance(place2, { place1 : distance }, distances)

    return distances

# This is my implementation of the nearest neighbour algorithm
# https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm
def nearestNeighbour(graph, start):
    visited = []
    current = start
    totalDistance = 0

    visited.append(start)
    # while we didn't visit all the nodes
    while len(visited) < len(graph):
        # get all distances from the current node
        routes = graph[current]
        # sort the dictionary by the value from min distance to max
        sortedRoutes = sorted(routes.items(), key=operator.itemgetter(1), reverse=True)
        
        closest = None
        # Find the minimum distance of the nodes that we didn't visit yet
        for item in sortedRoutes:
            closest, distance = item
            if  closest not in visited:
                current = closest
                visited.append(closest)
                totalDistance += distance
                break
        # If we didn't find it, go out of this
        if not closest:
            break
    # return the total distance traveled and the path (as a list)
    return totalDistance, visited


#
# Main program
#

# get distances
distances = createGraph()
minDistance = 0
minPath = []

# get the minimum route from all the nodes in the graph
for key in distances:
    distance, path = nearestNeighbour(distances, key)
    if distance > minDistance:
        minDistance = distance
        minPath = path

print minDistance, minPath
