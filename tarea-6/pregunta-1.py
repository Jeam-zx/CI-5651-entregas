import random


# Treap implementation based on the code
# from https://cp-algorithms.com/data_structures/treap.html
# The code has been modified to support multi-swap operations on the treap
class Node:
    """
    A class to represent a node in a treap.

    Attributes
    ----------
    value : int
        the value of the node
    prior : float
        a random priority assigned to the node
    cnt : int
        the count of nodes in the subtree rooted at this node
    l : Node
        the left child of the node
    r : Node
        the right child of the node
    """

    def __init__(self, value):
        self.prior = random.random()
        self.value = value
        self.cnt = 1
        self.l = None
        self.r = None


def cnt(it):
    """
    Function to get the count of nodes in the subtree rooted at a node.

    Parameters
    ----------
    it : Node
        the node whose subtree's count is to be returned

    Returns
    -------
    int
        the count of nodes in the subtree rooted at 'it'
    """
    return it.cnt if it else 0


def upd_cnt(it):
    """
    Function to update the count of nodes in the subtree rooted at a node.

    Parameters
    ----------
    it : Node
        the node whose subtree's count is to be updated
    """
    if it:
        it.cnt = cnt(it.l) + cnt(it.r) + 1


def merge(l, r):
    """
    Function to merge two treaps.

    Parameters
    ----------
    l : Node
        the root of the left treap
    r : Node
        the root of the right treap

    Returns
    -------
    Node
        the root of the merged treap
    """
    if not l or not r:
        return l if l else r
    elif l.prior > r.prior:
        l.r = merge(l.r, r)
        upd_cnt(l)
        return l
    else:
        r.l = merge(l, r.l)
        upd_cnt(r)
        return r


def split(t, key, add=0):
    """
    Function to split a treap into two treaps.

    Parameters
    ----------
    t : Node
        the root of the treap to be split
    key : int
        the value based on which the treap is to be split
    add : int, optional
        the count of nodes in the left subtree of 't' (default is 0)

    Returns
    -------
    Node, Node
        the roots of the two treaps resulting from the split
    """
    if not t:
        return None, None
    cur_key = add + cnt(t.l)
    if key <= cur_key:
        l, t.l = split(t.l, key, add)
        r = t
    else:
        t.r, r = split(t.r, key, add + 1 + cnt(t.l))
        l = t
    upd_cnt(t)
    return l, r


def output(t):
    """
    Function to print the values in the treap rooted at 't' in in-order traversal.

    Parameters
    ----------
    t : Node
        the root of the treap
    """
    if not t:
        return
    output(t.l)
    print(t.value, end=' ')
    output(t.r)


def multiswap(t, l, r):
    """
    Function to perform a multi-swap operation on a treap.

    Parameters
    ----------
    t : Node
        the root of the treap
    l : int
        the left boundary of the range to be swapped
    r : int
        the right boundary of the range to be swapped
    """
    n = cnt(t)
    t1, t2 = split(t, l)
    i = min(r - l, n - r)
    t2, t3 = split(t2, i)
    t3, t4 = split(t3, r - l - i)
    t4, t5 = split(t4, i)
    t = merge(t1, t4)
    t = merge(t, t3)
    t = merge(t, t2)
    t = merge(t, t5)
    output(t)


def main():
    """
    The main function to execute the program.

    This function creates a treap with 'n' nodes, performs a series of multi-swap operations on the treap,
    and prints the treap after each operation.
    """
    n = 6  # The number of nodes in the treap

    # A list of tuples, where each tuple represents a range of indices to be multi-swapped in the treap
    swap_ranges = [(0, 5), (1, 4), (4, 5), (3, 5), (4, 5), (1, 3)]

    t = None  # The root of the treap

    # Create a treap of the identity permutation
    for i in range(n):
        q = Node(i + 1)  # Create a new node with value 'i+1'
        t = merge(t, q) if t else q  # Merge the new node into the treap
        print(cnt(t))  # Print the count of nodes in the treap

    print("Initial treap:")
    output(t)  # Print the initial treap
    print()

    # Perform the multi-swap operations
    for l, r in swap_ranges:
        print(f"Multiswapping elements from index {l} to index {r}")
        multiswap(t, l, r)  # Perform a multi-swap operation on the range [l, r]
        print()  # Print the treap after the operation


if __name__ == "__main__":
    main()
