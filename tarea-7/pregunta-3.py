def kmpPre(x):
    """
    This function is a part of the Knuth-Morris-Pratt (KMP) algorithm that preprocesses the input string and
    creates an auxiliary array. This array is used to skip unnecessary comparisons when a mismatch occurs.

    Parameters:
    x (str): The input string.

    Returns:
    list: An array where the i-th element is the skip value for the i-th character of the input string.
    """
    b = [-1] * len(x)
    j = -1
    for i in range(1, len(x)):
        while j >= 0 and x[i - 1] != x[j]:
            j = b[j]
        j += 1
        b[i] = j
    return b


def longest_prefix_suffix(x):
    """
    Find the longest proper prefix of the input string which is also a suffix.

    This function uses the kmpPre function to compute the longest proper prefix which is also a suffix for each
    substring of the input string. The last element of the array returned by kmpPre contains the max index of the
    longest proper prefix which is also a suffix for the entire string if b[-1] != 0. If b[-1] == 0,  it checks if
    the first and last characters of the string are the same, else it returns an empty string.

    It then returns the longest such prefix for the entire string.

    Parameters:
    x (str): The input string.

    Returns:
    str: The longest proper prefix of the input string which is also a suffix. If no such prefix exists,
    it returns an empty string.
    """

    # Add a character (We assume that # doesn't appear in x) to the middle of the string. This is done to prevent the
    # kmpPre function from skipping all the characters when the entire string is a repeated letter. We know that the
    # longest proper prefix which is also a suffix cannot be longer than half the length of the string, because a longer
    # prefix would not leave enough characters for a matching suffix.
    x = x[:len(x) // 2] + "#" + x[len(x) // 2:] 
    b = kmpPre(x)
    if b[-1] != 0:
        return x[:b[-1] + 1]
    elif x[0] == x[-1]:
        return x[0]
    else:
        return ""


# Test the function
print(longest_prefix_suffix("ABRACADABRA"))  # Output: "ABRA"
print(longest_prefix_suffix("AREPERA"))  # Output: "A"
print(longest_prefix_suffix("LLLL"))  # Output: "LL"
print(longest_prefix_suffix("ALGORITMO"))  # Output: ""
print(longest_prefix_suffix("ABCDABCD"))  # Output: "ABCD"
