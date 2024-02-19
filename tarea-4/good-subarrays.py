def good_subarrays(a):
    """
    Calculate the number of good subarrays in the given array.

    B is a subarray of A if elements can be removed from array A, while respecting the order in which they appear,
    to obtain B.

    A subarray is considered good if the subarray is not empty and for all i, such that 1 ≤ i ≤ k,
    it holds that B[i] is divisible by i.

    Parameters:
    a (list): The input array.

    Returns:
    int: The number of good subarrays in the input array.
    """
    n = len(a)

    # dp[i] will contain the number of good subarrays of size i with 1 <= i <= n
    dp = [0] * (n + 1)

    # Iterate over each element in the array. The i-th element can belong to a good subarray of size at most i + 1.
    for i in range(n):
        # For each divisor of a[i] less than or equal to i + 1 (starting from the largest divisor)
        for d in range(i + 1, 0, -1):
            # If a[i] is divisible by d, we can construct subarrays of size d by taking this element as the last
            # element of each of the subarrays of size d - 1. In this case, we increase the number of good subarrays
            # of size d.
            if a[i] % d == 0:
                dp[d] += dp[d - 1]
            # As a base case, the element can always be part of a subarray of size 1 (by itself) since 1 divides all
            # numbers. So, if d is 1, we increase the number of good subarrays of size 1.
            if d == 1:
                dp[d] += 1

    # we return the total number of good subarrays
    return sum(dp)


# Test the function with a sample array
s = [2, 2, 1, 22, 15]
print(good_subarrays(s))
