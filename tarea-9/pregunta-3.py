import networkx as nx


def approx_vertex_cover(g):
    """
    Finds an approximate solution to the vertex cover problem using the maximum matching algorithm.
    This solution is guaranteed to be at most twice the size of the optimal solution.
    The time complexity of this algorithm could be over bound to O(|V|^4) where |V| is the number of vertices
    in the graph. Therefore, is a polynomial time algorithm.

    Parameters:
    g (nx.Graph): The input graph.

    Returns:
    set: The approximate solution to the vertex cover problem.
    """
    # Apply the maximum matching algorithm
    m = nx.maximal_matching(g)

    # Initialize an empty set for the approximate cover
    s_approx = set()

    # Go through each connection in the maximum match
    for u, v in m:
        # Add vertices u and v to the S_approx set
        s_approx.add(u)
        s_approx.add(v)

    # Return the S_approx set as the approximate solution of the vertex cover
    return s_approx


def main():
    # Read the number of vertices and edges
    n, m = map(int, input().split())

    # Create an empty graph
    g = nx.Graph()

    # Add the edges to the graph
    for _ in range(m):
        u, v = map(int, input().split())
        g.add_edge(u, v)

    # Get the approximate vertex cover
    s_approx = approx_vertex_cover(g)

    # Print the size of the approximate vertex cover
    print("Tamaño de la aproximación:", len(s_approx))
    # Print the vertices in the approximate vertex cover
    print("Vértices de la aproximación:")
    print(*s_approx)


if __name__ == "__main__":
    main()
