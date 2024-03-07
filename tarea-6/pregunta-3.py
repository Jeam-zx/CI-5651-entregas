class Node:
    """
    A class representing a node in a Segment Tree.

    Attributes:
    left (Node): The left child of the node.
    right (Node): The right child of the node.
    val (int): The value of the node.
    """

    def __init__(self, left=None, right=None, val=0):
        self.left = left
        self.right = right
        self.val = val


def build(l, r):
    """
    A function to build a Segment Tree.
    Each node in the tree represents a range of elements.

    Args:
    l (int): The left boundary of the range.
    r (int): The right boundary of the range.

    Returns:
    Node: The root node of the binary tree.
    """
    if l == r:
        return Node(val=0)
    mid = (l + r) // 2
    return Node(build(l, mid), build(mid + 1, r), 0)


def update(node, l, r, idx):
    """
    A function to update a node in the Persistent Segment Tree.

    Args:
    node (Node): The node to be updated.
    l (int): The left boundary of the range.
    r (int): The right boundary of the range.
    idx (int): The index of the node to be updated.

    Returns:
    Node: The updated node.
    """
    if l == r:
        return Node(val=node.val + 1)
    mid = (l + r) // 2
    if idx <= mid:
        return Node(update(node.left, l, mid, idx), node.right, node.val + 1)
    else:
        return Node(node.left, update(node.right, mid + 1, r, idx), node.val + 1)


def query(node_l, node_r, l, r, k):
    """
    A function to query a range in the Persistent Segment Tree.

    Args:
    node_l (Node): The left node of the range.
    node_r (Node): The right node of the range.
    l (int): The left boundary of the range.
    r (int): The right boundary of the range.
    k (int): The value to be queried.

    Returns:
    int: The result of the query.
    """
    if l == r:
        return l
    mid = (l + r) // 2
    if node_r.left.val - node_l.left.val >= k:
        return query(node_l.left, node_r.left, l, mid, k)
    else:
        return query(node_l.right, node_r.right, mid + 1, r, k - (node_r.left.val - node_l.left.val))


def seleccion(i, j, k):
    """
    A function to select a range in the Persistent Segment Tree.

    Args:
    i (int): The left boundary of the range.
    j (int): The right boundary of the range.
    k (int): The value to be selected.

    Returns:
    int: The result of the selection.
    """
    return sorted_nums[query(roots[i - 1], roots[j], 0, len(sorted_nums) - 1, k)]

def binary_search(arr, x):
    """
    A function to perform binary search on an array.

    Args:
    arr (list): The array to be searched.
    x (int): The value to be searched.

    Returns:
    int: The index of the value in the array.
    """
    l, r = 0, len(arr)
    while l < r:
        m = (l + r) // 2
        if arr[m] < x:
            l = m + 1
        else:
            r = m
    return l


def binary_tree_sort(arr):
    """
    A function to sort an array using a binary tree.

    Args:
    arr (list): The array to be sorted.

    Returns:
    list: The sorted array.
    """
    root = Node()
    for a in arr:
        node = root
        while node is not None:
            if a < node.val:
                if node.left is not None:
                    node = node.left
                else:
                    node.left = Node(val=a)
                    break
            else:
                if node.right is not None:
                    node = node.right
                else:
                    node.right = Node(val=a)
                    break
    result = []
    def inorder(node):
        if node is not None:
            inorder(node.left)
            result.append(node.val)
            inorder(node.right)
    inorder(root)
    return result[1:]

nums = [2, 6, 3, 1, 8, 4, 7, 9, 5]
N = len(nums)
sorted_nums = binary_tree_sort(nums)
roots = [None] * (N + 1)
roots[0] = build(0, len(sorted_nums) - 1)


for i in range(N):
    pos = binary_search(sorted_nums, nums[i])
    print(f"Searched {nums[i]} and found it at position {pos}")
    roots[i + 1] = update(roots[i], 0, len(sorted_nums) - 1, pos)

print(seleccion(2, 5, 3))  # Output: 6
print(seleccion(3, 7, 1))  # Output: 1
print(seleccion(1, 9, 5))  # Output: 5
print(seleccion(4, 6, 2))  # Output: 4
