def perrin(n):
    if n == 0:
        return 3
    if n == 1:
        return 0
    if n == 2:
        return 2
    else:
        v = [2, 0, 3]  # [P(2), P(1), P(0)]
        r = [[0, 1, 1], [1, 0, 0], [0, 1, 0]]
        pr = potenciaMatrizDV(r, n - 2)
        return matrizMult3x3(pr, v)


def potenciaMatrizDV(r, n):
    if n == 1:
        return r
    pr = potenciaMatrizDV(r, n // 2)
    if n % 2 == 0:
        return matrizMult3x3(pr, pr)
    else:
        return matrizMult3x3(r, matrizMult3x3(pr, pr))


def matrizMult3x3(r, s):
    t = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        for j in range(3):
            for k in range(3):
                t[i][j] += r[i][k] * s[k][j]
    return t

