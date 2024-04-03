import cmath
from collections import defaultdict
import math

# The implementation of the number of divisors algorithm for every number till n was taken in O(nlog(n))
# from the following source:
# https://programmersarmy.com/number-theory/total_div.html

# The implementation of the Fast Fourier Transform (FFT) and the Convolution algorithm was taken from the
# following source:
# https://cp-algorithms.com/algebra/fft.html


def sieve(n):
    """
    Function to calculate the Smallest Prime Factor (SPF) for every number till n.

    Parameters:
    n (int): The upper limit for the calculation of the SPF.

    Returns:
    list: The SPF array.
    """
    # Initialize an array of size n+1 with all elements as 0. This array will store the smallest prime factor (SPF)
    # for each number.
    spf = [0 for i in range(n + 1)]

    # Set the SPF of 1 as 1, since 1 is neither prime nor composite.
    spf[1] = 1

    # For each number from 2 to n, set its SPF as the number itself.
    # This is because we haven't found any smaller prime factor for these numbers yet.
    for i in range(2, n + 1):
        spf[i] = i

    # For each even number from 4 to n, set its SPF as 2.
    # This is because 2 is the smallest prime factor for all even numbers.
    for i in range(4, n + 1, 2):
        spf[i] = 2

    # For each number i from 3 to sqrt(n), if i is a prime number (i.e., its SPF is i itself),
    # then for each multiple of i from i*i to n, if the SPF of the multiple is the multiple itself,
    # set its SPF as i.
    # This is because i is a smaller prime factor for these multiples than the multiples themselves.
    for i in range(3, math.isqrt(n) + 1):
        if spf[i] == i:
            for j in range(i * i, n + 1, i):
                if spf[j] == j:
                    spf[j] = i

    # Return the SPF array.
    return spf


def get_factorization(x, spf):
    """
    Function to get the prime factorization of a number x using the smallest prime factor array spf.

    Parameters:
    x (int): The number to factorize.
    spf (list): The smallest prime factor array.

    Returns:
    list: The prime factorization of x.
    """
    # Initialize an empty list to store the prime factors of x.
    ret = []

    # While x is not equal to 1, continue the loop.
    while x != 1:
        # Append the smallest prime factor of x to the list.
        ret.append(spf[x])
        # Divide x by its smallest prime factor to get the next number to factorize.
        x = x // spf[x]

    # Return the list of prime factors of the original number.
    return ret


def num_divisors(n, spf):
    """
    Function to calculate the number of divisors of a number n.

    Parameters:
    n (int): The number to calculate the number of divisors.
    spf (list): The smallest prime factor array.

    Returns:
    int: The number of divisors of n.
    """
    # Get the prime factorization of the number n using the smallest prime factor array spf.
    p = get_factorization(n, spf)

    # Initialize a default dictionary to store the frequency of each prime factor.
    mp = defaultdict(int)

    # For each prime factor in the factorization of n, increment its frequency in the dictionary.
    for i in p:
        mp[i] += 1

    # Initialize the number of divisors as 1.
    ans = 1

    # For each prime factor in the dictionary, multiply the number of divisors by the frequency of the prime factor
    # plus 1. This is based on the formula for the number of divisors of a number, which is the product of the powers
    # of its prime factors plus 1.
    for x in mp.values():
        ans *= (x + 1)

    # Return the number of divisors of n.
    return ans

