import tkinter as tk
from tkinter import messagebox


class TigerVsDogs(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Tiger vs Dogs")
        self.geometry("400x400")

        self.board_size = 5
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.tiger_pos = (2, 2)
        self.dogs_pos = [(0, 1), (0, 3), (1, 0), (1, 4), (3, 0), (3, 4), (4, 1), (4, 3)]
        self.selected = None

        self.create_board()

    def create_board(self):
        self.buttons = [[None for _ in range(self.board_size)] for _ in range(self.board_size)]

        for i in range(self.board_size):
            for j in range(self.board_size):
                color = "white" if (i, j) == self.tiger_pos else "black"
                self.buttons[i][j] = tk.Button(self, bg=color, width=5, height=2,
                                               command=lambda row=i, col=j: self.on_click(row, col))
                self.buttons[i][j].grid(row=i, column=j)

    def on_click(self, row, col):
        if (row, col) == self.tiger_pos:
            self.selected = (row, col)
        elif self.selected and (row, col) not in self.dogs_pos:
            if self.is_valid_move(row, col):
                self.move_tiger(row, col)
                self.check_win()
            else:
                messagebox.showinfo("Invalid Move", "Cannot move to this position!")
                return
        else:
            messagebox.showinfo("Invalid Move", "Select the tiger first!")
            return

    def is_valid_move(self, row, col):
        if abs(row - self.selected[0]) + abs(col - self.selected[1]) == 1:
            return True
        return False

    def move_tiger(self, row, col):
        self.board[self.tiger_pos[0]][self.tiger_pos[1]] = 0
        self.tiger_pos = (row, col)
        self.board[row][col] = 1
        self.update_board()

    def update_board(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                color = "white" if (i, j) == self.tiger_pos else "black"
                self.buttons[i][j].configure(bg=color)

    def check_win(self):
        adjacent_dogs = [(self.tiger_pos[0] - 1, self.tiger_pos[1]), (self.tiger_pos[0] + 1, self.tiger_pos[1]),
                         (self.tiger_pos[0], self.tiger_pos[1] - 1), (self.tiger_pos[0], self.tiger_pos[1] + 1)]
        killed_dogs = []
        for dog in adjacent_dogs:
            if dog in self.dogs_pos:
                direction = (dog[0] - self.tiger_pos[0], dog[1] - self.tiger_pos[1])
                next_dog = (dog[0] + direction[0], dog[1] + direction[1])
                if next_dog in self.dogs_pos:
                    killed_dogs.append(dog)

        for dog in killed_dogs:
            self.dogs_pos.remove(dog)

        if len(self.dogs_pos) <= 6:
            messagebox.showinfo("Game Over", "Tiger player wins!")
            self.reset_board()
        elif not self.can_tiger_move():
            messagebox.showinfo("Game Over", "Dog player wins!")
            self.reset_board()

    def can_tiger_move(self):
        for i in range(self.tiger_pos[0] - 1, self.tiger_pos[0] + 2):
            for j in range(self.tiger_pos[1] - 1, self.tiger_pos[1] + 2):
                if (i, j) not in self.dogs_pos and 0 <= i < self.board_size and 0 <= j < self.board_size:
                    return True
        return False

    def reset_board(self):
        self.board = [[0 for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.tiger_pos = (2, 2)
        self.dogs_pos = [(0, 1), (0, 3), (1, 0), (1, 4), (3, 0), (3, 4), (4, 1), (4, 3)]
        self.selected = None
        self.update_board()


if __name__ == "__main__":
    app = TigerVsDogs()
    app.mainloop()
