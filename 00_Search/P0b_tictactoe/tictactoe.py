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
    num_x = 0
    num_y = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == X:
                num_x += 1
            elif board[i][j] == O:
                num_y += 1
    if num_x + num_y == 9:
        return "FULL"
    elif num_x == num_y:
        return X
    else:
        return O
    raise NotImplementedError


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    answer = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:    
                answer.add((i, j))
    return answer
    raise NotImplementedError


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    (i, j) = action
    pl = player(board)
    res = copy.deepcopy(board)
    res[i][j] = pl
    return res
    raise NotImplementedError


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for n in range(3):
        if board[n][0] == board[n][1] == board[n][2]:
            return board[n][0]
        if board[0][n] == board[1][n] ==  board[2][n]:
            return board[0][n]
    if board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    if board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    return None           
    raise NotImplementedError


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if player(board) == "FULL":
        return True
    elif winner(board) != None:
        return True
    else:
        return False
    raise NotImplementedError


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0
    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
   
    def max_val(board):
        best_action = (0,0)
        if terminal(board):
            return utility(board), best_action
        v = -100
        for action in actions(board):
            new = min_val(result(board, action))[0]
            if new > v:
                v = new
                best_action = action
        return v, best_action

    def min_val(board):
        best_action = (0,0)
        if terminal(board):
            return utility(board), best_action
        v = 100
        for action in actions(board):
            new = max_val(result(board, action))[0]
            if new < v:
                v = new
                best_action = action
        return v, best_action
    
    if terminal(board):
        return None
    pl = player(board)    
    
    if pl == X:
        return max_val(board)[1]
         
    if pl == O:
        return min_val(board)[1]
                
                
    raise NotImplementedError
