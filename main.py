import tkinter as tk
import random
import pickle
import copy
import tkinter.simpledialog

class GameOfLife:
    def __init__(self, master):
        self.master = master
        master.title("Conway's Game of Life")

        self.canvas = tk.Canvas(master, width=600, height=600, bg="white")
        self.canvas.pack()

        self.default_grid_size = 50
        self.default_cell_size = 12
        self.grid_size = self.default_grid_size
        self.cell_size = self.default_cell_size
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.running = False
        self.interval = 100

        self.control_frame = tk.Frame(master)
        self.control_frame.pack()

        self.reset_button = tk.Button(self.control_frame, text="Reset", command=self.reset_grid)
        self.reset_button.pack(side=tk.LEFT)

        self.randomize_button = tk.Button(self.control_frame, text="Randomize", command=self.randomize_grid)
        self.randomize_button.pack(side=tk.LEFT)

        self.save_button = tk.Button(self.control_frame, text="Save", command=self.save_grid)
        self.save_button.pack(side=tk.LEFT)

        self.load_button = tk.Button(self.control_frame, text="Load", command=self.load_grid)
        self.load_button.pack(side=tk.LEFT)

        self.undo_button = tk.Button(self.control_frame, text="Undo", command=self.undo_grid)
        self.undo_button.pack(side=tk.LEFT)

        self.redo_button = tk.Button(self.control_frame, text="Redo", command=self.redo_grid)
        self.redo_button.pack(side=tk.LEFT)

        self.clear_button = tk.Button(self.control_frame, text="Clear", command=self.clear_grid)
        self.clear_button.pack(side=tk.LEFT)

        self.grid_lines_button = tk.Button(self.control_frame, text="Toggle Grid Lines", command=self.toggle_grid_lines)
        self.grid_lines_button.pack(side=tk.LEFT)

        self.drawing_mode_button = tk.Button(self.control_frame, text="Drawing Mode", command=self.toggle_drawing_mode)
        self.drawing_mode_button.pack(side=tk.LEFT)

        self.custom_grid_button = tk.Button(self.control_frame, text="Set Custom Grid", command=self.set_custom_grid)
        self.custom_grid_button.pack(side=tk.LEFT)

        self.custom_interval_button = tk.Button(self.control_frame, text="Set Interval", command=self.set_custom_interval)
        self.custom_interval_button.pack(side=tk.LEFT)

        self.theme_button = tk.Button(self.control_frame, text="Theme: Light", command=self.switch_theme)
        self.theme_button.pack(side=tk.LEFT)

        self.status_label = tk.Label(master, text="Status: Idle")
        self.status_label.pack()

        self.alive_count_label = tk.Label(master, text="Alive Cells: 0")
        self.alive_count_label.pack()

        self.interval_label = tk.Label(master, text=f"Interval: {self.interval} ms")
        self.interval_label.pack()

        self.canvas.bind("<Button-1>", self.toggle_cell)
        self.canvas.bind("<B1-Motion>", self.draw_cells)
        self.master.bind("<space>", self.toggle_game)
        self.master.bind("<Escape>", self.stop_game)
        self.master.bind("<Up>", self.increase_speed)
        self.master.bind("<Down>", self.decrease_speed)

        self.update_timer = None

        self.history = []
        self.future = []

        self.show_grid_lines = True
        self.drawing_mode = False
        self.theme = "Light"

        self.draw_grid()

    def toggle_grid_lines(self):
        self.show_grid_lines = not            self.show_grid_lines
        self.draw_grid()


    def draw_grid(self):
        self.canvas.delete("all")
        alive_count = 0
        colors = {
            "Light": {"alive": "black", "dead": "white", "outline": "gray"},
            "Dark": {"alive": "white", "dead": "black", "outline": "darkgray"},
            "Blue": {"alive": "blue", "dead": "lightblue", "outline": "gray"},
        }
        color = colors[self.theme]
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x0 = i * self.cell_size
                y0 = j * self.cell_size
                x1 = x0 + self.cell_size
                y1 = y0 + self.cell_size
                cell_color = color["alive"] if self.grid[i][j] else color["dead"]
                if self.grid[i][j]:
                    alive_count += 1
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=cell_color, outline=color["outline"] if self.show_grid_lines else "")
        self.status_label.config(text=f"Status: {'Running' if self.running else 'Paused'}")
        self.alive_count_label.config(text=f"Alive Cells: {alive_count}")
        self.interval_label.config(text=f"Interval: {self.interval} ms")

    def toggle_cell(self, event):
        if not self.drawing_mode:
            x = event.x // self.cell_size
            y = event.y // self.cell_size
            self.save_state(self.grid)
            self.grid[x][y] = 1 - self.grid[x][y]
            self.draw_grid()

    def draw_cells(self, event):
        if self.drawing_mode:
            x = event.x // self.cell_size
            y = event.y // self.cell_size
            if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
                self.save_state(self.grid)
                self.grid[x][y] = 1
                self.draw_grid()

    def toggle_drawing_mode(self):
        self.drawing_mode = not self.drawing_mode
        if self.drawing_mode:
            self.drawing_mode_button.config(text="Drawing Mode: ON")
        else:
            self.drawing_mode_button.config(text="Drawing Mode: OFF")

    def switch_theme(self):
        themes = ["Light", "Dark", "Blue"]
        current_index = themes.index(self.theme)
        self.theme = themes[(current_index + 1) % len(themes)]
        self.theme_button.config(text=f"Theme: {self.theme}")
        self.draw_grid()

    def set_custom_grid(self):
        try:
            new_grid_size = int(tk.simpledialog.askstring("Grid Size", "Enter grid size:"))
            new_cell_size = int(tk.simpledialog.askstring("Cell Size", "Enter cell size:"))
            if new_grid_size > 0 and new_cell_size > 0:
                self.grid_size = new_grid_size
                self.cell_size = new_cell_size
                self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
                self.canvas.config(width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size)
                self.draw_grid()
        except (ValueError, TypeError):
            pass

    def set_custom_interval(self):
        try:
            new_interval = int(tk.simpledialog.askstring("Interval", "Enter interval (ms):"))
            if new_interval > 0:
                self.interval = new_interval
                self.interval_label.config(text=f"Interval: {self.interval} ms")
                if self.running:
                    self.stop_game(None)
                    self.start_game(None)
        except (ValueError, TypeError):
            pass

    def toggle_game(self, event):
        if self.running:
            self.stop_game(None)
        else:
            self.start_game(None)

    def start_game(self, event):
        self.running = True
        self.update_grid()
        self.update_timer = self.master.after(self.interval, self.update_grid)
        self.status_label.config(text="Status: Running")

    def stop_game(self, event):
        self.running = False
        if self.update_timer:
            self.master.after_cancel(self.update_timer)
            self.update_timer = None
        self.status_label.config(text="Status: Paused")

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
        self.interval_label.config(text=f"Interval: {self.interval} ms")

    def decrease_speed(self, event):
        self.interval += 10
        if self.running:
            self.stop_game(None)
            self.start_game(None)
        self.interval_label.config(text=f"Interval: {self.interval} ms")

    def reset_grid(self):
        self.save_state(self.grid)
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.draw_grid()

    def randomize_grid(self):
        self.save_state(self.grid)
        self.grid = [[random.choice([0, 1]) for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.draw_grid()

    def clear_grid(self):
        self.save_state(self.grid)
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.draw_grid()

    def save_grid(self):
        with open("grid_state.pkl", "wb") as f:
            pickle.dump((self.grid_size, self.cell_size, self.grid), f)

    def load_grid(self):
        try:
            with open("grid_state.pkl", "rb") as f:
                self.grid_size, self.cell_size, self.grid = pickle.load(f)
                self.canvas.config(width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size)
                self.draw_grid()
        except FileNotFoundError:
            pass

    def save_state(self, state):
        self.history.append(copy.deepcopy(state))
        self.future.clear()

    def undo_grid(self):
        if self.history:
            self.future.append(self.grid)
            self.grid = self.history.pop()
            self.draw_grid()

    def redo_grid(self):
        if self.future:
            self.save_state(self.grid)
            self.grid = self.future.pop()
            self.draw_grid()
        else:
            self.status_label.config(text="Status: Nothing to redo")

if __name__ == "__main__":
    root = tk.Tk()
    game = GameOfLife(root)
    root.mainloop()
