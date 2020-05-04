import networkx as nx
from parse import read_input_file, write_output_file
from Utility import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
import sys
import time
import multiprocessing

def solve(G, depth):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """
    result = []
    STs = genST(G, depth)
    print("STs gen!")
    i = 0
    for ST in STs:
        weight = 0
        for edge in ST.edges:
            weight += ST.edges[edge]['weight']
    for ST in STs:
        if i < depth:
            i += 1
            result += [starter(ST,G)]
    print("MDT gen!")
    result = sorted(result, key=lambda G: average_pairwise_distance_fast(G))
    #t = time.time() - start_time
    #print("total time takes:%d"%t)
    #print(result[0])
    return result[0]

def deletenode(T,O):
    oldcost = average_pairwise_distance_fast(T)
    leaves = []
    P = T.copy()
    for node in T.nodes:
        if T.degree[node] == 1:
            leaves += [node]
    leaves = sorted( leaves, key=lambda node: T.edges[ (list(T[node])[0], node) ]['weight'],reverse=True)
    for i in range(len(leaves)):
        G = T.copy()
        G.remove_node(leaves[i])
        if is_valid_network(O,G):
            newcost = average_pairwise_distance_fast(G)
            if newcost < oldcost:
                P = deletenode(G,O)
                return P
    return P


def starter(T,O):
    GraphArray = []
    oldcost = average_pairwise_distance_fast(T)
    leaves = []
    for node in T.nodes:
        if T.degree[node] == 1:
            leaves += [node]
    leaves = sorted( leaves, key=lambda node: T.edges[ (list(T[node])[0], node) ]['weight'],reverse=True)
    for i in range(len(leaves)):
        G = T.copy()
        G.remove_node(leaves[i])
        if is_valid_network(O,G):
            newcost = average_pairwise_distance_fast(G)
            if newcost < oldcost:
                GraphArray += [G]

    if len(GraphArray) < 2:
        return deletenode(T,O)
    elif len(GraphArray) == 2:
        return delete3node_S(GraphArray,O)
    else:
        return delete3node(GraphArray[:3], O)

def delete3node_S(GraphArray,O):
    newGraphArray = GraphArray.copy()
    for T in GraphArray:
        oldcost = average_pairwise_distance_fast(T)
        leaves = []
        for node in T.nodes:
            if T.degree[node] == 1:
                leaves += [node]
        leaves = sorted( leaves, key=lambda node: T.edges[ (list(T[node])[0], node) ]['weight'],reverse=True)
        cnt = 0
        for i in range(len(leaves)):
            if cnt < 3:
                G = T.copy()
                G.remove_node(leaves[i])
                if is_valid_network(O,G):
                    cnt += 1
                    newcost = average_pairwise_distance_fast(G)
                    if newcost < oldcost:
                        newGraphArray += [G]
    newGraphArray = sorted( newGraphArray, key=lambda tree: average_pairwise_distance_fast(tree))
    if len(newGraphArray) == 2:
        return newGraphArray[0]
    else:
        newGraphArray = newGraphArray[:3]
        return delete3node(newGraphArray,O)

def delete3node(GraphArray,O):
    newGraphArray = GraphArray.copy()
    for T in GraphArray:
        oldcost = average_pairwise_distance_fast(T)
        leaves = []
        for node in T.nodes:
            if T.degree[node] == 1:
                leaves += [node]
        leaves = sorted( leaves, key=lambda node: T.edges[ (list(T[node])[0], node) ]['weight'],reverse=True)
        cnt = 0
        for i in range(len(leaves)):
            if cnt < 3:
                G = T.copy()
                G.remove_node(leaves[i])
                if is_valid_network(O,G):
                    cnt += 1
                    newcost = average_pairwise_distance_fast(G)
                    if newcost < oldcost:
                        newGraphArray += [G]
    newGraphArray = sorted( newGraphArray, key=lambda tree: average_pairwise_distance_fast(tree))
    if len(newGraphArray) == 3:
        return newGraphArray[0]
    else:
        newGraphArray = newGraphArray[:3]
        return delete3node(newGraphArray,O)

def genST(G, depth):
    output = []
    outgraphs = []
    for u, v in G.edges:
        G.edges[u, v]['property'] = 'normal'
    List = {G}
    G.graph['MST'] = KruskalMST(G)
    MST = {tuple(G.graph['MST'])}
    if depth == -1:
        while len(MST) != 0:
            temp = min(List, key = lambda g: g.graph['cost'])
            output.append(temp.graph['MST'])
            List.remove(temp)
            MST.remove(tuple(temp.graph['MST']))
            Partition(temp, List, MST)
    else:
        while len(MST) != 0 and len(output) < depth:
            temp = min(List, key = lambda g: g.graph['cost'])
            output.append(temp.graph['MST'])
            List.remove(temp)
            MST.remove(tuple(temp.graph['MST']))
            Partition(temp, List, MST)


    for edges in output:
        P = nx.Graph()
        for edge in edges:
            P.add_edge(edge[0], edge[1])
            P.edges[edge[0], edge[1]]['weight'] = G.edges[edge[0], edge[1]]['weight']
        outgraphs += [P]
    return outgraphs

def Partition(P, List, MST):
    P1 = nx.Graph()
    P2 = nx.Graph()
    P1 = P.copy()
    P2 = P.copy()
    for u, v in P.graph['MST']:
        if P.edges[u, v]['property'] == 'normal':
            P1.edges[u, v]['property'] = 'excluded'
            P2.edges[u, v]['property'] = 'included'
            MSTP1 = KruskalMST(P1)
            P1.graph['MST'] = MSTP1
            #check if P1 is connected
            P3 = P1.copy()
            for u, v in P1.edges:
                if P1.edges[u, v]['property'] == 'excluded':
                    P3.remove_edge(u, v)
            if len(list(nx.dfs_edges(P3, source=1))) == P3.number_of_nodes() - 1:
                List.add(P1)
                MST.add(tuple(MSTP1))
            P1 = P2.copy()



def KruskalMST(P):
    G = P.copy()
    cost = 0

    normal_edges = [] #store all the normal edges
    result =[] #This will store the resultant MST
    i = 0 # An index variable, used for sorted edges
    e = 0 # An index variable, used for result[]


    for node in G.nodes:
        G.nodes[node]['parent'] = node
        G.nodes[node]['rank'] = 0

    for u, v in G.edges:
        if G.edges[u, v]['property'] == 'included':
            x = find(G, u)
            y = find(G ,v)
            union(G, x, y)
            result.append((u, v))
            e += 1
        elif G.edges[u, v]['property'] == 'excluded':
            G.edges[u, v]['weight'] = 1000
            normal_edges.append((u, v))
        else: normal_edges.append((u, v))

        # Step 1:  Sort all the edges in non-decreasing
            # order of their
            # weight.  If we are not allowed to change the
            # given graph, we can create a copy of graph
    if len(normal_edges) == 0:
        return result

    sortedges = sorted( normal_edges, key=lambda edge: G.edges[edge]['weight'])
    # Create V subsets with single elements



    # Number of edges to be taken is equal to V-1
    while e < G.number_of_nodes() - 1:

        # Step 2: Pick the smallest edge and increment
                # the index for next iteration
        if i > len(sortedges) - 1:
            return []
        u,v =  sortedges[i]

        i = i + 1
        x = find(G, u)
        y = find(G ,v)

        # If including this edge does't cause cycle,
                    # include it in result and increment the index
                    # of result for next edge
        if x != y:
            e = e + 1
            result.append((u,v))
            union(G, x, y)
        # Else discard the edge
    for i,j in result:
        cost += P.edges[i, j]['weight']
    P.graph['cost'] = cost
    P.graph['MST'] = result
    return result



def union(G, x, y):
    xroot = find(G, x)
    yroot = find(G, y)

    # Attach smaller rank tree under root of
    # high rank tree (Union by Rank)
    if G.nodes[xroot]['rank'] < G.nodes[yroot]['rank']:
        G.nodes[xroot]['parent'] = yroot
    elif G.nodes[xroot]['rank'] > G.nodes[yroot]['rank']:
        G.nodes[yroot]['parent'] = xroot

    # If ranks are same, then make one as root
    # and increment its rank by one
    else :
        G.nodes[yroot]['parent'] = xroot
        G.nodes[xroot]['rank'] += 1

def find(G, i):
    if G.nodes[i]['parent'] == i:
        return i
    return find(G, G.nodes[i]['parent'])

# Here's an example of how to run your solver.

# Usage: python3 solver.py

def solver_multi_threading(i, depth = 1):
    path = "inputs/{}-{}.in".format(i[0], i[1])
    
    G = read_input_file(path)
    print("Input  {} success!".format(path))
    T = solve(G, depth)
    #print("Average pairwise distance: {}".format(average_pairwise_distance_fast(T)))
    
    print("Output {} success!".format(path))
    write_output_file("outputs/{}-{}.out".format(i[0], i[1]), T)

def main():
    tt = sys.argv[1]
    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)

    task = []
    small_index = list(range(1, 304))
    med_index = list(range(304, 607))
    large_index = list(range(607, 1007))

    if tt == "all":
        task = large_index + med_index + small_index

    elif tt == 'small':
        task = small_index

    elif tt == 'medium':
        task = med_index

    elif tt == 'large':
        task = large_index

    pool.map(solver_multi_threading, task)

def p_main():
    path = sys.argv[1]
    f = open(path, 'r')
    lines = f.readlines()
    task = []
    for line in lines:
        (l, r) = line.split()
        (n, i) = l.split('-')
        i = int(i)
        print(n,i,r)
        if(int(r) > 10):
            task.append((n, i))

    cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=cores)
    pool.map(solver_multi_threading, task)

if __name__ == "__main__":
    p_main()
