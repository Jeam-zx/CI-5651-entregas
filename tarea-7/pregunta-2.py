from functools import cmp_to_key


# Graham's scan algorithm to find the convex hull of a set of points is based on the following resources:
# https://www.geeksforgeeks.org/convex-hull-using-graham-scan/

def left_index(points):
    """
    Function to find the point with the lowest x-coordinate. If there are multiple points with the same x-coordinate,
    the point with the highest y-coordinate is selected.

    Parameters:
    points (list): A list of tuples, where each tuple represents a point (x, y).

    Returns:
    int: The index of the point with the lowest x-coordinate.
    """
    left_most = 0
    for i in range(1, len(points)):
        if points[i][0] < points[left_most][0]:
            left_most = i
        elif points[i][0] == points[left_most][0]:
            if points[i][1] > points[left_most][1]:
                left_most = i
    return left_most


def orientation(p, q, r):
    """
    Function to find the orientation of an ordered triplet of points (p, q, r).

    Parameters:
    p, q, r (tuple): Each tuple represents a point (x, y).

    Returns:
    int: Returns 0 if p, q, and r are colinear, 1 if they are clockwise, and 2 if they are counterclockwise.
    """
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    elif val > 0:
        return 1
    else:
        return 2


def compare(p1, p2):
    """
    Comparison function used by the sorted function. It compares two points based on their orientation with a global
    point p0.

    Parameters:
    p1, p2 (tuple): Each tuple represents a point (x, y).

    Returns: int: Returns -1 if p1 is closer to p0 or if the orientation of p0, p1, and p2 is counterclockwise.
    Returns 1 otherwise.
    """
    o = orientation(p0, p1, p2)
    if o == 0:
        if dist_square(p0, p2) >= dist_square(p0, p1):
            return -1
        else:
            return 1
    else:
        if o == 2:
            return -1
        else:
            return 1


def dist_square(p1, p2):
    """
    Function to calculate the square of the distance between two points.

    Parameters:
    p1, p2 (tuple): Each tuple represents a point (x, y).

    Returns:
    int: The square of the distance between p1 and p2.
    """
    return ((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2)


def graham_scan(points):
    """
    Function to find the convex hull of a set of points using the Graham's scan algorithm.

    Parameters:
    points (list): A list of tuples, where each tuple represents a point (x, y).

    Returns:
    list: A list of points that form the convex hull of the input points.
    """
    global p0

    n = len(points)

    l = left_index(points)

    p0 = points[l]
    points[0], points[l] = points[l], points[0]

    points = sorted(points, key=cmp_to_key(compare))

    m = 1
    for i in range(1, n):
        while (i < n - 1) and (orientation(p0, points[i], points[i + 1]) == 0):
            i += 1
        points[m] = points[i]
        m += 1

    if m < 3:
        return

    stack = [points[0], points[1], points[2]]

    for i in range(3, m):
        while len(stack) > 1 and orientation(stack[-2], stack[-1], points[i]) != 2:
            stack.pop()
        stack.append(points[i])

    return stack


def iterative_graham_scan(points):
    """
    Function to apply the Graham's scan algorithm iteratively on a set of points until no more convex hulls can be found.

    Parameters:
    points (list): A list of tuples, where each tuple represents a point (x, y).

    Returns:
    int: The number of convex hulls found.
    """
    hulls = []
    while points:
        hull = graham_scan(points)
        if not hull or hull == points:
            break
        hulls.append(hull)
        points = [p for p in points if p not in hull]
    return len(hulls)


# Test the function
p = [(0, 3), (1, 1), (2, 2), (4, 4), (0, 0), (1, 2), (3, 1), (3, 3)]
print(iterative_graham_scan(p))  # Output: 2
