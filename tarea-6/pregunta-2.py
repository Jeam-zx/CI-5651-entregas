import numpy as np

# HL Decomposition Implementation is based on the following resources:
# https://www.geeksforgeeks.org/implementation-of-heavy-light-decomposition/

N = 11  # Number of nodes in the tree

# Matrix representing the tree
# Not included in the space complexity of the algorithm as it is an input
tree = np.full((N, N), -1)


class Node:
    """
    A class to represent a node in a tree.

    Attributes
    ----------
    par : int
        Parent of this node
    depth : int
        Depth of this node
    size : int
        Size of subtree rooted with this node
    pos_segbase : int
        Position in segment tree base
    chain : int
        Chain of this node
    """

    def __init__(self):
        self.par = None
        self.depth = None
        self.size = None
        self.pos_segbase = None
        self.chain = None


node = [Node() for _ in range(N)]


class Edge:
    """
    A class to represent an edge in a tree.

    Attributes
    ----------
    weight : int
        Weight of Edge
    deeper_end : int
        Deeper end of the edge
    """

    def __init__(self):
        self.weight = None
        self.deeper_end = None


edge = [Edge() for _ in range(N)]


class SegmentTree:
    """
    A class to represent a Segment Tree.

    Attributes
    ----------
    base_array : numpy array
        Base array of the segment tree
    tree : numpy array
        Array to store the segment tree
    """

    def __init__(self):
        self.base_array = np.zeros(N)
        self.tree = np.zeros(6 * N)


s = SegmentTree()


def addEdge(e, u, v, w):
    """
    Function to add an edge to the tree.

    Parameters
    ----------
    e : int
        Edge number
    u : int
        Node u
    v : int
        Node v
    w : int
        Weight of the edge
    """
    tree[u - 1][v - 1] = e - 1
    tree[v - 1][u - 1] = e - 1
    edge[e - 1].weight = w


def dfs(curr, prev, dep, n):
    """
    Recursive function for DFS on the tree.

    Parameters
    ----------
    curr : int
        Current node
    prev : int
        Previous node
    dep : int
        Depth of the current node
    n : int
        Total number of nodes
    """
    node[curr].par = prev
    node[curr].depth = dep
    node[curr].size = 1

    for j in range(n):
        if j != curr and j != node[curr].par and tree[curr][j] != -1:
            edge[tree[curr][j]].deeper_end = j
            dfs(j, curr, dep + 1, n)
            node[curr].size += node[j].size


def hld(curr_node, id, edge_counted, curr_chain, n, chain_heads):
    """
    Recursive function that decomposes the Tree into chains.

    Parameters
    ----------
    curr_node : int
        Current node
    id : int
        ID of the edge
    edge_counted : list
        List to keep track of the edges counted
    curr_chain : list
        List to keep track of the current chain
    n : int
        Total number of nodes
    chain_heads : numpy array
        Array to store the heads of the chains
    """
    if chain_heads[curr_chain[0]] == -1:
        chain_heads[curr_chain[0]] = curr_node

    node[curr_node].chain = curr_chain[0]
    node[curr_node].pos_segbase = edge_counted[0]
    s.base_array[edge_counted[0]] = edge[id].weight
    edge_counted[0] += 1

    spcl_chld = -1
    spcl_edg_id = None
    for j in range(n):
        if j != curr_node and j != node[curr_node].par and tree[curr_node][j] != -1:
            if spcl_chld == -1 or node[spcl_chld].size < node[j].size:
                spcl_chld = j
                spcl_edg_id = tree[curr_node][j]

    if spcl_chld != -1:
        hld(spcl_chld, spcl_edg_id, edge_counted, curr_chain, n, chain_heads)

    for j in range(n):
        if j != curr_node and j != node[curr_node].par and j != spcl_chld and tree[curr_node][j] != -1:
            curr_chain[0] += 1
            hld(j, tree[curr_node][j], edge_counted, curr_chain, n, chain_heads)


def construct_ST(ss, se, si):
    """
    Recursive function that constructs Segment Tree for array[ss..se).

    Parameters
    ----------
    ss : int
        Start of the segment
    se : int
        End of the segment
    si : int
        Index in the segment tree
    """
    if ss == se - 1:
        s.tree[si] = s.base_array[ss]
        return s.base_array[ss]

    mid = (ss + se) // 2
    s.tree[si] = max(construct_ST(ss, mid, si * 2), construct_ST(mid, se, si * 2 + 1))
    return s.tree[si]


