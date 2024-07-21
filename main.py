import tkinter as tk
import random

class GameOfLife:
    def __init__(self, master):
        self.master = master
        master.title("Conway's Game of Life")

        self.canvas = tk.Canvas(master, width=600, height=600, bg="white")
        self.canvas.pack()

        self.grid_size = 50
        self.cell_size = 12
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]

        self.draw_grid()

        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.master.bind("<space>", self.start_game)
        self.master.bind("<Escape>", self.stop_game)

    def draw_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0 = i * self.cell_size
                y0 = j * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                color = "black" if self.grid[i][j] else "white"
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="gray")

    def toggle_cell(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size
        self.grid[x][y] = 1 - self.grid[x][y]
        self.draw_grid()

    def start_game(self, event):
        pass

    def stop_game(self, event):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    game = GameOfLife(root)
    root.mainloop()
