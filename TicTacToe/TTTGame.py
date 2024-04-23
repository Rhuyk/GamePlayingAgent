from tkinter import *
import numpy as np


class TTTGame:
    rows = None
    cols = None
    condition = None
    board = []
    players = ["X", "O"]
    player = players[0]
    winner = None
    gameRunning = True

    window = Tk()
    window.title("Tic-Tac-Toe")
    label = Label(window, text=player + " turn", font=('consolas', 40))
    label.pack(side="top")
    frame = Frame(window)
    frame.pack()

    def __init__(self, rows, cols, condition):
        self.rows = rows
        self.cols = cols
        self.condition = condition

        for r in range(rows):
            # row_buttons = []
            for c in range(cols):
                button = Button(self.frame, text="", font=('consolas', 20), width=3, height=1,
                                command=lambda row=r, column=c: self.next_turn(row, column))
                button.grid(row=r, column=c)
                self.board.append(button)

        reset_button = Button(text="restart", font=('consolas', 20), command=self.new_game)
        reset_button.pack(side="top")

        self.window.mainloop()

    def next_turn(self, row, col):
        space = row * self.cols + col
        if self.board[space]['text'] == "" and self.check_winner() is False:

            if self.player == self.players[0]:
                self.board[space]['text'] = self.player
                if self.check_winner() is False:
                    self.player = self.players[1]
                    self.label.config(text=(self.players[1] + " turn"))
                elif self.check_winner() is True:
                    self.label.config(text=(self.players[0] + " wins"))
                elif self.check_winner() == "Tie":
                    self.label.config(text="Tie!")

            else:
                self.board[space]['text'] = self.player
                if self.check_winner() is False:
                    self.player = self.players[0]
                    self.label.config(text=(self.players[0] + " turn"))
                elif self.check_winner() is True:
                    self.label.config(text=(self.players[1] + " wins"))
                elif self.check_winner() == "Tie":
                    self.label.config(text="Tie!")

    def check_winner(self):
        """Start from first column"""
        for row in range(0, self.rows * self.cols, self.cols):
            '''Check row'''
            cond = 0
            for i in range(self.cols):
                space = row + i
                if self.board[space]['text'] == self.player:
                    cond += 1
                    if cond == self.condition:
                        for j in range(self.condition):
                            self.board[space - j].config(bg="green")
                        return True
                else:
                    cond = 0

            '''
            Check downward diagonal
            '''
            cond = 0
            r = None
            for i in range(row, self.rows * self.cols, self.cols + 1):
                space = i
                if self.board[space]['text'] == self.player and (r is None or r == space // self.cols - 1):
                    cond += 1
                    r = space // self.cols
                    if cond == self.condition:
                        for j in range(self.condition):
                            self.board[space - j * (self.cols + 1)].config(bg="green")
                        return True
                else:
                    cond = 0
                    r = None

        """Start from first row"""
        for col in range(self.cols):
            '''
            Check column
            '''
            cond = 0
            for i in range(0, self.rows * self.cols, self.cols):
                space = col + i
                if self.board[space]['text'] == self.player:
                    cond += 1
                    if cond == self.condition:
                        for j in range(self.condition):
                            self.board[space - j * self.cols].config(bg="green")
                        return True
                else:
                    cond = 0

            '''
            Check downward diagonal
            '''
            cond = 0
            r = None
            for i in range(col, self.rows * self.cols, self.cols + 1):
                space = i
                if self.board[space]['text'] == self.player and (r is None or r == space // self.cols - 1):
                    cond += 1
                    r = space // self.cols
                    if cond == self.condition:
                        for j in range(self.condition):
                            self.board[space - j * (self.cols + 1)].config(bg="green")
                        return True
                else:
                    cond = 0
                    r = None

            '''
            Check upward diagonal
            '''
            cond = 0
            r = None
            for i in range(col, -1, self.cols + 1):
                space = i
                if self.board[space]['text'] == self.player and (r is None or r == space // self.cols + 1):
                    cond += 1
                    r = space // self.cols
                    if cond == self.condition:
                        for j in range(self.condition):
                            self.board[space - j * (self.cols + 1)].config(bg="green")
                        return True
                else:
                    cond = 0
                    r = None

        """Start from last row"""
        for col in range((self.rows - 1) * self.cols, self.rows * self.cols, 1):
            '''
            Check upward diagonal
            '''
            cond = 0
            r = None
            for i in range(col, -1, -(self.cols - 1)):
                space = i
                if self.board[space]['text'] == self.player and (r is None or r == space // self.cols + 1):
                    cond += 1
                    r = space // self.cols
                    if cond == self.condition:
                        for j in range(self.condition):
                            self.board[space + j * (self.cols - 1)].config(bg="green")
                        return True
                else:
                    cond = 0
                    r = None

        if self.empty_spaces() is False:
            for space in range(self.rows * self.cols):
                self.board[space].config(bg="yellow")
            return "Tie"

        else:
            return False

    def empty_spaces(self):
        spaces = self.rows * self.cols
        for space in range(spaces):
            if self.board[space]['text'] != "":
                spaces -= 1
        return spaces != 0

    def new_game(self):
        self.player = self.players[0]
        self.label.config(text=self.player + " turn")

        for space in range(self.rows * self.cols):
            self.board[space].config(text="", bg="#F0F0F0")


ttt = TTTGame(3, 3, 3)

