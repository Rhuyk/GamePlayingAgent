import tkinter as tk
from tkinter import messagebox, OptionMenu
import random
from Players.AlphaBeta import best_alpha_beta
from Players.Minimax import best_minimax


class NimGameGUI:
    def __init__(self, master):
        self.turn_label = None
        self.quit_button = None
        self.master = master
        self.num_heaps = 0
        self.heap_sizes = []
        self.current_player = 1
        self.player_types = [None, None]  # To store player types for Player 1 and Player 2
        self.game_over = False
        self.master.title("Nim Game")
        self.evaluation = 0
        self.search_depth = 5  # Default search depth
        self.complete_tree_search = False  # Default to complete tree search
        self.center_window()
        self.create_inputs()

    def create_inputs(self):
        input_frame = tk.Frame(self.master)
        input_frame.pack(pady=10)

        num_heaps_label = tk.Label(input_frame, text="Enter the number of heaps:")
        num_heaps_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.num_heaps_entry = tk.Entry(input_frame)
        self.num_heaps_entry.grid(row=0, column=1, padx=5, pady=5)

        heap_sizes_label = tk.Label(input_frame, text="Enter the size of each heap (comma-separated):")
        heap_sizes_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.heap_sizes_entry = tk.Entry(input_frame)
        self.heap_sizes_entry.grid(row=1, column=1, padx=5, pady=5)

        # Create player type selection dropdown menus
        player1_label = tk.Label(input_frame, text="Player 1 Type:")
        player1_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.player1_var = tk.StringVar()
        player1_options = ["Human (H)", "Minimax (M)", "Alpha-Beta (AB)", "Random (R)"]
        self.player1_var.set(player1_options[0])  # Default to Human
        player1_dropdown = OptionMenu(input_frame, self.player1_var, *player1_options)
        player1_dropdown.grid(row=2, column=1, padx=5, pady=5)

        player2_label = tk.Label(input_frame, text="Player 2 Type:")
        player2_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.player2_var = tk.StringVar()
        self.player2_var.set(player1_options[0])  # Default to Human
        player2_dropdown = OptionMenu(input_frame, self.player2_var, *player1_options)
        player2_dropdown.grid(row=3, column=1, padx=5, pady=5)

        # Search depth input
        depth_label = tk.Label(input_frame, text="Search Depth:")
        depth_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.depth_entry = tk.Entry(input_frame)
        self.depth_entry.grid(row=4, column=1, padx=5, pady=5)
        self.depth_entry.insert(0, str(self.search_depth))  # Default depth

        # Complete tree search input
        tree_search_label = tk.Label(input_frame, text="Complete Tree Search (Yes/No):")
        tree_search_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.tree_search_var = tk.StringVar()
        self.tree_search_var.set("No")  # Default to No
        tree_search_dropdown = OptionMenu(input_frame, self.tree_search_var, "Yes", "No")
        tree_search_dropdown.grid(row=5, column=1, padx=5, pady=5)

        start_button = tk.Button(input_frame, text="Start Game", command=self.start_game)
        start_button.grid(row=6, columnspan=2, pady=10)

    def center_window(self):
        # Get screen width and height
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()

        # Calculate window width and height
        window_width = 600
        window_height = 400

        # Calculate x and y coordinates for the window to be centered
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)

        # Set the window position
        self.master.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def start_game(self):
        try:
            self.num_heaps = int(self.num_heaps_entry.get())
            sizes_input = self.heap_sizes_entry.get()
            self.heap_sizes = [int(size.strip()) for size in sizes_input.split(',')]

            if len(self.heap_sizes) != self.num_heaps or any(size <= 0 for size in self.heap_sizes):
                raise ValueError("Invalid input.")

            # Set player types based on selection
            self.set_player_types()

            self.search_depth = int(self.depth_entry.get())

            self.complete_tree_search = self.tree_search_var.get() == "Yes"

            # Hide input elements and start button
            for widget in self.master.winfo_children():
                widget.pack_forget()

            self.create_board()
            self.create_buttons()
            # Create a label to display current player's turn
            self.turn_label = tk.Label(self.master, text="Player 1's Turn", font=('Helvetica', 12, 'bold'))
            self.turn_label.pack(pady=10)
            self.play_turn()  # Start the game with the first player's turn
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid heap sizes.")

    def set_player_types(self):
        player1_selection = self.player1_var.get()
        player2_selection = self.player2_var.get()

        self.player_types[0] = self.parse_player_type(player1_selection)
        self.player_types[1] = self.parse_player_type(player2_selection)

    def parse_player_type(self, selection):
        if selection.startswith("Human"):
            return "Human"
        elif selection.startswith("Minimax"):
            return "Minimax"
        elif selection.startswith("Alpha-Beta"):
            return "Alpha-Beta"
        elif selection.startswith("Random"):
            return "Random"
        else:
            return None

    def create_board(self):
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()

        self.heap_labels = []
        for i, heap in enumerate(self.heap_sizes):
            label = tk.Label(self.board_frame, text=f"Heap {i + 1}: {'*' * heap}")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            self.heap_labels.append(label)

    def create_buttons(self):
        button_frame = tk.Frame(self.master)
        button_frame.pack()

        for i in range(self.num_heaps):
            heap_frame = tk.Frame(button_frame)
            heap_frame.grid(row=0, column=i, padx=5, pady=5)

            label = tk.Label(heap_frame, text=f"Heap {i + 1}:")
            label.pack()

            remove_entry = tk.Entry(heap_frame, width=5)
            remove_entry.pack()

            remove_button = tk.Button(heap_frame, text="Remove", command=lambda idx=i, entry=remove_entry: self.player_move(idx, entry))
            remove_button.pack()

    def play_turn(self):
        if self.check_winner():
            messagebox.showinfo("Game Over", f"Player {3 - self.current_player} wins!")
            self.master.destroy()
            return

        if self.player_types[self.current_player - 1] == "Human":
            # Human player's turn (wait for human input via GUI)
            return  # Human moves handled by GUI interaction

        else:
            # AI player's turn
            move = None
            if self.player_types[self.current_player - 1] == "Minimax":
                move = self.minimax_move()
            elif self.player_types[self.current_player - 1] == "Alpha-Beta":
                move = self.alpha_beta_move()
            elif self.player_types[self.current_player - 1] == "Random":
                move = self.random_move()

            if move is not None:
                heap_index, num_sticks = move  # Unpack move into heap_index and num_sticks
                self.make_move([heap_index, num_sticks])  # Execute the move

                # Update the game board in the GUI after executing the move
                self.update_board()

                # Check for game end
                if self.check_winner():
                    messagebox.showinfo("Game Over", f"Player {3 - self.current_player} wins!")
                    self.master.destroy()
                    return

                # Switch to the next player
                self.switch_player()
                self.update_turn_label()  # Update turn label after player switch

                # Use after() method to delay execution and allow GUI update
                self.master.after(1000, self.play_turn)  # Delay 1000 milliseconds (1 second) before next turn

    def make_move(self, move):
        self.heap_sizes[move[0]] -= move[1]
        self.update_board()  # Update the GUI to reflect the new heap sizes

    def player_move(self, heap_index, entry):
        try:
            num_sticks = int(entry.get())
            if num_sticks <= 0 or num_sticks > self.heap_sizes[heap_index]:
                raise ValueError("Invalid number of sticks.")

            # Call make_move with heap_index and num_sticks
            self.make_move([heap_index, num_sticks])

            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {3 - self.current_player} wins!")
                self.master.destroy()
            else:
                self.switch_player()
                self.update_turn_label()  # Update turn label after player switch
                self.play_turn()  # Continue the game with the next player's turn
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid number of sticks.")

    def minimax_move(self):
        if self.current_player == 0:
            move = best_minimax(self, self.search_depth, True, not self.complete_tree_search)
            return [move[0], move[1]]
        else:
            move = best_minimax(self, self.search_depth, False, not self.complete_tree_search)
            return [move[0], move[1]]

    def alpha_beta_move(self):
        if self.current_player == 0:
            move = best_alpha_beta(self, self.search_depth, True, not self.complete_tree_search)
            return [move[0], move[1]]
        else:
            move = best_alpha_beta(self, self.search_depth, False, not self.complete_tree_search)
            return [move[0], move[1]]

    def random_move(self):
        while True:
            heap_choice = random.choice(range(self.num_heaps))
            if self.heap_sizes[heap_choice] == 0:
                continue
            num_sticks = random.choice(range(self.heap_sizes[heap_choice])) + 1
            self.make_move([heap_choice, num_sticks])
            print("Remove ", num_sticks, " sticks from heap ", heap_choice + 1)
            break

    def update_board(self):
        # Update heap labels in the GUI to reflect the current heap sizes
        for i, heap in enumerate(self.heap_sizes):
            self.heap_labels[i].config(text=f"Heap {i + 1}: {'*' * heap}")

    def check_winner(self):
        # Check if all heaps are empty (i.e., game is over)
        return all(heap == 0 for heap in self.heap_sizes)

    def switch_player(self):
        # Switch current player between Player 1 (1) and Player 2 (2)
        self.current_player = 3 - self.current_player

    def update_turn_label(self):
        # Update turn label to show the current player's turn
        self.turn_label.config(text=f"Player {self.current_player}'s Turn")

    def undo_move(self, move):
        self.heap_sizes[move[0]] += move[1]
        self.evaluation = 0
        self.game_over = False
        self.switch_player()

    def available_moves(self):
        moves = []
        for heap, sticks in enumerate(self.heap_sizes):
            for i in range(sticks):
                moves.append([heap, i + 1])

        random.shuffle(moves)
        return moves

    def check_move(self):
        self.switch_player()
        if all(heap == 0 for heap in self.heap_sizes):
            self.evaluation = 2 - self.current_player * 2 - 1
            self.game_over = True


if __name__ == "__main__":
    root = tk.Tk()
    game = NimGameGUI(root)
    root.mainloop()