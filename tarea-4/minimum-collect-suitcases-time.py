import sys


def distance2(a, b):
    """
    Calculate the square of the distance between two points.

    Parameters:
    a (tuple): The first point in the form of a tuple (x, y).
    b (tuple): The second point in the form of a tuple (x, y).

    Returns:
    int: The square of the distance between the two points.
    """
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2


def time(a, b):
    """
    Calculate the total time taken to travel from the origin to point b,
    then to point a, and back to the origin.

    Parameters:
    a (tuple): The first point in the form of a tuple (x, y).
    b (tuple): The second point in the form of a tuple (x, y).

    Returns:
    int: The total time taken for the journey.
    """
    return distance2((0, 0), b) + distance2(b, a) + distance2(a, (0, 0))


def collect_dp(s, dp, suitcases, n):
    """
    A dynamic programming function to find the minimum time to collect all suitcases.

    Parameters:
    s (int): The current state represented as a bitmask.
    dp (list): The memoization table.
    suitcases (list): The list of suitcases, each represented as a point (x, y).
    n (int): The total number of suitcases.

    Returns:
    int: The minimum time to collect all suitcases.
    """
    # Check if all suitcases have been collected. If so, return 0 as no more time is needed.
    if s == (1 << n) - 1:
        return 0

    # If the minimum time to collect the remaining suitcases from the current state `s` has been previously calculated,
    # return it directly.
    if dp[s] != sys.maxsize:
        return dp[s]

    # Iterate over all suitcases. If a suitcase `i` has not been collected, try to pair it with another uncollected
    # suitcase `j` to minimize the total time.
    for i in range(n):
        if (s & (1 << i)) == 0:
            best_time = sys.maxsize
            best_pair = -1
            # If a suitcase `j` has not been collected and the time to collect suitcases `i` and `j` is less than the
            # current best time, update the best time and the best pair.
            for j in range(i + 1, n):
                if (s & (1 << j)) == 0 and time(suitcases[i], suitcases[j]) < best_time:
                    best_time = time(suitcases[i], suitcases[j])
                    best_pair = j
            # If a pair of suitcases has been found, update the memoization table `dp` with the minimum time to
            # collect all suitcases from the current state `s`.
            if best_pair != -1:
                dp[s] = min(dp[s], collect_dp(s | (1 << i) | (1 << best_pair), dp, suitcases, n) + best_time)

    # Return the minimum time to collect all suitcases from the current state `s`.
    return dp[s]


def collect(suitcases):
    """
    Prepare the memoization table and start the dynamic programming process.

    Parameters:
    suitcases (list): The list of suitcases, each represented as a point (x, y).

    Returns:
    int: The minimum time to collect all suitcases.
    """
    # Calculate the total number of suitcases
    n = len(suitcases)

    # If the number of suitcases is even
    if n % 2 == 0:
        # Prepare the memoization table with a size of 2^n and initialize all elements to sys.maxsize
        dp = [sys.maxsize] * (1 << n)
        # Start the dynamic programming process with the initial state 0
        return collect_dp(0, dp, suitcases, n)
    else:
        # If the number of suitcases is odd, append a dummy suitcase at the origin
        suitcases.append((0, 0))
        # Prepare the memoization table with a size of 2^(n+1) and initialize all elements to sys.maxsize
        dp = [sys.maxsize] * (1 << (n + 1))
        # Start the dynamic programming process with the initial state 0
        return collect_dp(0, dp, suitcases, n + 1)


# Example usage
suitcases = [(1, 2), (-3, 4), (5, 6)]

result = collect(suitcases)

print(result)  # Output: 148

# Example usage
suitcases = [(1, 2), (-3, 4), (5, 6), (7, 8)]

result = collect(suitcases)

print(result)  # Output: 232
