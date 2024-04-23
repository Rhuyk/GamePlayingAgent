from tkinter import *
import numpy as np


class TTTGame:
    rows = None
    cols = None
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

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

        for r in range(rows):
            row_buttons = []
            for c in range(cols):
                button = Button(self.frame, text="", font=('consolas', 40), width=5, height=2,
                                command=lambda row=r, column=c: self.next_turn(row, column))
                button.grid(row=r, column=c)
                row_buttons.append(button)
            self.board.append(row_buttons)

        reset_button = Button(text="restart", font=('consolas', 20), command=self.new_game)
        reset_button.pack(side="top")

        self.window.mainloop()

    def next_turn(self, row, col):
        if self.board[row][col]['text'] == "" and self.check_winner() is False:

            if self.player == self.players[0]:
                self.board[row][col]['text'] = self.player
                if self.check_winner() is False:
                    self.player = self.players[1]
                    self.label.config(text=(self.players[1] + " turn"))
                elif self.check_winner() is True:
                    self.label.config(text=(self.players[0] + " wins"))
                elif self.check_winner() == "Tie":
                    self.label.config(text="Tie!")

            else:
                self.board[row][col]['text'] = self.player
                if self.check_winner() is False:
                    self.player = self.players[0]
                    self.label.config(text=(self.players[0] + " turn"))
                elif self.check_winner() is True:
                    self.label.config(text=(self.players[1] + " wins"))
                elif self.check_winner() == "Tie":
                    self.label.config(text="Tie!")

    def check_winner(self):
        for row in range(self.rows):
            if self.board[row][0]['text'] == self.board[row][1]['text'] == self.board[row][2]['text'] != "":
                self.board[row][0].config(bg="green")
                self.board[row][1].config(bg="green")
                self.board[row][2].config(bg="green")
                return True

        for column in range(self.cols):
            if self.board[0][column]['text'] == self.board[1][column]['text'] == self.board[2][column]['text'] != "":
                self.board[0][column].config(bg="green")
                self.board[1][column].config(bg="green")
                self.board[2][column].config(bg="green")
                return True

        if self.board[0][0]['text'] == self.board[1][1]['text'] == self.board[2][2]['text'] != "":
            self.board[0][0].config(bg="green")
            self.board[1][1].config(bg="green")
            self.board[2][2].config(bg="green")
            return True

        elif self.board[0][2]['text'] == self.board[1][1]['text'] == self.board[2][0]['text'] != "":
            self.board[0][2].config(bg="green")
            self.board[1][1].config(bg="green")
            self.board[2][0].config(bg="green")
            return True

        elif self.empty_spaces() is False:
            for row in range(self.rows):
                for column in range(self.cols):
                    self.board[row][column].config(bg="yellow")
            return "Tie"

        else:
            return False

    def empty_spaces(self):
        spaces = self.rows * self.cols
        for row in range(self.rows):
            for column in range(self.cols):
                if self.board[row][column]['text'] != "":
                    spaces -= 1
        return spaces != 0

    def new_game(self):
        self.player = self.players[0]
        self.label.config(text=self.player + " turn")

        for row in range(self.rows):
            for column in range(self.cols):
                self.board[row][column].config(text="", bg="#F0F0F0")


ttt = TTTGame(3, 3)
# ttt.print_board()
# ttt.run_game()
