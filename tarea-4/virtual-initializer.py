def is_initialized(a, b, i, cnt):
    """
    Checks if a given index is initialized in the arrays a and b.

    Parameters:
    a (list): The list of initialized positions.
    b (list): The list of positions to check.
    i (int): The index to check.
    cnt (int): The current count of initialized positions.

    Returns:
    bool: True if the index is initialized, False otherwise.
    """
    return 1 <= b[i] <= cnt and a[b[i]] == i


def main():
    """
    Main function to handle user input and manage the arrays.

    The user can input several commands:
    - "SALIR" to exit the program.
    - "ASIGNAR" followed by two integers to assign a value to a position.
    - "CONSULTAR" followed by an integer to check the value at a position.
    - "LIMPIAR" to reset the count of initialized positions.
    """
    n = int(input("Ingrese el tamaño del arreglo a utilizar: "))
    t = [0] * n
    a = [0] * n
    b = [0] * n
    cnt = 0
    while True:
        instruction = input("Ingrese la instrucción a realizar: ").split()
        if instruction[0] == "SALIR" and len(instruction) == 1:
            break
        elif instruction[0] == "ASIGNAR" and len(instruction) == 3:
            pos, val = map(int, instruction[1:])

            if pos < 0 or pos >= n:
                print(f"La posición a consultar tiene que estar en el rango [0, {n})")
            else:
                t[pos] = val
                if cnt == 0 or not is_initialized(a, b, pos, cnt):
                    cnt += 1
                    b[pos] = cnt
                    a[cnt] = pos
        elif instruction[0] == "CONSULTAR" and len(instruction) == 2:
            pos = int(instruction[1])
            if pos < 0 or pos >= n:
                print(f"La posición a consultar tiene que estar en el rango [0, {n})")
            else:
                if cnt == 0 or not is_initialized(a, b, pos, cnt):
                    print("Posicion sin inicializar")
                else:
                    print(f"El valor en la posición {pos} es {t[pos]}")
        elif instruction == "LIMPIAR" and len(instruction) == 1:
            cnt = 0
        else:
            print("Instrucción no válida")
            print("USO: SALIR | ASIGNAR <posición> <valor> | CONSULTAR <posición> | LIMPIAR")


if __name__ == "__main__":
    """
    Entry point of the program. Calls the main function.
    """
    main()
