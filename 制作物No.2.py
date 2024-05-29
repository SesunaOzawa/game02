import tkinter as tk
from tkinter import messagebox

class ReversiGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Reversi")
        
        self.board_size = 8
        self.cell_size = 50
        self.board = [[0] * self.board_size for _ in range(self.board_size)]
        
        self.canvas = tk.Canvas(self.root, width=self.board_size*self.cell_size, height=self.board_size*self.cell_size)
        self.canvas.pack()
        
        self.canvas.bind("<Button-1>", self.on_click)
        
        self.current_player = 1
        self.initialize_board()
        self.draw_board()

    def initialize_board(self):
        mid = self.board_size // 2
        self.board[mid-1][mid-1] = 1
        self.board[mid][mid] = 1
        self.board[mid-1][mid] = -1
        self.board[mid][mid-1] = -1
    
    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.board_size):
            for col in range(self.board_size):
                x1, y1 = col * self.cell_size, row * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                
                if self.board[row][col] == 1:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="black")
                elif self.board[row][col] == -1:
                    self.canvas.create_oval(x1+5, y1+5, x2-5, y2-5, fill="white")
    
    def on_click(self, event):
        col = event.x // self.cell_size
        row = event.y // self.cell_size
        
        if self.is_valid_move(row, col, self.current_player):
            self.make_move(row, col, self.current_player)
            self.current_player = -self.current_player
            self.draw_board()
            
            if not self.has_valid_move(self.current_player):
                self.current_player = -self.current_player
                if not self.has_valid_move(self.current_player):
                    self.end_game()
    
    def is_valid_move(self, row, col, player):
        if self.board[row][col] != 0:
            return False
        for drow, dcol in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            if self.check_direction(row, col, drow, dcol, player):
                return True
        return False
    
    def check_direction(self, row, col, drow, dcol, player):
        i, j = row + drow, col + dcol
        if not (0 <= i < self.board_size and 0 <= j < self.board_size):
            return False
        if self.board[i][j] != -player:
            return False
        i += drow
        j += dcol
        while 0 <= i < self.board_size and 0 <= j < self.board_size:
            if self.board[i][j] == 0:
                return False
            if self.board[i][j] == player:
                return True
            i += drow
            j += dcol
        return False
    
    def make_move(self, row, col, player):
        self.board[row][col] = player
        for drow, dcol in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            if self.check_direction(row, col, drow, dcol, player):
                self.flip_pieces(row, col, drow, dcol, player)
    
    def flip_pieces(self, row, col, drow, dcol, player):
        i, j = row + drow, col + dcol
        while self.board[i][j] == -player:
            self.board[i][j] = player
            i += drow
            j += dcol
    
    def has_valid_move(self, player):
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.is_valid_move(row, col, player):
                    return True
        return False
    
    def end_game(self):
        black_count = sum(row.count(1) for row in self.board)
        white_count = sum(row.count(-1) for row in self.board)
        if black_count > white_count:
            winner = "Black wins!"
        elif white_count > black_count:
            winner = "White wins!"
        else:
            winner = "It's a tie!"
        messagebox.showinfo("Game Over", winner)
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    game = ReversiGame(root)
    root.mainloop()