def LCA(u, v, n):
    """
    Function to find the Lowest Common Ancestor (LCA) of two nodes.

    Parameters
    ----------
    u : int
        Node u
    v : int
        Node v
    n : int
        Total number of nodes
    """
    LCA_aux = np.full(n + 5, -1)

    if node[u].depth < node[v].depth:
        u, v = v, u

    while u != -1:
        LCA_aux[u] = 1
        u = node[u].par

    while v:
        if LCA_aux[v] == 1:
            break
        v = node[v].par

    return v


def RMQUtil(ss, se, qs, qe, index):
    """
    Utility function for Range Maximum Query (RMQ). It uses the Segment Tree built by the construct_ST function.

    Parameters:
    ss (int): Starting index of the segment of the input array.
    se (int): Ending index of the segment of the input array.
    qs (int): Starting index of the query range.
    qe (int): Ending index of the query range.
    index (int): Index of the current node in the Segment Tree.

    Returns:
    int: Maximum value in the given range.
    """
    if qs <= ss and qe >= se - 1:
        return s.tree[index]

    if se - 1 < qs or ss > qe:
        return -1

    mid = (ss + se) // 2
    return max(RMQUtil(ss, mid, qs, qe, 2 * index), RMQUtil(mid, se, qs, qe, 2 * index + 1))


def RMQUtilMin(ss, se, qs, qe, index):
    """
    Utility function for Range Minimum Query (RMQ). It uses the Segment Tree built by the construct_ST function.

    Parameters:
    ss (int): Starting index of the segment of the input array.
    se (int): Ending index of the segment of the input array.
    qs (int): Starting index of the query range.
    qe (int): Ending index of the query range.
    index (int): Index of the current node in the Segment Tree.

    Returns:
    int: Minimum value in the given range.
    """
    if qs <= ss and qe >= se - 1:
        return s.tree[index]

    if se - 1 < qs or ss > qe:
        return float('inf')

    mid = (ss + se) // 2
    return min(RMQUtilMin(ss, mid, qs, qe, 2 * index), RMQUtilMin(mid, se, qs, qe, 2 * index + 1))


def RMQ(qs, qe, n):
    """
    Function to get the maximum value in a given range. It uses the RMQUtil function to find the maximum value.

    Parameters:
    qs (int): Starting index of the query range.
    qe (int): Ending index of the query range.
    n (int): Total number of nodes.

    Returns:
    int: Maximum value in the given range.
    """
    if qs < 0 or qe > n - 1 or qs > qe:
        print("Invalid Input")
        return -1

    return RMQUtil(0, n, qs, qe, 1)


def RMQMin(qs, qe, n):
    """
    Function to get the minimum value in a given range. It uses the RMQUtilMin function to find the minimum value.

    Parameters:
    qs (int): Starting index of the query range.
    qe (int): Ending index of the query range.
    n (int): Total number of nodes.

    Returns:
    int: Minimum value in the given range.
    """
    if qs < 0 or qe > n - 1 or qs > qe:
        print("Invalid Input")
        return float('inf')

    return RMQUtilMin(0, n, qs, qe, 1)


def crawl_tree(u, v, n, chain_heads):
    """
    Function to crawl up the tree from node u to node v. It uses the RMQ function to find the maximum value in the path.

    Parameters:
    u (int): Node u.
    v (int): Node v.
    n (int): Total number of nodes.
    chain_heads (numpy array): Array to store the heads of the chains.

    Returns:
    int: Maximum value in the path from node u to node v.
    """
    chain_v = node[v].chain
    ans = 0

    while True:
        chain_u = node[u].chain

        if chain_u == chain_v:
            if u != v:
                ans = max(RMQ(node[v].pos_segbase + 1, node[u].pos_segbase, n), ans)
            break

        else:
            ans = max(ans, RMQ(node[chain_heads[chain_u]].pos_segbase, node[u].pos_segbase, n))
            u = node[chain_heads[chain_u]].par

    return ans


