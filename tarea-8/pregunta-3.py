# For this problem, we will use the Convex Hull Trick to find the minimum distance between the points.
# For execute the program, you must indicate the number of points and the x and y coordinates of each point.
# An example of execution is the following:
# 4
# 1 1
# 2 2
# 3 3
# 4 4
# Where the first line indicates the number of points, and the following lines indicate the x and y coordinates of
# each point.

class ConvexHullTrick:
    def __init__(self):
        self.last = None # Last line index queried
        self.M = [] # Slopes
        self.B = [] # Intercepts
        self.considered_points = [] # Considered points in the trick

    def is_line_redundant(self, l1, l2, l3):
        """
        Function to check if a line is redundant given the slopes and intercepts of three lines.

        Parameters:
        l1, l2, l3 (int): Indexes of the lines to check.

        Returns:
        bool: True if the line is redundant, False otherwise.
        """
        return (self.B[l3] - self.B[l1]) * (self.M[l1] - self.M[l2]) < (self.B[l2] - self.B[l1]) * (
                    self.M[l1] - self.M[l3])

    def add(self, m, b):
        """
        Function to add a line to the trick.

        Parameters:
        m (int): Slope of the line.
        b (int): Intercept of the line.
        """
        self.M.append(m)
        self.B.append(b)
        # Remove lines that are now redundant
        while len(self.M) >= 3 and self.is_line_redundant(len(self.M) - 3, len(self.M) - 2, len(self.M) - 1):
            self.M.pop(len(self.M) - 2)
            self.B.pop(len(self.B) - 2)
            self.considered_points.pop(len(self.considered_points) - 2)

    def query(self, x):
        """
        Function to query the minimum value of the trick at a given x.

        Parameters:
        x (int): The x value to query.

        Returns:
        int: The minimum value of the trick at x.
        """
        if self.last >= len(self.M):
            self.last = len(self.M) - 1
        while self.last < len(self.M) - 1 and self.M[self.last + 1] * x + self.B[self.last + 1] < self.M[
            self.last] * x + self.B[self.last]:
            self.last += 1
        self.considered_points.append((x, self.M[self.last]))
        return self.M[self.last] * x + self.B[self.last]


def main():
    # Read the number of points
    trick = ConvexHullTrick()
    n = int(input())
    points = []
    # Read the points
    for i in range(n):
        x, y = map(int, input().split())
        points.append((x, y))
    # Sort the points in ascending order based on their x coordinates
    points.sort()

    # Find the minimal points in the set of points deleting the points that are dominated by others
    minimal_points = []
    for x, y in points:
        # When we find a point that dominates the last point in the minimal points list, we remove the last point
        while minimal_points and minimal_points[-1][1] <= y:
            minimal_points.pop()
        minimal_points.append((x, y))

    # Initialize the trick with the first point
    # At the beginning, the minimum distance is 0
    trick.add(minimal_points[0][1], 0)
    # Initialize the last line queried to 0
    trick.last = 0

    # Query the minimum distance for each minimal point
    for x, y in minimal_points:
        # Query the minimum distance for the current minimal point
        cost = trick.query(x)
        if minimal_points.index((x, y)) < len(minimal_points) - 1:
            trick.add(minimal_points[minimal_points.index((x, y)) + 1][1], cost)

    # At this point, we only have used the convex hull trick to find the
    # minimum distance without considering the partitions, as we know this takes O(nlogn) time
    print(f"The minimum distance is: {cost}")

    # Now, we will find the partitions, given the representative points of each partition
    representative_points = []

    # Remove unnecessary points in the trick, this will take O(n) time
    x, m = trick.considered_points[0]
    for x1, m1 in trick.considered_points[1:]:
        # If the slope changes, we add the point to the representative points
        if m1 != m:
            representative_points.append((x, m))
        x, m = x1, m1

    # Add the last point
    representative_points.append((x, m))

    # Sort the representative points, this will take O(nlogn) time
    representative_points.sort()

    # Find the partitions
    partitions = [[] for _ in range(len(representative_points))]

    # Now each point will be assigned to the partition that contains the representative point that dominates it
    # Consider that the representative points are sorted same as the points list, so we can iterate in lineal time.
    # This will take O(n) time, because the points are sorted
    i, j = 0, 0
    while i < n and j < len(representative_points):
        if points[i][0] <= representative_points[j][0] and points[i][1] <= representative_points[j][1]:
            partitions[j].append(points[i])
            i += 1
        else:
            j += 1
            print(f"j: {j}")

    # Finally, the whole process will take O(nlogn) time.
    for i, partition in enumerate(partitions):
        print(f"Partition {i}: ", end="")
        for height, width in partition:
            print(f"({height}, {width}) ", end="")
        print()


if __name__ == "__main__":
    main()