def fft(a, invert=False):
    """
    Function to calculate the Fast Fourier Transform (FFT) of an array a.

    Parameters:
    a (list): The array to calculate the FFT.
    invert (bool): A flag to indicate if the inverse FFT should be calculated.
    """
    n = len(a)
    # If the length of the array is 1, we return as the FFT of a single element is the element itself.
    if n == 1:
        return

    # Split the array into even and odd indexed elements.
    a0 = a[::2]
    a1 = a[1::2]

    # Recursively apply the FFT on the even and odd indexed arrays.
    fft(a0, invert)
    fft(a1, invert)

    # Calculate the angle for the complex roots of unity. The angle is negative if we are calculating the inverse FFT.
    ang = 2 * cmath.pi / n * (-1 if invert else 1)

    # Initialize the complex root of unity.
    w = 1
    # Calculate the complex root of unity.
    wn = cmath.rect(1, ang)

    # Combine the results of the FFTs of the even and odd indexed arrays to get the FFT of the original array.
    for i in range(n // 2):
        # The FFT value for the i-th element is the sum of the FFT values of the even and odd indexed arrays,
        # scaled by the complex root of unity.
        a[i] = a0[i] + w * a1[i]
        # The FFT value for the (i + n//2)-th element is the difference of the FFT values of the even and odd indexed arrays,
        # scaled by the complex root of unity.
        a[i + n // 2] = a0[i] - w * a1[i]
        # If we are calculating the inverse FFT, we scale the FFT values by 1/2.
        if invert:
            a[i] /= 2
            a[i + n // 2] /= 2
        # Multiply the complex root of unity by itself to get the next power of the root of unity.
        w *= wn


def convolution(a, b):
    """
    Function to calculate the convolution of two arrays a and b.

    Parameters:
    a (list): The first array.
    b (list): The second array.

    Returns:
    list: The convolution of a and b.
    """
    # Convert each element in the input lists a and b to complex numbers.
    # This is necessary for the FFT algorithm, which operates on complex numbers.
    fa = [complex(x) for x in a]
    fb = [complex(x) for x in b]

    # Find the smallest power of 2 that is greater than or equal to the sum of the lengths of a and b.
    # This is the size that the input lists need to be padded to for the FFT algorithm.
    n = 1
    while n < len(a) + len(b):
        n <<= 1

    # Pad the input lists with zeros until they reach the required size.
    fa += [0] * (n - len(fa))
    fb += [0] * (n - len(fb))

    # Perform the FFT on the input lists.
    fft(fa, False)
    fft(fb, False)

    # Multiply corresponding elements in the transformed input lists.
    # This is the key step in the convolution operation.
    for i in range(n):
        fa[i] *= fb[i]

    # Perform the inverse FFT on the result.
    # This transforms the result back into the time domain, giving the final result of the convolution.
    fft(fa, True)

    # Round the real part of each element in the result to the nearest integer.
    # This is necessary because the FFT and inverse FFT can introduce small rounding errors.
    result = [round(x.real) for x in fa]

    # Return the result of the convolution.
    return result


def decomp(n):
    """
    Function to calculate the decomp array for every number till n.

    Parameters:
    n (int): The upper limit for the calculation of the decomp array.

    Returns:
    list: The decomp array.
    """
    # First, we calculate the smallest prime factor (SPF) for every number up to n.
    # The sieve function returns a list where the i-th element is the smallest prime factor of i.
    primes = sieve(n)

    # Next, we calculate the number of divisors for every number from 1 to n.
    # We use the previously calculated SPF for this.
    # The result is a list where the i-th element is the number of divisors of i.
    divisors = [num_divisors(i, primes) for i in range(1, n + 1)]

    # We then calculate the convolution of the divisors list with itself. The convolution function returns a new list
    # where the i-th element is the sum of divisors[j] * divisors[i - j] for all j from 1 to i-1. This effectively
    # calculates the sum of the product of the number of divisors for all pairs of numbers that add up to i. This is
    # equivalent to calculating the number of tuples (a, b, c, d ) such that ab + cd = i where ab = j and cd = i-j,
    # because the number of divisors of a number j is equal to the number of tuples (a, b) such that ab = j and this
    # is divisors[j]. Finally, if we sum all the divisors[j] * divisors[i - j] for all j from 1 to i-1, we get the
    # number of tuples (a, b, c, d) such that ab + cd = i.
    result = convolution(divisors, divisors)

    # Finally, we return the first n - 1 elements of the result. This is because the convolution result has length
    # 2n - 1, but we only need the first n - 1 elements that correspond to the numbers from 2 to n.
    return result[0:n - 1]


def main():
    # Read the value of N
    N = int(input("Ingrese el valor de N: "))
    # Check if N is less than 2
    if N < 2:
        # If N is less than 2, there is no tuple (a, b, c, d) that satisfies the condition, so the maximum value of the
        # decomp array is 0.
        print("El valor de la descomposición máxima es: 0")
        return
    else:
        # Calculate the decomp array for every number till N
        max_decomp_list = decomp(N)
        # Print the maximum value of the decomp array
        print("El valor de la descomposición máxima es:")
        print(max(max_decomp_list))


if __name__ == "__main__":
    main()
