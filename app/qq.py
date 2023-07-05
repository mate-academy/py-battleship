from tabulate import tabulate

def print_board(board):
    print(board)
    print(tabulate(board, tablefmt="grid"))

    board = [['X', 'O', 'X'],
             ['O', 'X', 'O'],
             ['X', 'O', 'X']]
