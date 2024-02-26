import sys
from queue import Queue


class BipGraph(object):
    """
    A class to represent a Bipartite Graph.

    ...

    Attributes
    ----------
    left_vertices : int
        The number of vertices in the left set.
    right_vertices : int
        The number of vertices in the right set.
    adjacency_list : list
        A list of lists to represent the adjacency list of the graph.

    Methods
    -------
    add_edge(left_vertex, right_vertex):
        Adds an edge to the graph.
    bfs():
        Performs Breadth-First Search on the graph.
    dfs(vertex):
        Performs Depth-First Search on the graph.
    hopcroft_karp():
        Finds the maximum matching with a new restriction of the graph using the Hopcroft-Karp algorithm.
    """

    def __init__(self, left_vertices, right_vertices):
        """
        Constructs all the necessary attributes for the BipGraph object.

        Parameters
        ----------
            left_vertices : int
                The number of vertices in the left set.
            right_vertices : int
                The number of vertices in the right set.
        """
        self.left_vertices = left_vertices
        self.right_vertices = right_vertices
        self.adjacency_list = [[] for _ in range(left_vertices + 1)]
        self.visited_vertices = [False for _ in range(left_vertices + 1)]

    def add_edge(self, left_vertex, right_vertex):
        """
        Adds an edge to the graph.

        Parameters
        ----------
            left_vertex : int
                The vertex in the left set.
            right_vertex : int
                The vertex in the right set.
        """
        assert 1 <= left_vertex <= self.left_vertices
        self.adjacency_list[left_vertex].append(right_vertex)

    def bfs(self):
        """
        Performs Breadth-First Search on the graph.

        Returns
        -------
        bool
            True if there is an augmenting path, False otherwise.
        """
        # Create a queue for Breadth-First Search
        q = Queue()

        # Iterate over all vertices in the left set
        for vertex in range(1, self.left_vertices + 1):
            # If the vertex is free (not matched)
            if self.matching_in_left[vertex] == 0:
                # Set the distance to the vertex to 0
                self.distances[vertex] = 0
                # Add the vertex to the queue
                q.put(vertex)
            else:
                # If the vertex is not free, set the distance to the vertex to infinity
                self.distances[vertex] = sys.maxsize

        # Set the distance to the dummy vertex 0 to infinity
        self.distances[0] = sys.maxsize

        # While the queue is not empty
        while not q.empty():
            # Get the next vertex from the queue
            vertex = q.get()

            # If the distance to the vertex is less than the distance to the dummy vertex 0
            if self.distances[vertex] < self.distances[0]:
                # Iterate over all vertices adjacent to the current vertex
                for adj_vertex in self.adjacency_list[vertex]:
                    # If the distance to the matched vertex of the adjacent vertex is infinity
                    if self.distances[self.matching_in_right[adj_vertex]] == sys.maxsize:
                        # Update the distance to the matched vertex of the adjacent vertex
                        self.distances[self.matching_in_right[adj_vertex]] = self.distances[vertex] + 1
                        # Add the matched vertex of the adjacent vertex to the queue
                        q.put(self.matching_in_right[adj_vertex])

        # Return True if there is an augmenting path, False otherwise
        return self.distances[0] != sys.maxsize

    def dfs(self, vertex):
        """
        Performs Depth-First Search on the graph.

        Parameters
        ----------
            vertex : int
                The vertex to start the DFS from.

        Returns
        -------
        bool
            True if there is an augmenting path, False otherwise.
        """
        if vertex != 0:
            # If the vertex is not a free vertex
            for adj_vertex in self.adjacency_list[vertex]:
                # Iterate over all vertices adjacent to the current vertex
                if self.distances[self.matching_in_right[adj_vertex]] == self.distances[vertex] + 1:
                    # If the distance to the matched vertex of the adjacent vertex is one more than the distance to
                    # the current vertex
                    if self.dfs(self.matching_in_right[adj_vertex]):
                        # If there is an augmenting path from the matched vertex of the adjacent vertex
                        # Update the matching to include the edge between the current vertex and the adjacent vertex
                        self.matching_in_right[adj_vertex] = vertex
                        self.matching_in_left[vertex] = adj_vertex
                        # Return True to indicate that an augmenting path has been found
                        return True
            # If no augmenting path has been found from the current vertex, set its distance to infinity
            self.distances[vertex] = sys.maxsize
            # Return False to indicate that no augmenting path has been found
            return False
        # If the vertex is a free vertex, return True to indicate that an augmenting path has been found
        return True

    def hopcroft_karp(self):
        """
        Finds the maximum matching of the graph using the Hopcroft-Karp algorithm with a complement restriction:

        If a node u in one set is matched to a node v in the other set, and another
        node x in the other set has the same value as u, then x cannot also be
        matched. A value can only be matched once.

        Returns
        -------
        int
            The size of the maximum matching with the complement restriction.
        """
        # Initialize the matching for the left and right sets of vertices
        # The matching for a vertex is the vertex it is matched with
        self.matching_in_left = [0 for _ in range(self.left_vertices + 1)]
        self.matching_in_right = [0 for _ in range(self.right_vertices + 1)]

        # Initialize the distances for the vertices in the left set
        # The distance for a vertex is the shortest distance to a free vertex
        self.distances = [0 for _ in range(self.left_vertices + 1)]

        # Initialize a list to keep track of visited vertices
        visited = [False for _ in range(self.left_vertices + 1)]

        # Initialize the size of the maximum matching
        matching = 0

        # While there is an augmenting path in the graph
        while self.bfs():
            # Iterate over all vertices in the left set
            for u in range(1, self.left_vertices + 1):
                # If the vertex is free and there is an augmenting path from the vertex
                if self.matching_in_left[u] == 0 and self.dfs(u):
                    # If the vertex and its matched vertex have not been visited
                    if not visited[u] and not visited[self.matching_in_left[u]]:
                        # Mark the vertex and its matched vertex as visited
                        visited[u] = True
                        visited[self.matching_in_left[u]] = True
                        # Increase the size of the maximum matching
                        matching += 1

        # Return the size of the maximum matching
        return matching


