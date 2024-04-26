import random

from Players.AlphaBeta import best_alpha_beta
from Players.Minimax import best_minimax


class NimGame:
    def __init__(self, num_heaps, heap_sizes, player_1, player_2):
        self.num_heaps = num_heaps
        self.heaps = heap_sizes
        self.current_player = 0  # 0: player_1, 1: player_2
        self.playersType = [player_1, player_2]  # human(H), minimax(M), alpha-beta(AB), random(R)
        self.evaluation = None  # 1 = player_1 winning, -1 = player_2 winning

    def display_board(self):
        print("Current board:")
        for i, heap in enumerate(self.heaps):
            print(f"Heap {i + 1}: {'*' * heap}")

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
            heap_choice = int(input(f"Enter heap number (1 - {self.num_heaps}): ")) - 1
            if heap_choice < 0 or heap_choice >= self.num_heaps:
                print("Invalid heap number. Please try again.")
                continue
            num_sticks = int(input(f"Enter number of sticks to remove from heap {heap_choice + 1}: "))
            if num_sticks <= 0 or num_sticks > self.heaps[heap_choice]:
                print("Invalid number of sticks. Please try again.")
                continue
            self.make_move([heap_choice, num_sticks])
            break

    def minimax_move(self):
        if self.current_player == 0:
            move = best_minimax(self, 5, True, True)
            self.make_move(move)
            print("Remove ", move[0], " sticks from heap ", move[1] + 1)
        else:
            move = best_minimax(self, 5, False, True)
            self.make_move(move)
            print("Remove ", move[0], " sticks from heap ", move[1] + 1)

    def alpha_beta_move(self):
        if self.current_player == 0:
            move = best_alpha_beta(self, 5, True, True)
            self.make_move(move)
            print("Remove ", move[0], " sticks from heap ", move[1] + 1)
        else:
            move = best_alpha_beta(self, 5, False, True)
            self.make_move(move)
            print("Remove ", move[0], " sticks from heap ", move[1] + 1)

    def random_move(self):
        while True:
            heap_choice = random.choice(range(self.num_heaps))
            if self.heaps[heap_choice] == 0:
                continue
            num_sticks = random.choice(range(self.heaps[heap_choice])) + 1
            self.make_move([heap_choice, num_sticks])
            print("Remove ", num_sticks, " sticks from heap ", heap_choice + 1)
            break

    def make_move(self, move):
        self.heaps[move[0]] -= move[1]

    def undo_move(self, move):
        self.heaps[move[0]] += move[1]
        self.evaluation = None
        self.switch_player()

    def available_moves(self):
        moves = []
        for heap, sticks in enumerate(self.heaps):
            for i in range(sticks):
                moves.append([heap, i + 1])
        return moves

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def check_move(self):
        self.switch_player()
        if all(heap == 0 for heap in self.heaps):
            self.evaluation = 2 - self.current_player * 2 - 1
            return True
        else:
            return False

    def play(self):
        self.switch_player()

        while not self.check_move():
            self.display_board()
            print(f"Player {self.current_player + 1}'s turn:")
            self.player_move()

        self.switch_player()
        print(f"Player {self.current_player + 1} wins!")


if __name__ == "__main__":
    num_heaps = int(input("Enter the number of heaps: "))
    heap_sizes = []
    for i in range(num_heaps):
        size = int(input(f"Enter the size of heap {i + 1}: "))
        heap_sizes.append(size)

    game = NimGame(num_heaps, heap_sizes, "M", "AB")
    game.play()
