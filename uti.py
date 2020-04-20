from collections import *

def DFS(matrix, v, f_v, f_e):
    '''run DFS on matrix staring at v, apply f_v to visited vertex, f_e to visitied edge'''
    def DFSUtil(v, visited, f_v, f_e, matrix, g):
        visited[v] = True
        f_v(v)
        # Recur for all the vertices
        # adjacent to this vertex
        for i in g[v]:
            if visited[i] == False:
                matrix[v][i] = f_e(matrix[v][i])
                matrix[i][v] = matrix[v][i]
                DFSUtil(i, visited, f_v, f_e, matrix, g)

    #generate the graph
    g = defaultdict(list)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] != 0:
                g[i].append(j)

    visited = [False] * (len(g))
    DFSUtil(v, visited, f_v, f_e, matrix, g)


# Returns true if the graph is a tree,
# else false.
def isTree(matrix):
    def isCyclicUtil(g, v, visited, parent):
        # Mark current node as visited
        visited[v] = True

        # Recur for all the vertices adjacent
        # for this vertex
        for i in g[v]:
            # If an adjacent is not visited,
            # then recur for that adjacent
            if visited[i] == False:
                if isCyclicUtil(g, i, visited, v) == True:
                    return True

            # If an adjacent is visited and not
            # parent of current vertex, then there
            # is a cycle.
            elif i != parent:
                return True

        return False
    # Mark all the vertices as not visited
    # and not part of recursion stack
    g = defaultdict(list)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if matrix[i][j] != 0:
                g[i].append(j)
    visited = [False] * (len(g))

    # The call to isCyclicUtil serves multiple
    # purposes. It returns true if graph reachable
    # from vertex 0 is cyclcic. It also marks
    # all vertices reachable from 0.
    if isCyclicUtil(g, 0, visited, -1) == True:
        return False

    # If we find a vertex which is not reachable
    # from 0 (not marked by isCyclicUtil(),
    # then we return false
    for i in range(len(g)):
        if visited[i] == False:
            return False

    return True

def Val(matrix):
    '''precheck if matrix is a valid T