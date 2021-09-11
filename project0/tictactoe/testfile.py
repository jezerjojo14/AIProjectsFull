from tictactoe import minimax, initial_state

board=initial_state()

i=0
while i<3:
    j=0
    while j<3:
        board[i][j]=input("Enter input: ")
        if board[i][j]=='':
            board[i][j]=None
        j+=1
    i+=1

globalHighestLevel=True

print(board, minimax(board))
