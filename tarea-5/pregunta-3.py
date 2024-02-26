class State:
    """
    A class used to represent the state of the game.

    ...

    Attributes
    ----------
    board : list
        a list of lists representing the game board
    player : int
        an integer representing the current player (1 for the first player, 2 for the second player)
    previous_move : tuple
        a tuple representing the last move made on the board

    Methods
    -------
    next_states():
        Generates all possible next states from the current state.
    """

    def __init__(self, board, player, previous_move):
        """
        Constructs all the necessary attributes for the state object.

        Parameters
        ----------
            board : list
                a list of lists representing the game board
            player : int
                an integer representing the current player (1 for the first player, 2 for the second player)
            previous_move : tuple
                a tuple representing the last move made on the board
        """
        self.board = board
        self.player = player
        self.previous_move = previous_move

    def next_states(self):
        """
        Generates all possible next states from the current state.

        The method iterates over all cells of the board. If a cell is not the same as the previous move and does not
        already contain a '+', a new state is created with the current player's symbol added to the cell. The new state
        is then added to the list of next states. The player is also switched for the next state.

        Returns
        -------
        list
            a list of State objects representing all possible next states from the current state
        """
        # Initialize an empty list to store the next states
        next_states = []

        # Iterate over all cells of the board
        for i in range(3):
            for j in range(3):
                # Check if the cell is not the same as the previous move and does not already contain a '+'
                if (i, j) != self.previous_move and self.board[i][j] != '+':
                    # Create a deep copy of the board
                    new_board = [row[:] for row in self.board]
                    # Determine the symbol of the previous player
                    previous_player_symbol = '-' if self.player == 1 else '|'
                    # If the cell contains the previous player's symbol, can be replaced with '+'
                    if new_board[i][j] == previous_player_symbol:
                        new_board[i][j] = '+'
                    # If the cell is empty, add the current player's symbol
                    elif new_board[i][j] == ' ':
                        new_board[i][j] = ('|' if self.player == 1 else '-')
                    # If the cell contains the current player's symbol, skip this cell
                    else:
                        continue
                    # Create a new state with the updated board and add it to the list of next states
                    next_states.append(State(new_board, 3 - self.player, (i, j)))

        # Return the list of next states
        return next_states

    def __iter__(self):
        """
        Initializes an iterator over the next states
        of the game.

        Returns
        -------
        self : object
            The instance of the State class.
        """
        self._next_states_iter = iter(self.next_states())
        return self

    def __next__(self):
        """
        Returns the next state from the list of
        next states of the game.

        Returns
        -------
        State
            The next state in the list of next states.

        Raises
        ------
        StopIteration
            If there are no more items to return, it raises the StopIteration exception.
        """
        return next(self._next_states_iter)

    def is_end_state(self):
        """
        Checks if the current state is an end state.

        Returns
        -------
        bool
            True if the current state is an end state, False otherwise
        """
        # Iterate over all rows and columns of the board
        for i in range(3):
            # Check if the current row or column contains three '+'
            if self.board[i] == ['+', '+', '+'] or [self.board[j][i] for j in range(3)] == ['+', '+', '+']:
                # If it does, the current state is an end state, so return True
                return True

        # Check if the main diagonal or the secondary diagonal contains three '+'
        if ([self.board[i][i] for i in range(3)] == ['+', '+', '+'] or
                [self.board[i][2 - i] for i in range(3)] == ['+', '+', '+']):
            # If it does, the current state is an end state, so return True
            return True

        # If no row, column, or diagonal contains three '+', the current state is not an end state, so return False
        return False


def eval(state):
    """
    Evaluates the desirability of a game state.

    Parameters
    ----------
    state : State
        The current state of the game.

    Returns
    -------
    int
        The evaluation of the state. If is desirable for the first player, the evaluation is positive. If is desirable
        for the second player, the evaluation is negative. If the state is neutral, the evaluation is 0.
    """
    # Check if the current state is a winning configuration
    if state.is_end_state():
        # If the current state is a winning configuration, return 10 if the current player is the first player and -10
        # if it's the second player
        return 10 if state.player == 1 else -10

    # Check for potential win in the next turns
    # Iterate over all rows and columns of the board
    for i in range(3):
        # Get the current row and column
        row = state.board[i]
        col = [state.board[j][i] for j in range(3)]
        # Check if the current row or column contains two '+' and one '-
        if row.count('+') == 2 and row.count('-') == 1 or col.count('+') == 2 and col.count('-') == 1:
            # If the current player is the player 1, it could win in its next turn
            return 5
        if row.count('+') == 2 and row.count('|') == 1 or col.count('+') == 2 and col.count('|') == 1:
            # If the current player is the player 2, it could win in its next turn
            return -5

        if row.count('+') == 1 and row.count('-') == 1 or col.count('+') == 1 and col.count('-') == 1:
            # If the current player is the player 1, it could make a cross in its next turn
            return 3
        if row.count('+') == 1 and row.count('|') == 1 or col.count('+') == 1 and col.count('|') == 1:
            # If the current player is the player 2, it could make a cross in its next turn
            return -3

        if row.count('+') == 0 and row.count('-') == 1 or col.count('+') == 0 and col.count('-') == 1:
            # If the current player is the player 1, it could make a cross in its next turn
            return 1

        if row.count('+') == 0 and row.count('|') == 1 or col.count('+') == 0 and col.count('|') == 1:
            # If the current player is the player 2, it could make a cross in its next turn
            return -1

    # Check for potential win in the next turns in the diagonals
    # Get the main and secondary diagonals
    main_diag = [state.board[i][i] for i in range(3)]
    sec_diag = [state.board[i][2 - i] for i in range(3)]
    # Check if the main diagonal contains two '+' and one '-'

    if main_diag.count('+') == 2 and main_diag.count('-') == 1 or sec_diag.count('+') == 2 and sec_diag.count('-') == 1:
        # If the current player is the player 1, it could win in its next turn
        return 5
    if main_diag.count('+') == 2 and main_diag.count('|') == 1 or sec_diag.count('+') == 2 and sec_diag.count('|') == 1:
        # If the current player is the player 2, it could win in its next turn
        return -5

    if main_diag.count('+') == 1 and main_diag.count('-') == 1 or sec_diag.count('+') == 1 and sec_diag.count('-') == 1:
        # If the current player is the player 1, it could make a cross in its next turn
        return 3
    if main_diag.count('+') == 1 and main_diag.count('|') == 1 or sec_diag.count('+') == 1 and sec_diag.count('|') == 1:
        # If the current player is the player 2, it could make a cross in its next turn
        return -3

    if main_diag.count('+') == 0 and main_diag.count('-') == 1 or sec_diag.count('+') == 0 and sec_diag.count('-') == 1:
        # If the current player is the player 1, it could make a cross in its next turn
        return 1
    if main_diag.count('+') == 0 and main_diag.count('|') == 1 or sec_diag.count('+') == 0 and sec_diag.count('|') == 1:
        # If the current player is the player 2, it could make a cross in its next turn
        return -1

    # If we can't infer anything from the current state, return 0
    return 0


