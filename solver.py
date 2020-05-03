import networkx as nx
from parse import read_input_file, write_output_file
from utility import is_valid_network, average_pairwise_distance, average_pairwise_distance_fast
import sys
import time

def solve(G, times = 100):
    """
    Args:
        G: networkx.Graph

    Returns:
        T: networkx.Graph
    """

    # TODO: your code here!
    start_time = time.time()

    result = []
    STs = genST(G,times)
    print("STs gen!")
    i = 0

    for ST in STs:
        weight = 0
        for edge in ST.edges:
            weight += ST.edges[edge]['weight']
        print(ST.edges)
        print(weight)
        print(nx.is_tree(ST))
    print("__________________________________")
    for ST in STs:
        print(ST.edges)
        if i < times:
            i += 1
            result += [deletenode(ST,G)]
    print("min deo-tree gen!")
    result = sorted(result, key=lambda G: average_pairwise_distance_fast(G))
    t = time.time() - start_time
    print("total time takes:%d"%t)
    print(result[0])
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
            else:
                return P
    return P




def genST(G, times = 100):
    output = []
    outgraphs = []
    for u, v in G.edges:
        G.edges[u, v]['property'] = 'normal'
    List = {G}
    G.graph['MST'] = KruskalMST(G)
    MST = {tuple(G.graph['MST'])}
    while len(MST) != 0 and len(output) < times:
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

# Usage: python3 solver.py test.in

if __name__ == '__main__':
    path = "self_test/2.in"
    G = read_input_file(path)
    print("Input success!")
    T = solve(G, 50)
    print("Average  pairwise distance: {}".format(average_pairwise_distance_fast(T)))
    write_output_file('test.out',T)
