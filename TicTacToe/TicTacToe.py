from tkinter import *
from enum import Enum
import random

from Players.AlphaBeta import best_alpha_beta
from Players.Minimax import best_minimax


class Piece(Enum):
    X = "X"
    O = "O"

    def opposite(self):
        if self == Piece.X:
            return Piece.O
        else:
            return Piece.X

    def number(self):
        if self == Piece.X:
            return 0
        else:
            return 1


class TTTSetup:
    def __init__(self):
        self.window = Tk()
        self.window.title("Tic-Tac-Toe Setup")

        # Create input widgets
        Label(self.window, text="Rows:").grid(row=0, column=0)
        Label(self.window, text="Columns:").grid(row=1, column=0)
        Label(self.window, text="Connect Condition:").grid(row=2, column=0)
        Label(self.window, text="Player 1 Type (H/M/AB):").grid(row=3, column=0)
        Label(self.window, text="Player 2 Type (H/M/AB):").grid(row=4, column=0)

        self.rows_entry = Entry(self.window)
        self.cols_entry = Entry(self.window)
        self.condition_entry = Entry(self.window)
        self.player1_entry = Entry(self.window)
        self.player2_entry = Entry(self.window)

        self.rows_entry.grid(row=0, column=1)
        self.cols_entry.grid(row=1, column=1)
        self.condition_entry.grid(row=2, column=1)
        self.player1_entry.grid(row=3, column=1)
        self.player2_entry.grid(row=4, column=1)

        Button(self.window, text="Start Game", command=self.start_game).grid(row=5, columnspan=2)
        self.center_window()
        self.window.mainloop()

    def center_window(self):
        window_width = self.window.winfo_reqwidth()
        window_height = self.window.winfo_reqheight()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def start_game(self):
        rows = int(self.rows_entry.get())
        cols = int(self.cols_entry.get())
        condition = int(self.condition_entry.get())
        player1_type = self.player1_entry.get().upper()
        player2_type = self.player2_entry.get().upper()

        ttt_game = TTTGame(rows, cols, condition, player1_type, player2_type)
        self.window.destroy()


