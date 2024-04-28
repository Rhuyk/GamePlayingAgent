import math
import random

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from functools import partial
from Players.AlphaBeta import best_alpha_beta
from Players.Minimax import best_minimax


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
            move = best_minimax(self, 5, True, True)
            self.make_move(move)
        else:
            move = best_minimax(self, 5, False, True)
            self.make_move(move)

    def alpha_beta_move(self):
        if self.current_player == 0:
            self.make_move(best_alpha_beta(self, 6, True, True))
        else:
            self.make_move(best_alpha_beta(self, 6, False, True))

    def random_move(self):
        move = random.choice(self.available_moves())
        self.make_move(move)

    def make_move(self, move):
        if move[0] == self.tiger_location:
            self.previous_boards.append(set(self.dogs_locations))
            self.tiger_location = move[1]
            self.check_tiger_move()
        else:
            self.dogs_locations.remove(move[0])
            self.dogs_locations.add(move[1])
        self.evaluate_game()

    def undo_move(self, move):
        if move[1] == self.tiger_location:
            self.tiger_location = move[0]
            self.dogs_locations = self.previous_boards.pop()
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
        random.shuffle(moves)
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

        score += (16 - len(self.dogs_locations)) * 50
        if self.tiger_location % 2 == 0:
            score += 5
        if self.tiger_location in {0, 1, 2, 3, 4, 5, 9, 10, 14, 15, 19, 20, 21, 22, 23, 24}:
            score -= 5
        if self.tiger_location in {0, 4, 20, 24}:
            score -= 10

        score -= (8 - len(self.board[self.tiger_location] - self.dogs_locations)) * 10
        for dog in self.dogs_locations:
            score -= len(self.board[dog] & self.dogs_locations)
        self.evaluation = score

    def switch_player(self):
        self.current_player = 1 - self.current_player

    def check_move(self):
        self.switch_player()
        if self.board[self.tiger_location] <= self.dogs_locations:
            self.evaluation = -10000
            self.game_over = True
        elif not self.dogs_locations:
            self.evaluation = 10000
            self.game_over = True


