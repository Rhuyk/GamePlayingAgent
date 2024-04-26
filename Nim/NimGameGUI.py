import tkinter as tk
from tkinter import messagebox


class NimGameGUI:
    def __init__(self, master):
        self.master = master
        self.num_heaps = None
        self.heap_sizes = []
        self.current_player = 1

        self.master.title("Nim Game")

        self.create_inputs()

    def create_inputs(self):
        input_frame = tk.Frame(self.master)
        input_frame.pack(pady=10)

        num_heaps_label = tk.Label(input_frame, text="Enter the number of heaps:")
        num_heaps_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.num_heaps_entry = tk.Entry(input_frame)
        self.num_heaps_entry.grid(row=0, column=1, padx=5, pady=5)

        heap_sizes_label = tk.Label(input_frame, text="Enter the size of each heap:")
        heap_sizes_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")

        self.heap_sizes_entries = []
        for i in range(4):  # Assuming maximum of 4 heaps for simplicity
            entry = tk.Entry(input_frame)
            entry.grid(row=1, column=i + 1, padx=5, pady=5)
            self.heap_sizes_entries.append(entry)

        start_button = tk.Button(input_frame, text="Start Game", command=self.start_game)
        start_button.grid(row=2, columnspan=5, pady=10)

    def start_game(self):
        try:
            self.num_heaps = int(self.num_heaps_entry.get())
            self.heap_sizes = [int(entry.get()) for entry in self.heap_sizes_entries[:self.num_heaps]]

            if self.num_heaps <= 0 or any(size <= 0 for size in self.heap_sizes):
                raise ValueError("Invalid input.")

            self.create_board()
            self.create_buttons()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid heap sizes.")

    def create_board(self):
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()

        self.heap_labels = []
        for i, heap in enumerate(self.heap_sizes):
            label = tk.Label(self.board_frame, text=f"Heap {i + 1}: {'*' * heap}")
            label.grid(row=i, column=0, padx=5, pady=5, sticky="w")
            self.heap_labels.append(label)

    def create_buttons(self):
        self.button_frame = tk.Frame(self.master)
        self.button_frame.pack()

        for i in range(self.num_heaps):
            heap_frame = tk.Frame(self.button_frame)
            heap_frame.grid(row=0, column=i, padx=5, pady=5)

            label = tk.Label(heap_frame, text=f"Heap {i + 1}:")
            label.pack()

            remove_button = tk.Button(heap_frame, text="Remove", command=lambda index=i: self.player_move(index))
            remove_button.pack()

    def player_move(self, heap_index):
        try:
            num_sticks = int(self.heap_sizes_entries[heap_index].get())
            if num_sticks <= 0 or num_sticks > self.heap_sizes[heap_index]:
                raise ValueError("Invalid number of sticks.")
            self.heap_sizes[heap_index] -= num_sticks
            self.update_board()
            if self.check_winner():
                messagebox.showinfo("Game Over", f"Player {3 - self.current_player} wins!")
                self.master.destroy()
            else:
                self.switch_player()
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid number of sticks.")

    def update_board(self):
        for i, heap in enumerate(self.heap_sizes):
            self.heap_labels[i].config(text=f"Heap {i + 1}: {'*' * heap}")

    def check_winner(self):
        return all(heap == 0 for heap in self.heap_sizes)

    def switch_player(self):
        self.current_player = 3 - self.current_player


if __name__ == "__main__":
    root = tk.Tk()
    game = NimGameGUI(root)
    root.mainloop()