def crawl_tree_min(u, v, n, chain_heads):
    """
    Function to crawl up the tree from node u to node v. It uses the RMQMin function to find the minimum value in the path.

    Parameters:
    u (int): Node u.
    v (int): Node v.
    n (int): Total number of nodes.
    chain_heads (numpy array): Array to store the heads of the chains.

    Returns:
    int: Minimum value in the path from node u to node v.
    """
    chain_v = node[v].chain
    ans = float('inf')

    while True:
        chain_u = node[u].chain

        if chain_u == chain_v:
            if u != v:
                ans = min(RMQMin(node[v].pos_segbase + 1, node[u].pos_segbase, n), ans)
            break

        else:
            ans = min(ans, RMQMin(node[chain_heads[chain_u]].pos_segbase, node[u].pos_segbase, n))
            u = node[chain_heads[chain_u]].par

    return ans


def maxEdge(u, v, n, chain_heads):
    """
    Function to find the maximum edge value in the path from node u to node v.

    Parameters:
    u (int): Node u.
    v (int): Node v.
    n (int): Total number of nodes.
    chain_heads (numpy array): Array to store the heads of the chains.

    Returns:
    int: Maximum edge value in the path from node u to node v.
    """
    lca = LCA(u, v, n)
    return max(crawl_tree(u, lca, n, chain_heads), crawl_tree(v, lca, n, chain_heads))


def minEdge(u, v, n, chain_heads):
    """
    Function to find the minimum edge value in the path from node u to node v.

    Parameters:
    u (int): Node u.
    v (int): Node v.
    n (int): Total number of nodes.
    chain_heads (numpy array): Array to store the heads of the chains.

    Returns:
    int: Minimum edge value in the path from node u to node v.
    """
    lca = LCA(u, v, n)
    return min(crawl_tree_min(u, lca, n, chain_heads), crawl_tree_min(v, lca, n, chain_heads))


def bool_to_int(b):
    """
    Function to convert a boolean value to an integer.

    Parameters:
    b (bool): Boolean value.

    Returns:
    int: Integer representation of the boolean value.
    """
    return 1 if b else 0


def print_tree():
    """
    Function to print the tree.
    """
    for i in range(N):
        print(tree[i])


def forall(u, v, n, chain_heads):
    """
    Function to check if all connections between nodes u and v result in true.

    Parameters:
    u (int): Node u.
    v (int): Node v.
    n (int): Total number of nodes.
    chain_heads (numpy array): Array to store the heads of the chains.

    Returns:
    bool: True if all connections result in true, False otherwise.
    """
    if minEdge(u - 1, v - 1, n, chain_heads) == 1:
        print(f"todas las conexiones entre los nodos {u} y {v} resultan en true.")
        return True
    else:
        print(f"al menos una de las conexiones entre los nodos {u} y {v} resulta en false.")
        return False


def exists(u, v, n, chain_heads):
    """
    Function to check if any connection between nodes u and v results in true.

    Parameters:
    u (int): Node u.
    v (int): Node v.
    n (int): Total number of nodes.
    chain_heads (numpy array): Array to store the heads of the chains.

    Returns:
    bool: True if any connection results in true, False otherwise.
    """
    if maxEdge(u - 1, v - 1, n, chain_heads) == 1:
        print(f"alguna de las conexiones entre los nodos {u} y {v} resulta en true.")
        return True
    else:
        print(f"ninguna de las conexiones entre los nodos {u} y {v} resulta en true.")
        return False

def main():
    # Example usage - Edges of the tree
    e = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (3, 7), (4, 8), (4, 9), (5, 10), (5, 11)]
    #         1
    #       /    \
    #      2      3
    #    /  \    / \
    #   4    5  6   7
    #  / \  / \
    # 8  9 10 11

    # predicated value of the edges
    p = [True, False, True, False, True, False, True, False, True, True]

    # Adding edges to the tree
    for i in range(N - 1):
        addEdge(i + 1, e[i][0], e[i][1], bool_to_int(p[i]))

    # Root of the tree
    root = 0
    parent_of_root = -1
    depth_of_root = 0

    dfs(root, parent_of_root, depth_of_root, N)

    # Chain heads
    chain_heads = np.full(N, -1)

    edge_counted = [0]
    curr_chain = [0]

    # Heavy-Light Decomposition
    hld(root, N - 1, edge_counted, curr_chain, N, chain_heads)

    # Construct Segment Tree
    construct_ST(0, edge_counted[0], 1)

    # Example usage
    x, y = 1, 11 # Nodes to check
    forall(x, y, N, chain_heads)
    exists(x, y, N, chain_heads)


if __name__ == "__main__":
    main()
