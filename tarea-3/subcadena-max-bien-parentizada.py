class Node:
    """
    Clase para representar un nodo en el árbol de segmentos.

    Atributos:
    begin (int): Índice de inicio del rango que cubre este nodo.
    end (int): Índice de fin del rango que cubre este nodo.
    PAR (int): Cantidad de paréntesis abiertos que no están bien parentizados en el rango.
    PCR (int): Cantidad de paréntesis cerrados que no están bien parentizados en el rango.
    left (Node): Nodo hijo izquierdo.
    right (Node): Nodo hijo derecho.
    """
    def __init__(self, begin, end, PAR, PCR):
        self.begin = begin
        self.end = end
        self.PCR = PCR
        self.PAR = PAR
        self.left = None
        self.right = None


class SegmentTreeSubStringMaxBP:
    """
    Clase para representar un árbol de segmentos para resolver el problema de la subcadena bien parentizada más larga.

    Atributos:
    root (Node): Nodo raíz del árbol de segmentos.
    """
    def __init__(self, root):
        self.root = root

    def build(self, S, i, j):
        """
        Método para construir el árbol de segmentos a partir de la cadena de caracteres dada.

        Parámetros:
        S (str): Cadena de caracteres compuesta únicamente de paréntesis que abren y que cierran.
        i (int): Índice de inicio del rango.
        j (int): Índice de fin del rango.

        Retorna:
        Node: Nodo raíz del árbol de segmentos construido.
        """
        if i == j:
            if S[i] == '(':
                return Node(i, j, 1, 0)
            else:
                return Node(i, j, 0, 1)
        else:
            mid = (i + j) // 2
            left = self.build(S, i, mid)
            right = self.build(S, mid + 1, j)
            minPAR_PCR = min(left.PAR, right.PCR)
            length = j - i + 1
            PAR = left.PAR + right.PAR - minPAR_PCR
            PCR = left.PCR + right.PCR - minPAR_PCR
            node = Node(i, j, PAR, PCR)
            node.left = left
            node.right = right
            return node

    def query(self, node, i, j):
        """
        Método para realizar consultas en el árbol de segmentos.

        Parámetros:
        node (Node): Nodo actual.
        i (int): Índice de inicio del rango de la consulta.
        j (int): Índice de fin del rango de la consulta.

        Retorna:
        tuple: Tupla con la cantidad de paréntesis abiertos y cerrados que no están bien parentizados en el rango.
        """
        if i == node.begin and j == node.end:
            return node.PAR, node.PCR
        if i >= node.begin and j <= node.end:
            mid = (node.begin + node.end) // 2
            if j <= mid:
                return self.query(node.left, i, j)
            if i > mid:
                return self.query(node.right, i, j)
            left = self.query(node.left, i, mid)
            right = self.query(node.right, mid + 1, j)
            minPAR_PCR = min(left[0], right[1])
            PAR = left[0] + right[0] - minPAR_PCR
            PCR = left[1] + right[1] - minPAR_PCR
            return PAR, PCR
        else:
            return 0

    def maxBP(self, i, j):
        """
        Método para obtener la longitud de la subcadena bien parentizada más larga en el rango [i, j].

        Parámetros:
        i (int): Índice de inicio del rango.
        j (int): Índice de fin del rango.

        Retorna:
        int: Longitud de la subcadena bien parentizada más larga en el rango.
        """
        (PAR, PCR) = self.query(self.root, i, j)
        return j - i + 1 - PAR - PCR

# Ejemplo de uso
S = "())(())(())("
tree = SegmentTreeSubStringMaxBP(None)
tree.root = tree.build(S, 0, len(S) - 1)
result = tree.maxBP(2, 9)
print(result)  # Imprime: 6