class TTTGame:
    evaluation = None  # 1 = X winning, -1 = O winning

    def __init__(self, rows, cols, condition, player_x, player_o):
        self.rows = rows
        self.cols = cols
        self.condition = condition
        self.playersType = [player_x, player_o]
        self.currentPlayer = Piece.X
        self.gameOngoing = True  # Add gameOngoing attribute

        self.window = Tk()
        self.window.title("Tic-Tac-Toe")

        # Calculate button width and height based on board size
        button_width = max(80 // cols, 114)  # Ensure minimum width for smaller boards
        button_height = max(40 // rows, 114)  # Ensure minimum height for smaller boards

        self.label = Label(self.window, text=self.currentPlayer.value + " turn", font=('consolas', 40))
        self.label.pack(side="top")

        self.frame = Frame(self.window)
        self.frame.pack()

        self.board = []
        for r in range(self.rows):
            for c in range(self.cols):
                button = Button(self.frame, text="", font=('consolas', 20), width=3, height=1,
                                command=lambda row=r, column=c: self.human_move(row, column))
                button.grid(row=r, column=c, padx=5, pady=5)
                self.board.append(button)

        Button(self.window, text="Restart", font=('consolas', 20), command=self.new_game).pack(side="top")

        # Calculate window width and height based on board size
        window_width = (button_width + 1) * self.cols * 2  # Add padding and ensure double the button size
        window_height = (button_height + 1) * self.rows * 2  # Add padding and ensure double the button size

        self.center_window(window_width, window_height)

        self.next_turn()
        self.window.mainloop()

    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def next_turn(self):
        if not self.gameOngoing:
            return

        if self.playersType[self.currentPlayer.number()] == "H":
            self.enable_buttons()
        elif self.playersType[self.currentPlayer.number()] == "M":
            self.disable_buttons()
            self.minimax_move()
            self.next_turn()
        elif self.playersType[self.currentPlayer.number()] == "AB":
            self.disable_buttons()
            self.alpha_beta_move()
            self.next_turn()
        else:
            self.disable_buttons()
            self.random_move()
            self.next_turn()

    def enable_buttons(self):
        for button in self.board:
            button.config(state=NORMAL)

    def disable_buttons(self):
        for button in self.board:
            button.config(state="disabled")

    def human_move(self, row, col):
        space = row * self.cols + col
        if self.board[space]['text'] == "" and self.check_winner() is False:
            self.make_move(space)
            self.check_move()
            self.next_turn()

    def minimax_move(self):
        if self.currentPlayer.number() == 0:
            self.make_move(best_minimax(self, 4, True, True))
        else:
            self.make_move(best_minimax(self, 4, False, True))
        self.check_move()
        self.next_turn()

    def alpha_beta_move(self):
        if self.currentPlayer.number() == 0:
            self.make_move(best_alpha_beta(self, 4, True, False))
        else:
            self.make_move(best_alpha_beta(self, 4, False, False))
        self.check_move()
        self.next_turn()

    def random_move(self):
        space = random.choice(self.available_moves())
        self.make_move(space)
        self.check_move()
        self.next_turn()

    def make_move(self, space):
        self.board[space]['text'] = self.currentPlayer.value

    def undo_move(self, space):
        self.board[space]['text'] = ""
        self.evaluation = None
        if self.gameOngoing:
            self.currentPlayer = self.currentPlayer.opposite()
        self.gameOngoing = True

    def available_moves(self):
        spaces = []
        for index in range(self.rows * self.cols):
            if self.board[index]['text'] == "":
                spaces.append(index)
        return spaces

    def check_move(self):
        if self.check_winner() is False:
            self.currentPlayer = self.currentPlayer.opposite()
            self.label.config(text=(self.currentPlayer.value + " turn"))
            self.evaluation = None
            self.gameOngoing = True
        elif self.check_winner() is True:
            self.label.config(text=(self.currentPlayer.value + " wins"))
            self.evaluate_winning_game()
            self.gameOngoing = False
        elif self.check_winner() == "Tie":
            self.label.config(text="Tie!")
            self.evaluation = 0
            self.gameOngoing = False

    def evaluate_winning_game(self):
        if self.currentPlayer.value == "X":
            self.evaluation = 1
        else:
            self.evaluation = -1

    def check_winner(self):
        """Start from first column"""
        for row in range(0, self.rows * self.cols, self.cols):
            '''
            Check row
            '''
            cond = 0
            for i in range(self.cols):
                space = row + i
                if self.board[space]['text'] == self.currentPlayer.value:
                    cond += 1
                    if cond == self.condition:
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
                if self.board[space]['text'] == self.currentPlayer.value and (r is None or r == space // self.cols - 1):
                    cond += 1
                    r = space // self.cols
                    if cond == self.condition:
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
                if self.board[space]['text'] == self.currentPlayer.value:
                    cond += 1
                    if cond == self.condition:
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
                if self.board[space]['text'] == self.currentPlayer.value and (r is None or r == space // self.cols - 1):
                    cond += 1
                    r = space // self.cols
                    if cond == self.condition:
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
                if self.board[space]['text'] == self.currentPlayer.value and (r is None or r == space // self.cols + 1):
                    cond += 1
                    r = space // self.cols
                    if cond == self.condition:
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
                if self.board[space]['text'] == self.currentPlayer.value and (r is None or r == space // self.cols + 1):
                    cond += 1
                    r = space // self.cols
                    if cond == self.condition:
                        return True
                else:
                    cond = 0
                    r = None

        if self.empty_spaces() is False:
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
        self.evaluation = None
        self.gameOngoing = True
        self.currentPlayer = Piece.X
        self.label.config(text=self.currentPlayer.value + " turn")
        for space in range(self.rows * self.cols):
            self.board[space]['text'] = ""
        self.next_turn()


if __name__ == "__main__":
    TTTSetup()
