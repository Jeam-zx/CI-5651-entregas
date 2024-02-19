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
    # Get the size of the array from the user
    n = int(input("Ingrese el tamaño del arreglo a utilizar: "))

    # Initialize the arrays with zeros
    t = [0] * n
    a = [0] * n
    b = [0] * n

    # Initialize the counter
    cnt = 0

    # Start an infinite loop to handle user commands
    while True:
        # Get the user command and split it into a list of words
        instruction = input("Ingrese la instrucción a realizar: ").split()

        # If the command is "SALIR" and there are no additional words, break the loop
        if instruction[0] == "SALIR" and len(instruction) == 1:
            break

        # If the command is "ASIGNAR" and there are exactly two additional words
        elif instruction[0] == "ASIGNAR" and len(instruction) == 3:
            # Convert the additional words to integers and assign them to pos and val
            pos, val = map(int, instruction[1:])

            # If pos is not a valid index, print an error message
            if pos < 0 or pos >= n:
                print(f"La posición a consultar tiene que estar en el rango [0, {n})")
            else:
                # Assign val to t[pos]
                t[pos] = val

                # If cnt is 0 or the position is not initialized, increment cnt and update a and b
                if cnt == 0 or not is_initialized(a, b, pos, cnt):
                    cnt += 1
                    b[pos] = cnt
                    a[cnt] = pos

        # If the command is "CONSULTAR" and there is exactly one additional word
        elif instruction[0] == "CONSULTAR" and len(instruction) == 2:
            # Convert the additional word to an integer and assign it to pos
            pos = int(instruction[1])

            # If pos is not a valid index, print an error message
            if pos < 0 or pos >= n:
                print(f"La posición a consultar tiene que estar en el rango [0, {n})")
            else:
                # If cnt is 0 or the position is not initialized, print a message
                if cnt == 0 or not is_initialized(a, b, pos, cnt):
                    print("Posicion sin inicializar")
                else:
                    # Print the value at t[pos]
                    print(f"El valor en la posición {pos} es {t[pos]}")

        # If the command is "LIMPIAR" and there are no additional words, reset cnt
        elif instruction[0] == "LIMPIAR" and len(instruction) == 1:
            cnt = 0

        # If the command is not recognized, print an error message
        else:
            print("Instrucción no válida")
            print("USO: SALIR | ASIGNAR <posición> <valor> | CONSULTAR <posición> | LIMPIAR")


if __name__ == "__main__":
    """
    Entry point of the program. Calls the main function.
    """
    main()