def first_player(state, n, alpha, beta):
    """
    Implements the Minimax algorithm for the first player with Alpha-Beta pruning.

    Parameters
    ----------
    state : State
        The current state of the game.
    n : int
        The depth of the game tree to explore.
    alpha : float
        The best value that the maximizing player can guarantee at current level or above.
    beta : float
        The best value that the minimizing player can guarantee at current level or above.

    Returns
    -------
    max_eval : float
        The maximum evaluation value of the next states.
    """
    # Check if the depth is 0 or the current state is an end state
    if n == 0 or state.is_end_state():
        # If it is, return the evaluation of the state
        return eval(state)
    else:
        # If it's not, initialize the maximum evaluation value to negative infinity (neutral element for the maximum)
        max_eval = -float('inf')
        # Iterate over all next states of the current state
        for next_state in state.next_states():
            # For each next state, call the `second_player` function and update the maximum evaluation value
            max_eval = max(max_eval, second_player(next_state, n - 1, alpha, beta))
            # Update alpha to be the maximum of alpha and the current maximum evaluation value
            alpha = max(alpha, max_eval)
            # If beta is less than or equal to alpha, break the loop because the minimizing player has a better value
            # at some ancestor node
            if beta <= alpha:
                break
        # Return the maximum evaluation value
        return max_eval


def second_player(state, n, alpha, beta):
    """
    Implements the Minimax algorithm for the second player with Alpha-Beta pruning.

    Parameters
    ----------
    state : State
        The current state of the game.
    n : int
        The depth of the game tree to explore.
    alpha : float
        The best value that the maximizing player can guarantee at current level or above.
    beta : float
        The best value that the minimizing player can guarantee at current level or above.

    Returns
    -------
    min_eval : float
        The minimum evaluation value of the next states.
    """
    # Check if the depth is 0 or the current state is an end state
    if n == 0 or state.is_end_state():
        # If it is, return the evaluation of the state
        # The eval function evaluates the desirability of a game state
        return eval(state)
    else:
        # If it's not, initialize the minimum evaluation value to positive infinity (neutral element for the minimum)
        min_eval = float('inf')
        # Iterate over all next states of the current state
        for next_state in state.next_states():
            # For each next state, call the `first_player` function and update the minimum evaluation value
            min_eval = min(min_eval, first_player(next_state, n - 1, alpha, beta))
            # Update beta to be the minimum of beta and the current minimum evaluation value
            beta = min(beta, min_eval)
            # If beta is less than or equal to alpha, break the loop because the maximizing player has a better value
            # at some ancestor node
            if beta <= alpha:
                break
        # Return the minimum evaluation value
        return min_eval


def main():
    """
    The main function of the program. It initializes the game and determines the winner.

    The function first initializes an empty 3x3 board and a state with the first player to move. It then calls the
    `first_player` function to get the result of the game. If the result is 0, it increases the depth and calls the
    `first_player` function again until the result is not 0. Finally, it prints the winner and the maximum number of
    moves.
    """
    # Initialize an empty 3x3 board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    # Initialize a state with the first player to move
    state = State(board, 1, None)
    # Set the initial depth to 9
    n = 9
    # Call the `first_player` function to get the result of the game
    result = first_player(state, n, -float('inf'), float('inf'))
    # If the result is 0, increase the depth and call the `first_player` function again until the result is not 10
    # or -10.
    while result != 10 and result != -10:
        n += 1
        result = first_player(state, n, -float('inf'), float('inf'))

    # Print the winner and the maximum number of moves
    if result > 0:
        print("Gana el primer jugador en maximo", n, "movimientos.")
    else:
        print("Gana el segundo jugador en maximo", n, "movimientos.")


if __name__ == "__main__":
    """
    Entry point of the program. Calls the main function.
    """
    main()
