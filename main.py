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
        self.running = False
        self.interval = 100  # milliseconds

        self.draw_grid()

        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.master.bind("<space>", self.toggle_game)
        self.master.bind("<Escape>", self.stop_game)
        self.master.bind("<Up>", self.increase_speed)
        self.master.bind("<Down>", self.decrease_speed)

        self.update_timer = None

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

    def toggle_game(self, event):
        if self.running:
            self.stop_game(None)
        else:
            self.start_game(None)

    def start_game(self, event):
        self.running = True
        self.update_grid()
        self.update_timer = self.master.after(self.interval, self.update_grid)

    def stop_game(self, event):
        self.running = False
        if self.update_timer:
            self.master.after_cancel(self.update_timer)
            self.update_timer = None

    def update_grid(self):
        if not self.running:
            return

        new_grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                neighbors = sum(
                    self.grid[x][y]
                    for x in range(max(0, i-1), min(self.grid_size, i+2))
                    for y in range(max(0, j-1), min(self.grid_size, j+2))
                    if (x, y) != (i, j)
                )
                if self.grid[i][j] == 1 and neighbors in [2, 3]:
                    new_grid[i][j] = 1
                elif self.grid[i][j] == 0 and neighbors == 3:
                    new_grid[i][j] = 1

        self.grid = new_grid
        self.draw_grid()
        self.update_timer = self.master.after(self.interval, self.update_grid)

    def increase_speed(self, event):
        if self.interval > 10:
            self.interval -= 10
            if self.running:
                self.stop_game(None)
                self.start_game(None)

    def decrease_speed(self, event):
        self.interval += 10
        if self.running:
            self.stop_game(None)
            self.start_game(None)

if __name__ == "__main__":
    root = tk.Tk()
    game = GameOfLife(root)
    root.mainloop()