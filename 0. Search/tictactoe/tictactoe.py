"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None

def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    if board == initial_state():
        return X

    # Change Player
    PlayerX = 0
    PlayerO = 0
    for row in board:
        PlayerX += row.count(X)
        PlayerO += row.count(O)
        
    if PlayerX > PlayerO:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    Output = set()

    # adds all the possible positions
    for row in range(3):
        for col in range(3):
            if board[row][col] == EMPTY:
                Output.add((row, col))
    
    return Output


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """  
    # Raise exception if not valid
    if action[0] not in range (3) or action[1] not in range(3) or board[action[0]][action[1]] is not EMPTY:
        raise Exception("This is an invalid move")
   
    # Check the players move
    result = copy.deepcopy(board)
    result[action[0]][action[1]] = player(board)
    return result
    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for mark in [X, O]:
        
        # check for Row
        for row in range(3):
            if all(board[row][col] == mark for col in range(3)):
                return mark

        # check for Col
        for col in range(3):
            if all(board[row][col] == mark for row in range(3)):
                return mark

        # check for Diag
        diagonals = [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]
        for diagonal in diagonals:
            if all(board[row][col] == mark for (row, col) in diagonal):
                return mark

    # If no one has won
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there is a winner
    if winner(board) is not None:
        return True

    # If there is a tie
    all_coord = []
    for row in range(3):
        for col in range(3):
            all_coord.append((row, col))

    if not any(board[row][col] == None for (row, col) in all_coord):
        return True

    # Game is still on!
    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    if winner(board) == O:
        return -1
    
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    # If the game is done.
    if terminal(board):
        return None

    optimal_move = None
    max_val = -math.inf
    min_val = math.inf

    # If the current player is X
    if player(board) == X:
        for action in actions(board):
            val = minmax_val(result(board, action), X)
            if val > max_val:
                max_val = val
                optimal_move = action

    # If the current player is O
    elif player(board) == O:
        for action in actions(board):
            val = minmax_val(result(board, action), O)
            if val < min_val:
                min_val = val
                optimal_move = action

    return optimal_move


def minmax_val(board, player):
    """
    Returns the minmax_val for each possible move
    """
    # If the board is terminal return the points. 
    if terminal(board):
        return utility(board)

    # Recurse by predicting O's optimal move
    if player == X:
        val = math.inf
        for action in actions(board):
            val = min(val, minmax_val(result(board, action), O))

        return val

    # Recurse by predicting X's optimal move.
    if player == O:
        val = -math.inf
        for action in actions(board):
            val = max(val, minmax_val(result(board, action), X))
        
        return val
