"""
Tic Tac Toe Player
"""

import math

X = "X"
O = "O"
EMPTY = None

from copy import deepcopy

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
    x=0
    o=0
    for row in board:
        for col in row:
            if col==X:
                x+=1
            if col==O:
                o+=1
    if x>o:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actionList=[]
    i=0
    while i<3:
        j=0
        while j<3:
            if board[i][j]==EMPTY:
                actionList.append((i, j))
            j+=1
        i+=1
    return actionList


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if board[action[0]][action[1]]==EMPTY:
        newBoard=deepcopy(board)
        newBoard[action[0]][action[1]]=player(board)
        return newBoard
    else:
        raise Exception("Invalid input")

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    for i in range(3):
        if (board[i][0]!=EMPTY and board[i][0]==board[i][1] and board[i][0]==board[i][2]) or (board[0][i]!=EMPTY and board[0][i]==board[1][i] and board[0][i]==board[2][i]):
            if player(board)==X:
#                print("Winner is O")
                return O
            else:
#                print("Winner is X")
                return X
    if board[1][1]!=EMPTY and ((board[0][0]==board[1][1] and board[0][0]==board[2][2]) or (board[0][2]==board[1][1] and board[1][1]==board[2][0])):
        if player(board)==X:
#            print("Winner is O")
            return O
        else:
#            print("Winner is X")
            return X
#    print("No winner")
    return None

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board)==None:
        i=0
        while i<3:
            j=0
            while j<3:
                if board[i][j]==EMPTY:
#                    print("Game not over")
                    return False
                j+=1
            i+=1
#    print("This game is over")
    return True

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board)==X:
        return 1
    elif winner(board)==O:
        return -1
    else:
        return 0

def minimax(board):
    if terminal(board):
        return None
    elif board==initial_state():
        return (0, 0)
    else:
        optimalAction=unique_actions(board)[0]
        optimalMoveQuality=move_quality(board, optimalAction)
        efficiency=float(optimalMoveQuality[1])/optimalMoveQuality[0]
        for action in unique_actions(board):
            moveQuality=move_quality(board, action)
            if player(board)==X:
                if utility(result(board, action))==1:
                    return action
                if float(moveQuality[1])/moveQuality[0]>efficiency:
                    efficiency=float(moveQuality[1])/moveQuality[0]
                    optimalAction=action
            else:
                if utility(result(board, action))==-1:
                    return action
                if float(moveQuality[1])/moveQuality[0]<efficiency:
                    efficiency=float(moveQuality[1])/moveQuality[0]
                    optimalAction=action
        return optimalAction

def move_quality(board, action):
    if terminal(result(board, action)):
        return (1, utility(result(board, action)))
    else:
        nextMoveQuality=move_quality(result(board, action), minimax(result(board, action)))
        return (nextMoveQuality[0]+1, nextMoveQuality[1])

def unique_actions(board):
    uniqueActions=actions(board)
    verticallySymmetric=True
    for j in range(3):
        if board[0][j]!=board[2][j]:
            verticallySymmetric=False
    if verticallySymmetric:
        i=0
        while i<len(uniqueActions):
            if uniqueActions[i][0]==2:
                del uniqueActions[i]
            i+=1
    horizontallySymmetric=True
    for j in range(3):
        if board[j][0]!=board[j][2]:
            horizontallySymmetric=False
    if horizontallySymmetric:
        i=0
        while i<len(uniqueActions):
            if uniqueActions[i][1]==2:
                del uniqueActions[i]
            i+=1
    if board[0][1]==board[1][0] and board[0][2]==board[2][0] and board[1][2]==board[2][1]:
        i=0
        del_list=[]
        while i<len(uniqueActions):
            if uniqueActions[i]==(1, 0) or uniqueActions[i]==(2, 0) or uniqueActions[i]==(2, 1):
                del_list.append(i)
            i+=1
        j=0
        for i in del_list:
            del uniqueActions[i-j]
            j+=1
    if board[0][0]==board[2][2] and board[0][1]==board[1][2] and board[1][0]==board[2][1]:
        i=0
        del_list=[]
        while i<len(uniqueActions):
            if uniqueActions[i]==(2, 1) or uniqueActions[i]==(2, 2) or uniqueActions[i]==(1, 2):
                del_list.append(i)
            i+=1
        j=0
        for i in del_list:
            del uniqueActions[i-j]
            j+=1
    return uniqueActions
