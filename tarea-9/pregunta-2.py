import random
from math import log, ceil


def freivald(a, b, c):
    """
    Function to check if the product of two matrices equals a third one using Freivalds algorithm.

    Parameters:
    a (list): The first matrix.
    b (list): The second matrix.
    c (list): The third matrix.

    Returns:
    bool: False if the product of the matrices is not equal to the third matrix, if it is equal True
          there is a probability of 1/2 that the matrices are not equal.
    """
    n = len(a)
    # Generate a random vector r of size n
    r = [0] * n

    # Fill the vector r with random values
    for i in range(0, n):
        r[i] = random.randint(0, 1)

    # Calculate the product of the matrices and the vector r
    bxr = [0] * n

    for i in range(0, n):
        for j in range(0, n):
            bxr[i] = bxr[i] + b[i][j] * r[j]

    # Calculate the product of the matrices and the vector c*r
    cxr = [0] * n
    for i in range(0, n):
        for j in range(0, n):
            cxr[i] = cxr[i] + c[i][j] * r[j]

    # Calculate the product of the matrices and the vector a*(b*r)
    axbxr = [0] * n
    for i in range(0, n):
        for j in range(0, n):
            axbxr[i] = axbxr[i] + a[i][j] * bxr[j]

    # Finally check if value of expression
    # (a*(b*r) - c*r) is zero or not
    for i in range(0, n):
        if axbxr[i] - cxr[i] != 0:
            return False

    return True


def is_inverse(a, b, e):
    """
    Function to check if B is the inverse of A with error e.

    Parameters:
    a (list): The matrix A.
    b (list): The matrix B.
    e (float): The error.

    Returns:
    bool: True if B is the inverse of A with error e, False otherwise.
    """
    # Calculate the number of iterations required, this is the smallest k such that 2^k >= 1/e
    k = ceil(log(1 / e, 2))
    # Check if the matrices have the same dimensions, this could be done in O(n) time
    n = len(a)
    if len(b) != n:
        return False
    for j in range(n):
        if len(a[j]) != n or len(b[j]) != n:
            return False
    # initialize I as the identity matrix, this could be done in O(n) time
    i = [[0] * n for i in range(n)]
    for j in range(n):
        i[j][j] = 1
    # The statement B = A^-1 holds true if and only if the product of A and B equals the identity matrix (I). We can
    # verify this condition using Freivalds algorithm, which checks if the product of two matrices equals a third
    # one. The time complexity of Freivalds algorithm is O(n^2) for each iteration, and we perform k iterations for
    # have a probability of error less than e. Therefore, the overall time complexity of this function is O(k*n^2)
    # that is O(log(1/e)*n^2).
    for j in range(0, k):
        if not freivald(a, b, i):
            return False
    return True


def main():
    # Read the value of n
    n = int(input("Ingrese el valor de n: "))
    # Read the matrices A and B
    print("Ingrese la matriz A")
    a = [list(map(int, input().split())) for i in range(n)]
    print("Ingrese la matriz B")
    b = [list(map(int, input().split())) for i in range(n)]
    # Read the value of e
    e = float(input("Ingrese el valor del error e:"))
    # Check if B is the inverse of A with error e
    if is_inverse(a, b, e):
        print("B es la inversa de A, el error del resultado es menor a", e)
    else:
        print("B no es la inversa de A, el error del resultado es menor a", e)


if __name__ == "__main__":
    main()