class TigersVsDogsGUI:
    def __init__(self, master):
        self.player_types_label = None
        self.master = master
        self.master.title("Tigers vs Dogs Game")
        self.buttons = []

        window_width = 520
        window_height = 520

        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.master.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        header_label = tk.Label(self.master, text="Tigers vs Dogs", font=("Arial", 20, "bold"))
        header_label.pack(pady=20)

        creator_label = tk.Label(self.master, text="Made by Feng-Min Hu and Prom Jack Sirisukha", font=("Arial", 12))
        creator_label.pack()

        self.game = None

        self.player_types = ["Human (H)", "Minimax (M)", "Alpha-beta Pruning (AB)", "Random (R)"]

        self.create_input_fields()

    def disable_board_buttons(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)

    def enable_board_buttons(self):
        for button in self.buttons:
            button.config(state=tk.NORMAL)

    def create_input_fields(self):
        # Player 1 Type input field
        player1_frame = tk.Frame(self.master)
        player1_frame.pack(pady=20)
        player1_label = tk.Label(player1_frame, text="Player 1 (Tiger) Type:", font=("Arial", 14))
        player1_label.pack(side=tk.LEFT, padx=10)
        self.player1_var = tk.StringVar()
        player1_dropdown = ttk.Combobox(player1_frame, textvariable=self.player1_var, values=self.player_types)
        player1_dropdown.pack(side=tk.LEFT, padx=10)
        player1_dropdown.set("Human (H)")

        # Player 2 Type input field
        player2_frame = tk.Frame(self.master)
        player2_frame.pack(pady=20)
        player2_label = tk.Label(player2_frame, text="Player 2 (Dogs) Type:", font=("Arial", 14))
        player2_label.pack(side=tk.LEFT, padx=10)
        self.player2_var = tk.StringVar()
        player2_dropdown = ttk.Combobox(player2_frame, textvariable=self.player2_var, values=self.player_types)
        player2_dropdown.pack(side=tk.LEFT, padx=10)
        player2_dropdown.set("Human (H)")

        # Start Game button
        start_button = tk.Button(self.master, text="Start Game", command=self.start_game)
        start_button.pack(pady=20)

        quit_button = tk.Button(self.master, text="Quit", command=self.master.quit)
        quit_button.pack(pady=10)

    def start_game(self):
        player1_type = self.player1_var.get()
        player2_type = self.player2_var.get()

        if player1_type.startswith("A"):
            player1_type_short = "AB"
        else:
            player1_type_short = player1_type[0]

        if player2_type.startswith("A"):
            player2_type_short = "AB"
        else:
            player2_type_short = player2_type[0]

        self.game = TDGame(player1_type_short, player2_type_short)

        self.create_board_ui()

        if player1_type_short != "H" and player2_type_short != "H":
            self.play_ai_vs_ai()
        elif player1_type_short != "H" and player2_type_short == "H":
            self.play_ai_vs_human()

    def play_ai_vs_ai(self):
        if self.game is None or self.game.game_over:
            self.enable_board_buttons()
            return

        self.disable_board_buttons()

        if not self.game.game_over:
            current_player = self.game.current_player
            self.trigger_ai_move()
            if not self.game.game_over:
                self.update_player_turn_label()
                self.update_board()
                self.game.check_move()
                self.check_game_over()
                self.game.current_player = 1 - current_player

                self.master.after(500, self.play_ai_vs_ai)

    def play_ai_vs_human(self):
        if not self.game.game_over:
            current_player_type = self.game.playersType[self.game.current_player]
            if current_player_type != "H":
                self.trigger_ai_move()
                self.update_player_turn_label()
                self.update_board()
                self.game.check_move()
                self.check_game_over()
                self.game.current_player = 1 - self.game.current_player

    def create_board_ui(self):
        for widget in self.master.winfo_children():
            widget.pack_forget()

        header_label = tk.Label(self.master, text="Tigers vs Dogs", font=("Arial", 20, "bold"))
        header_label.pack(pady=20)

        creator_label = tk.Label(self.master, text="Made by Feng-Min Hu and Prom Jack Sirisukha", font=("Arial", 12))
        creator_label.pack()

        player_types_text = f"Player 1 ({self.player1_var.get()}): vs Player 2 ({self.player2_var.get()})"
        self.player_types_label = tk.Label(self.master, text=player_types_text, font=("Arial", 12))
        self.player_types_label.pack()

        self.info_label = tk.Label(self.master, text="Player 1's turn: Move Tiger", font=("Arial", 14))
        self.info_label.pack(pady=10)

        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()

        self.buttons = []
        self.selected_dog = None  # Track selected dog position

        for i in range(25):
            row, col = divmod(i, 5)
            button = tk.Button(self.board_frame, text="", width=4, height=2, font=("Arial", 12),
                               command=partial(self.on_click, i), relief=tk.RAISED)
            button.grid(row=row, column=col, padx=3, pady=3)
            self.buttons.append(button)

        return_button = tk.Button(self.master, text="Return to Menu", command=self.return_to_menu)
        return_button.pack(pady=20)

        self.update_board()

    def return_to_menu(self):
        self.game = None

        for widget in self.master.winfo_children():
            widget.pack_forget()

        self.enable_board_buttons()
        self.create_input_fields()

    def on_click(self, position):
        if self.selected_dog is None:
            if self.game.current_player == 0:  # Player 1 (Tiger) turn
                if position in self.game.board[self.game.tiger_location] - self.game.dogs_locations:
                    self.game.make_move([self.game.tiger_location, position])
                    self.update_board()
                    self.game.check_move()
                    self.check_game_over()

                    if not self.game.game_over:
                        self.update_player_turn_label()  # Update player turn label
                        if self.game.playersType[1] != "H" or self.game.playersType[0] != "H":
                            self.trigger_ai_move()

                else:
                    messagebox.showerror("Invalid Move", "Cannot move tiger to this position.")
            else:  # Player 2 (Dog) turn
                if position in self.game.dogs_locations:
                    self.select_dog(position)
                else:
                    messagebox.showerror("Invalid Selection", "Please select a dog to move.")
        else:
            if position in self.game.board[self.selected_dog] - {self.game.tiger_location} - self.game.dogs_locations:
                self.game.make_move([self.selected_dog, position])
                self.update_board()
                self.game.check_move()
                self.check_game_over()

                if not self.game.game_over:
                    self.update_player_turn_label()
                    self.clear_button_selection(position)
                    if self.game.playersType[1] != "H" or self.game.playersType[0] != "H":
                        self.trigger_ai_move()
                        self.update_player_turn_label()

            elif position == self.selected_dog:
                self.clear_button_selection(position)
            else:
                messagebox.showerror("Invalid Move", "Cannot move dog to this position.")

    def update_player_turn_label(self):
        current_player = self.game.current_player
        player_label_text = f"Player {current_player + 1}'s turn: "

        if current_player == 0:
            player_label_text += "Move Tiger"
        else:
            player_label_text += "Move Dog"

        self.info_label.config(text=player_label_text)

    def trigger_ai_move(self):
        current_player = self.game.current_player
        player_type = self.game.playersType[current_player]

        if player_type == "M" or player_type == "AB" or player_type == "R":
            if player_type == "M":
                self.game.minimax_move()
            elif player_type == "AB":
                self.game.alpha_beta_move()
            elif player_type == "R":
                self.game.random_move()

        self.update_board()
        self.game.check_move()
        self.check_game_over()

    def select_dog(self, position):
        if self.selected_dog is not None:
            if self.selected_dog != position:
                self.buttons[self.selected_dog].config(bg="brown")
        self.selected_dog = position
        self.buttons[position].config(bg="green")  # Highlight selected dog

    def clear_button_selection(self, position):
        if self.selected_dog is not None:
            self.buttons[position].config(bg="brown")
            self.selected_dog = None

    def update_board(self):
        for i in range(25):
            if i == self.game.tiger_location:
                self.buttons[i].config(text="T", bg="orange", fg="black")
            elif i in self.game.dogs_locations:
                self.buttons[i].config(text="D", bg="brown", fg="white")
            else:
                self.buttons[i].config(text="", bg="lightgray", fg="black")

    def check_game_over(self):
        if self.game.game_over:
            winner = "Player 1: Tiger" if self.game.current_player == 1 else "Player 2: Dogs"
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.master.destroy()


def main():
    root = tk.Tk()
    app = TigersVsDogsGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