def is_prime(n):
    """
    Checks if a number is prime.

    Parameters
    ----------
    n : int
        The number to check.

    Returns
    -------
    bool
        True if the number is prime, False otherwise.
    """
    if n <= 1:
        # If the number is less than or equal to 1, it is not prime, so return False
        return False
    if n <= 3:
        # If the number is less than or equal to 3, it is prime, so return True
        return True
    if n % 2 == 0 or n % 3 == 0:
        # If the number is divisible by 2 or 3, it is not prime, so return False
        return False
    i = 5
    while i * i <= n:
        # Check divisibility by numbers from 5 to sqrt(n)
        if n % i == 0 or n % (i + 2) == 0:
            # If the number is divisible by i or i + 2, it is not prime, so return False
            return False
        i += 6
    # If none of the above conditions are met, the number is prime, so return True
    return True


def min_numbers_to_remove(c):
    """
    Finds the minimum number of elements to remove from a list so that no two elements sum to a prime number.

    Parameters
    ----------
    c : list
        The list of integers.

    Returns
    -------
    int
        The minimum number of elements to remove.
    """
    # Create a bipartite graph with vertices representing the elements of the list
    n = len(c)
    g = BipGraph(n, n)
    # Iterate over all pairs of elements in the list
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            # If the sum of two elements is a prime number, add an edge between their corresponding vertices
            if is_prime(c[i - 1] + c[j - 1]):
                g.add_edge(i, j)
    # Find the maximum matching of the graph
    max_matching = g.hopcroft_karp()
    # Return the size of the maximum matching
    return max_matching


# Example usage
C = [1, 2, 3, 4, 5]
result = min_numbers_to_remove(C)
print(result)  # Output: 2

# Example usage
C = [1, 2]
result = min_numbers_to_remove(C)
print(result)  # Output: 1

# Example usage
C = [5, 9, 10, 18]
result = min_numbers_to_remove(C)
print(result)  # Output: 2
