import numpy as np


class TTTGame:
    board = None
    currentPlayer = "x"
    winner = None
    gameRunning = True

    def __init__(self, rows, cols):
        self.board = np.empty((rows, cols), dtype=str)
        self.board[:] = "-"

    def printBoard(self):
        print(" " + self.board[0, 0] + " | " + self.board[0, 1] + " | " + self.board[0, 2])
        print("-----------")
        print(" " + self.board[1, 0] + " | " + self.board[1, 1] + " | " + self.board[1, 2])
        print("-----------")
        print(" " + self.board[2, 0] + " | " + self.board[2, 1] + " | " + self.board[2, 2])


ttt = TTTGame(3, 3)
ttt.printBoard()
