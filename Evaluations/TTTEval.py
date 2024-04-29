from tkinter import *
from enum import Enum
import random
import tkinter
from tkinter import TclError, messagebox
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


class TTTGame:
    def __init__(self, rows, cols, condition, player_x, player_o):
        self.rows = rows
        self.cols = cols
        self.condition = condition
        self.playersType = [player_x, player_o]
        self.currentPlayer = Piece.X
        self.game_over = False
        self.board = [{'text': ""} for _ in range(rows * cols)]
        self.evaluation = 0

    def play_game(self):
        self.game_over = False
        self.board = [{'text': ""} for _ in range(self.rows * self.cols)]
        while not self.game_over:
            if self.playersType[self.currentPlayer.number()] == "H":
                pass
            elif self.playersType[self.currentPlayer.number()] == "M":
                self.minimax_move()
            elif self.playersType[self.currentPlayer.number()] == "AB":
                self.alpha_beta_move()
            else:
                self.random_move()
            self.check_move()
        self.evaluate_game()  # Evaluate game outcome after game is over
        return self.evaluation

    def minimax_move(self):
        depth = 5
        move = best_minimax(self, depth, self.currentPlayer == Piece.X, True)
        self.make_move(move)

    def alpha_beta_move(self):
        depth = 5
        move = best_alpha_beta(self, depth, self.currentPlayer == Piece.X, True)
        self.make_move(move)

    def random_move(self):
        move = random.choice(self.available_moves())
        self.make_move(move)

    def make_move(self, space):
        self.board[space]['text'] = self.currentPlayer.value
        self.currentPlayer = self.currentPlayer.opposite()

    def available_moves(self):
        moves = [index for index in range(self.rows * self.cols) if self.board[index]['text'] == ""]
        random.shuffle(moves)  # Shuffle the list of available moves
        return moves

    def check_move(self):
        winner = self.check_winner()
        if winner:
            self.game_over = True
        elif not self.available_moves():
            self.game_over = True

    def evaluate_game(self):
        winner = self.check_winner()
        if winner == Piece.X.number():
            self.evaluation = 0  # 'X' wins
        elif winner == Piece.O.number():
            self.evaluation = 1  # 'O' wins
        else:
            if not self.empty_spaces():  # Check for draw
                self.evaluation = -1  # Draw

    def undo_move(self, space):
        self.board[space]['text'] = ""
        self.evaluation = 0
        if not self.game_over:
            self.currentPlayer = self.currentPlayer.opposite()
        self.game_over = False

    def check_winner(self):
        # Check rows
        for row in range(0, self.rows * self.cols, self.cols):
            if self.board[row]['text'] != "":
                current_piece = self.board[row]['text']
                for i in range(1, self.cols):
                    if self.board[row + i]['text'] != current_piece:
                        break
                    if i == self.condition - 1:
                        return Piece(current_piece)

        # Check columns
        for col in range(self.cols):
            if self.board[col]['text'] != "":
                current_piece = self.board[col]['text']
                for i in range(1, self.rows):
                    if self.board[col + i * self.cols]['text'] != current_piece:
                        break
                    if i == self.condition - 1:
                        return Piece(current_piece)

        # Check diagonals
        for row in range(self.rows - self.condition + 1):
            for col in range(self.cols - self.condition + 1):
                if self.board[row * self.cols + col]['text'] != "":
                    current_piece = self.board[row * self.cols + col]['text']
                    # Check downward-right diagonal
                    if all(self.board[(row + i) * self.cols + (col + i)]['text'] == current_piece for i in
                           range(self.condition)):
                        return Piece(current_piece)
                    # Check downward-left diagonal
                    if all(self.board[(row + i) * self.cols + (col + self.condition - 1 - i)]['text'] == current_piece
                           for i in range(self.condition)):
                        return Piece(current_piece)

        # Check for draw
        if not self.empty_spaces():
            return "Tie"

        return None  # No winner yet

    def empty_spaces(self):
        spaces = self.rows * self.cols
        for space in range(spaces):
            if self.board[space]['text'] != "":
                spaces -= 1
        return spaces != 0


def evaluate_players(rows, cols, condition, player1_type, player2_type, num_games):
    player1_wins = 0
    player2_wins = 0
    draws = 0

    for _ in range(num_games):
        game = TTTGame(rows, cols, condition, player1_type, player2_type)
        winner = game.play_game()
        if winner == 0:
            player1_wins += 1
        elif winner == 1:
            player2_wins += 1
        else:
            draws += 1

    return player1_wins, player2_wins, draws


def main():
    rows = 3
    cols = 3
    condition = 3
    num_games = 100

    player1_type = input("Enter Player 1 type (H/M/AB/R): ").upper()
    player2_type = input("Enter Player 2 type (H/M/AB/R): ").upper()

    valid_player_types = ["H", "M", "AB", "R"]
    if player1_type not in valid_player_types or player2_type not in valid_player_types:
        print("Invalid Player Type. Please enter a valid player type (H/M/AB/R).")
        return

    player1_wins, player2_wins, draws = evaluate_players(rows, cols, condition, player1_type, player2_type, num_games)

    print(f"Player 1 ({player1_type}) Wins: {player1_wins}")
    print(f"Player 2 ({player2_type}) Wins: {player2_wins}")
    print(f"Draws: {draws}")


if __name__ == "__main__":
    main()
