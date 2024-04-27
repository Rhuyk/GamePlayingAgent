import tkinter as tk
import random

from Players.AlphaBeta import best_alpha_beta
from Players.Minimax import best_minimax


class ConnectFour:
    def __init__(self, player_1, player_2):
        self.current_player = 1  # 1: player_1, 2: player_2
        self.playersType = [player_1, player_2]  # human(H), minimax(M), alpha-beta(AB), random(R)
        self.evaluation = 0
        self.game_over = False
        self.board = [[0] * 7 for _ in range(6)]  # 0 represents empty, 1 for player 1, 2 for player 2
        self.last_move = []

        self.root = tk.Tk()
        self.root.title("Connect Four")
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.draw_board()
        self.root.bind("<Button-1>", self.human_move)

        self.next_turn()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(6):
            for col in range(7):
                self.canvas.create_rectangle(50 * col, 50 * row, 50 * (col + 1), 50 * (row + 1), fill="blue")
                if self.board[row][col] == 1:
                    self.canvas.create_oval(50 * col + 5, 50 * row + 5, 50 * (col + 1) - 5, 50 * (row + 1) - 5, fill="red")
                elif self.board[row][col] == 2:
                    self.canvas.create_oval(50 * col + 5, 50 * row + 5, 50 * (col + 1) - 5, 50 * (row + 1) - 5, fill="yellow")

    def next_turn(self):
        if self.game_over:
            self.switch_player()
            self.canvas.create_text(200, 200, text=f"Player {self.current_player} wins!", font=("Helvetica", 24))
            return

        if self.playersType[self.current_player - 1] == "H":
            self.root.bind("<Button-1>", self.human_move)
        elif self.playersType[self.current_player - 1] == "M":
            self.root.unbind("<Button-1>")
            self.minimax_move()
            self.draw_board()
            self.check_move()
            self.next_turn()
        elif self.playersType[self.current_player - 1] == "AB":
            self.root.unbind("<Button-1>")
            self.alpha_beta_move()
            self.draw_board()
            self.check_move()
            self.next_turn()
        else:
            self.root.unbind("<Button-1>")
            self.random_move()
            self.draw_board()
            self.check_move()
            self.next_turn()

    def human_move(self, event):
        col = event.x // 50
        for row in range(5, -1, -1):
            if self.board[row][col] == 0:
                self.make_move([row, col])
                self.draw_board()
                self.check_move()
                self.next_turn()
                break

    def minimax_move(self):
        if self.current_player == 1:
            self.make_move(best_minimax(self, 5, True, True))
        else:
            self.make_move(best_minimax(self, 5, False, True))

    def alpha_beta_move(self):
        if self.current_player == 1:
            self.make_move(best_alpha_beta(self, 7, True, True))
        else:
            self.make_move(best_alpha_beta(self, 7, False, True))

    def random_move(self):
        move = random.choice(self.available_moves())
        self.make_move(move)

    def make_move(self, move):
        self.board[move[0]][move[1]] = self.current_player
        self.last_move = [move[0], move[1]]
        self.evaluate_game()

    def undo_move(self, move):
        self.board[move[0]][move[1]] = 0
        self.evaluate_game()
        self.game_over = False
        self.switch_player()

    def available_moves(self):
        moves = []
        for col in range(7):
            for row in range(5, -1, -1):
                if self.board[row][col] == 0:
                    moves.append([row, col])
                    break
        random.shuffle(moves)
        return moves

    def check_move(self):
        if self.check_winner(self.last_move[0], self.last_move[1]) is True:
            self.game_over = True
            if self.current_player == 1:
                self.evaluation = 10000
            else:
                self.evaluation = -10000
        self.switch_player()

    def check_winner(self, row, col):
        directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
        for dr, dc in directions:
            count = 1
            for i in range(1, 4):
                r, c = row + i * dr, col + i * dc
                if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            for i in range(1, 4):
                r, c = row - i * dr, col - i * dc
                if 0 <= r < 6 and 0 <= c < 7 and self.board[r][c] == self.current_player:
                    count += 1
                else:
                    break
            if count >= 4:
                return True
        return False

    def switch_player(self):
        self.current_player = 3 - self.current_player

    def evaluate_game(self):
        player_1_score = self.get_score(1)
        player_2_score = self.get_score(2)
        self.evaluation = player_1_score - player_2_score

    def get_score(self, player):
        score = 0
        for row in range(6):
            for col in range(7):
                if self.board[row][col] == player:
                    # Check horizontally
                    if col <= 3:
                        if self.board[row][col + 1] == player and self.board[row][col + 2] == player and \
                                self.board[row][col + 3] == player:
                            score += 1
                    # Check vertically
                    if row <= 2:
                        if self.board[row + 1][col] == player and self.board[row + 2][col] == player and \
                                self.board[row + 3][col] == player:
                            score += 1
                    # Check diagonally (top-left to bottom-right)
                    if row <= 2 and col <= 3:
                        if self.board[row + 1][col + 1] == player and self.board[row + 2][col + 2] == player and \
                                self.board[row + 3][col + 3] == player:
                            score += 1
                    # Check diagonally (top-right to bottom-left)
                    if row <= 2 and col >= 3:
                        if self.board[row + 1][col - 1] == player and self.board[row + 2][col - 2] == player and \
                                self.board[row + 3][col - 3] == player:
                            score += 1
        return score


if __name__ == "__main__":
    game = ConnectFour("H", "AB")
    game.root.mainloop()
