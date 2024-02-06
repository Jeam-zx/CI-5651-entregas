def merge_sort(lst, compare):
    """
    Esta función implementa el algoritmo de ordenamiento por mezcla (merge sort).

    Parámetros:
    lst (lista): La lista de elementos a ordenar.
    compare (función): Una función de comparación que toma dos elementos y devuelve True si
    el primer elemento debe preceder al segundo en el ordenamiento, y False en caso contrario.

    Devuelve:
    lista: La lista de elementos ordenada.
    """
    if len(lst) <= 1:
        return lst
    mid = len(lst) // 2
    left = merge_sort(lst[:mid], compare)
    right = merge_sort(lst[mid:], compare)
    return merge(left, right, compare)

def merge(left, right, compare):
    """
    Esta función combina dos listas ordenadas en una nueva lista ordenada.

    Parámetros:
    left, right (lista): Las dos listas ordenadas a combinar.
    compare (función): Una función de comparación que toma dos elementos y devuelve True si el
    primer elemento debe preceder al segundo en el ordenamiento, y False en caso contrario.

    Devuelve:
    lista: La nueva lista ordenada.
    """
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if compare(left[i], right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    while i < len(left):
        result.append(left[i])
        i += 1
    while j < len(right):
        result.append(right[j])
        j += 1
    return result


def maximal_set_of_requests(n, p, t):
    """
    Esta función calcula el conjunto maximal de peticiones basado en los parámetros dados.

    Parámetros:
    n (int): El número total de peticiones.
    p (lista): Una lista de enteros que representan el el punto de inicio de cada petición.
    t (lista): Una lista de enteros que representan el tamaño de cada petición.

    Devuelve:
    lista: Una lista de enteros que representa el conjunto maximal de peticiones.
    """

    # Inicializa una lista con índices de 0 a n-1
    o = [i for i in range(n)]
    # Inicializa una lista vacía para almacenar el conjunto máximo de peticiones
    perm = []

    def compare_requests(i, j):
        """
        Esta función compara dos peticiones segun su punto final basándose en su punto de inicio y tamaño.

        Parámetros:
        i, j (int): Los índices de las dos peticiones a comparar.

        Devuelve:
        bool: Verdadero si el punto final de la petición i-ésima es menor o igual al punto final
         de la petición j-ésima, Falso en caso contrario.
        """
        return p[i] + t[i] <= p[j] + t[j]

    # Ordena la lista de índices basándose en la función de comparación
    o = merge_sort(o, compare_requests)

    # Itera sobre la lista ordenada de índices
    for i in range(n):
        # Calcula el rango de la petición i-ésima
        rango_o_i = [p[o[i]], p[o[i]] + t[o[i]]]

        # Si la lista de peticiones maximal está vacía o el punto de inicio de la petición actual
        # es mayor o igual al punto de inicio de la última petición en el conjunto maximal,
        # añade la petición actual al conjunto maximal
        if len(perm) == 0 or rango_o_i[0] >= p[perm[-1]]:
            perm.append(o[i])

    # Incrementa los índices en el conjunto maximal en 1 para que coincidan con los
    # números de petición originales
    for i in range(len(perm)):
        perm[i] += 1

    # Devuelve el conjunto maximal de peticiones
    return perm
