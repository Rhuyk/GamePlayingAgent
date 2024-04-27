import tkinter as tk

class ConnectFour:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Connect Four")
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        self.board = [[0] * 7 for _ in range(6)]  # 0 represents empty, 1 for player 1, 2 for player 2
        self.current_player = 1
        self.draw_board()
        self.root.bind("<Button-1>", self.drop_piece)
        self.winner = None

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(6):
            for col in range(7):
                self.canvas.create_rectangle(50 * col, 50 * row, 50 * (col + 1), 50 * (row + 1), fill="blue")
                if self.board[row][col] == 1:
                    self.canvas.create_oval(50 * col + 5, 50 * row + 5, 50 * (col + 1) - 5, 50 * (row + 1) - 5, fill="red")
                elif self.board[row][col] == 2:
                    self.canvas.create_oval(50 * col + 5, 50 * row + 5, 50 * (col + 1) - 5, 50 * (row + 1) - 5, fill="yellow")

    def drop_piece(self, event):
        if self.winner is not None:
            return
        col = event.x // 50
        for row in range(5, -1, -1):
            if self.board[row][col] == 0:
                self.board[row][col] = self.current_player
                self.draw_board()
                if self.check_winner(row, col):
                    self.winner = self.current_player
                    self.canvas.create_text(200, 200, text=f"Player {self.winner} wins!", font=("Helvetica", 24))
                    break
                self.current_player = 1 if self.current_player == 2 else 2
                break

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

if __name__ == "__main__":
    game = ConnectFour()
    game.root.mainloop()
