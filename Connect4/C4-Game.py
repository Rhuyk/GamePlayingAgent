import tkinter as tk
from tkinter import messagebox
import random
from tkinter import ttk
from Players.AlphaBeta import best_alpha_beta
from Players.Minimax import best_minimax


class ConnectFour:
    def __init__(self, player_1, player_2, search_depth, complete_tree_search):
        self.current_player = 1  # 1: player_1, 2: player_2
        self.playersType = [player_1, player_2]  # human(H), minimax(M), alpha-beta(AB), random(R)
        self.evaluation = 0
        self.game_over = False
        self.board = [[0] * 7 for _ in range(6)]  # 0 represents empty, 1 for player 1, 2 for player 2
        self.last_move = []
        self.search_depth = search_depth
        self.complete_tree_search = complete_tree_search
        self.root = tk.Tk()
        self.root.title("Connect Four")
        window_width = 400
        window_height = 400
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

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
                    self.canvas.create_oval(50 * col + 5, 50 * row + 5, 50 * (col + 1) - 5, 50 * (row + 1) - 5,
                                            fill="red")
                elif self.board[row][col] == 2:
                    self.canvas.create_oval(50 * col + 5, 50 * row + 5, 50 * (col + 1) - 5, 50 * (row + 1) - 5,
                                            fill="yellow")

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
        if not self.game_over:
            col = event.x // 50
            try:
                for row in range(5, -1, -1):
                    if self.board[row][col] == 0:
                        self.make_move([row, col])
                        self.draw_board()
                        self.check_move()
                        self.next_turn()
                        break
            except IndexError:
                pass

    def minimax_move(self):
        if self.current_player == 1:
            self.make_move(best_minimax(self, self.search_depth, True, not self.complete_tree_search))
        else:
            self.make_move(best_minimax(self, self.search_depth, False, not self.complete_tree_search))

    def alpha_beta_move(self):
        if self.current_player == 1:
            self.make_move(best_alpha_beta(self, self.search_depth, True, not self.complete_tree_search))
        else:
            self.make_move(best_alpha_beta(self, self.search_depth, False, not self.complete_tree_search))

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


class ConnectFourGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect Four")
        self.search_depth = 5 # Default search depth
        self.complete_tree_search = False  # Default to complete tree search
        window_width = 520
        window_height = 520
        screen_width = self.master.winfo_screenwidth()
        screen_height = self.master.winfo_screenheight()
        x_position = (screen_width - window_width) // 2
        y_position = (screen_height - window_height) // 2
        self.master.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

        header_label = tk.Label(self.master, text="Connect Four", font=("Arial", 20, "bold"))
        header_label.pack(pady=20)

        creator_label = tk.Label(self.master, text="Made by Feng-Min Hu and Prom Jack Sirisukha", font=("Arial", 12))
        creator_label.pack()

        self.player_types = ["Human (H)", "Minimax (M)", "Alpha-beta (AB)", "Random (R)"]

        self.create_input_fields()

    def create_input_fields(self):
        player1_frame = tk.Frame(self.master)
        player1_frame.pack(pady=20)
        player1_label = tk.Label(player1_frame, text="Player 1 Type (Red):", font=("Arial", 14))
        player1_label.pack(side=tk.LEFT, padx=10)
        self.player1_var = tk.StringVar()
        player1_dropdown = ttk.Combobox(player1_frame, textvariable=self.player1_var, values=self.player_types)
        player1_dropdown.pack(side=tk.LEFT, padx=10)
        player1_dropdown.set("Human (H)")

        player2_frame = tk.Frame(self.master)
        player2_frame.pack(pady=20)
        player2_label = tk.Label(player2_frame, text="Player 2 Type (Yellow):", font=("Arial", 14))
        player2_label.pack(side=tk.LEFT, padx=10)
        self.player2_var = tk.StringVar()
        player2_dropdown = ttk.Combobox(player2_frame, textvariable=self.player2_var, values=self.player_types)
        player2_dropdown.pack(side=tk.LEFT, padx=10)
        player2_dropdown.set("Human (H)")

        # Search Depth Entry
        depth_frame = tk.Frame(self.master)
        depth_frame.pack(pady=10)
        depth_label = tk.Label(depth_frame, text="Search Depth:")
        depth_label.pack(side=tk.LEFT, padx=10)
        self.depth_entry = tk.Entry(depth_frame)
        self.depth_entry.pack(side=tk.LEFT, padx=10)
        self.depth_entry.insert(0, str(self.search_depth))

        # Complete Tree Search Dropdown
        tree_search_frame = tk.Frame(self.master)
        tree_search_frame.pack(pady=10)
        tree_search_label = tk.Label(tree_search_frame, text="Complete Tree Search:")
        tree_search_label.pack(side=tk.LEFT, padx=10)
        self.tree_search_var = tk.StringVar()
        tree_search_dropdown = ttk.Combobox(tree_search_frame, textvariable=self.tree_search_var, values=["Yes", "No"])
        tree_search_dropdown.pack(side=tk.LEFT, padx=10)
        tree_search_dropdown.set("No" if not self.complete_tree_search else "Yes")

        start_button = tk.Button(self.master, text="Start Game", command=self.start_game)
        start_button.pack(pady=20)

        quit_button = tk.Button(self.master, text="Quit", command=self.master.destroy)
        quit_button.pack(pady=10)

    def start_game(self):
        player1_type = self.player1_var.get()[0]
        player2_type = self.player2_var.get()[0]
        self.master.withdraw()
        try:
            self.search_depth = int(self.depth_entry.get())
        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please enter a valid search depth.")
            return
        self.complete_tree_search = True if self.tree_search_var.get() == "Yes" else False

        self.game = ConnectFour(player1_type, player2_type, self.search_depth, self.complete_tree_search)
        self.game.root.protocol("WM_DELETE_WINDOW", self.show_menu)
        self.game.root.title("Connect Four")
        self.game.root.mainloop()

    def show_menu(self):
        if hasattr(self, 'game') and self.game:
            self.game.root.destroy()
            del self.game

        self.master.deiconify()


def main():
    root = tk.Tk()
    app = ConnectFourGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
