import math
import random

from Players.AlphaBeta import best_alpha_beta
from Players.Minimax import best_minimax


class GameState:
    def __init__(self, dogs_locations):
        self.dogs_locations = dogs_locations

class TDGame:
    def __init__(self, player_1, player_2):
        self.current_player = 0  # 0: player_1, 1: player_2
        self.playersType = [player_1, player_2]  # human(H), minimax(M), alpha-beta(AB), random(R)
        self.evaluation = 0
        self.game_over = False
        self.previous_boards = []

        self.tiger_location = 12
        self.dogs_locations = {0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 19, 20, 21, 22, 23, 24}

        self.board = []
        for index in range(25):
            adjacent_nums = set()

            '''up and down'''
            if not index - 5 < 0:
                adjacent_nums.add(index - 5)
            if not index + 5 > 24:
                adjacent_nums.add(index + 5)
            '''left and right'''
            if index not in {0, 5, 10, 15, 20}:
                adjacent_nums.add(index - 1)
            if index not in {4, 9, 14, 19, 24}:
                adjacent_nums.add(index + 1)

            if index % 2 == 0:
                '''diagonals'''
                if index not in {0, 2, 4, 10, 20}:
                    adjacent_nums.add(index - 6)
                if index not in {4, 14, 20, 22, 24}:
                    adjacent_nums.add(index + 6)
                if index not in {0, 2, 4, 14, 24}:
                    adjacent_nums.add(index - 4)
                if index not in {0, 10, 20, 22, 24}:
                    adjacent_nums.add(index + 4)

            self.board.append(adjacent_nums)

    def display_board(self):
        print("Current board:")
        print("-------------------------------")
        row = 0
        for i in range(5):
            for j in range(5):
                piece = j + row
                if len(str(piece)) != 2:
                    piece = f" {piece}"
                if j + row == self.tiger_location:
                    piece = " T"
                elif j + row in self.dogs_locations:
                    piece = " D"

                print(f"| {piece}  ", end="")
            print("|")
            print("-------------------------------")
            row += 5

    def player_move(self):
        if self.playersType[self.current_player] == "H":
            self.human_move()
        elif self.playersType[self.current_player] == "M":
            self.minimax_move()
        elif self.playersType[self.current_player] == "AB":
            self.alpha_beta_move()
        else:
            self.random_move()

    def human_move(self):
        while True:
            if self.current_player == 0:
                move_choice = int(input(f"Move tiger to: "))
                if move_choice not in self.board[self.tiger_location] - self.dogs_locations:
                    print("Invalid space number. Please try again.")
                    continue
                self.make_move([self.tiger_location, move_choice])
                break
            else:
                dog_location = int(input(f"Move dog from: "))
                if dog_location not in self.dogs_locations:
                    print("Invalid location number. Please try again.")
                    continue
                move_choice = int(input(f"Move dog to: "))
                if move_choice not in self.board[dog_location] - {self.tiger_location} - self.dogs_locations:
                    print("Invalid space number. Please try again.")
                    continue
                self.make_move([dog_location, move_choice])
                break

    def minimax_move(self):
        if self.current_player == 0:
            self.make_move(best_minimax(self, 4, True, True))
        else:
            self.make_move(best_minimax(self, 4, False, True))

    def alpha_beta_move(self):
        if self.current_player == 0:
            self.make_move(best_alpha_beta(self, 4, True, True))
        else:
            self.make_move(best_alpha_beta(self, 4, False, True))

    def random_move(self):
        move = random.choice(self.available_moves())
        self.make_move(move)

    def make_move(self, move):
        if move[0] == self.tiger_location:
            self.previous_boards.append(GameState(self.dogs_locations))
            print("Append: ", self.dogs_locations)
            print("")
            self.tiger_location = move[1]
            self.check_tiger_move()
        else:
            self.dogs_locations.remove(move[0])
            self.dogs_locations.add(move[1])
        self.evaluate_game()

    def undo_move(self, move):
        if move[1] == self.tiger_location:
            self.tiger_location = move[0]
            print("Before Pop: ", self.dogs_locations)
            self.dogs_locations = self.previous_boards.pop().dogs_locations
            print("Pop: ", self.dogs_locations)
            print("")
        else:
            self.dogs_locations.remove(move[1])
            self.dogs_locations.add(move[0])
        self.evaluate_game()
        self.game_over = False
        self.switch_player()

    def available_moves(self):
        moves = []
        if self.current_player == 0:
            for move in self.board[self.tiger_location] - self.dogs_locations:
                moves.append([self.tiger_location, move])
        else:
            for dog in self.dogs_locations:
                for move in self.board[dog] - {self.tiger_location} - self.dogs_locations:
                    moves.append([dog, move])
        return moves

    def check_tiger_move(self):
        surrounding_dogs = self.board[self.tiger_location] & self.dogs_locations

        '''horizontal'''
        if surrounding_dogs >= {self.tiger_location - 1, self.tiger_location + 1}:
            kill_dogs = True

            left = self.tiger_location - 2
            while kill_dogs and left not in {-1, 4, 9, 14, 19}:
                if left in self.dogs_locations:
                    kill_dogs = False
                else:
                    left -= 1
            right = self.tiger_location + 2
            while kill_dogs and right not in {5, 10, 15, 20, 25}:
                if right in self.dogs_locations:
                    kill_dogs = False
                else:
                    right += 1

            if kill_dogs:
                self.kill_dogs([self.tiger_location - 1, self.tiger_location + 1])

        '''vertical'''
        if surrounding_dogs >= {self.tiger_location - 5, self.tiger_location + 5}:
            kill_dogs = True

            up = self.tiger_location - 10
            while kill_dogs and up > -1:
                if up in self.dogs_locations:
                    kill_dogs = False
                else:
                    up -= 5
            down = self.tiger_location + 10
            while kill_dogs and down < 25:
                if down in self.dogs_locations:
                    kill_dogs = False
                else:
                    down += 5

            if kill_dogs:
                self.kill_dogs([self.tiger_location - 5, self.tiger_location + 5])

        if self.tiger_location % 2 == 0:
            '''upward diagonal'''
            if surrounding_dogs >= {self.tiger_location - 4, self.tiger_location + 4}:
                kill_dogs = True

                up = self.tiger_location - 8
                while kill_dogs and up > 0 and up != 10:
                    if up in self.dogs_locations:
                        kill_dogs = False
                    else:
                        up -= 4
                down = self.tiger_location + 8
                while kill_dogs and down < 24 and down != 14:
                    if down in self.dogs_locations:
                        kill_dogs = False
                    else:
                        down += 4

                if kill_dogs:
                    self.kill_dogs([self.tiger_location - 4, self.tiger_location + 4])

            '''downward diagonal'''
            if surrounding_dogs >= {self.tiger_location - 6, self.tiger_location + 6}:
                kill_dogs = True

                up = self.tiger_location - 12
                while kill_dogs and up >= 0 and up != 4:
                    if up in self.dogs_locations:
                        kill_dogs = False
                    else:
                        up -= 6
                down = self.tiger_location + 12
                while kill_dogs and down <= 24 and down != 20:
                    if down in self.dogs_locations:
                        kill_dogs = False
                    else:
                        down += 6

                if kill_dogs:
                    self.kill_dogs([self.tiger_location - 6, self.tiger_location + 6])

    def kill_dogs(self, dogs):
        self.dogs_locations.remove(dogs[0])
        self.dogs_locations.remove(dogs[1])

    def evaluate_game(self):
        score = 0
        score += (16 - len(self.dogs_locations)) * 10
        score -= len(self.board[self.tiger_location] - self.dogs_locations) * 3
        self.evaluation = score

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def check_move(self):
        self.switch_player()
        if self.board[self.tiger_location] <= self.dogs_locations:
            self.evaluation = -math.inf
            self.game_over = True
        elif not self.dogs_locations:
            self.evaluation = math.inf
            self.game_over = True

    def play(self):
        while not self.game_over:
            self.display_board()
            print(f"Player {self.current_player + 1}'s turn:")
            self.player_move()
            self.check_move()

        self.switch_player()
        self.display_board()
        print(f"Player {self.current_player + 1} wins!")


if __name__ == "__main__":
    game = TDGame("R", "AB")
    game.play()
