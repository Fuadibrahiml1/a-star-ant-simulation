import tkinter as tk
import random

GRID_SIZE = 22
MAX_ANTS = 1

class AntPathApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Ant Path Visualization")
        self.cells = {}
        self.ants = []
        self.ant_count = tk.IntVar(value=0)
        self.mode = None  

        self.grid_frame = tk.Frame(master)
        self.grid_frame.pack()
        self.control_frame = tk.Frame(master)
        self.control_frame.pack(pady=20)

        self.make_grid()

        tk.Button(self.control_frame, text="Add Ant", command=self.set_mode_ant).pack(side="left", padx=5)
        tk.Button(self.control_frame, text="Place Random Ants", command=self.place_random_ants).pack(side="left", padx=5)
        tk.Button(self.control_frame, text="Place/Remove Obstacles", command=self.set_mode_obstacle).pack(side="left", padx=5)
        tk.Button(self.control_frame, text="Place/Remove Food", command=self.set_mode_food).pack(side="left", padx=5)
        tk.Button(self.control_frame, text="Clear", command=self.clear_grid).pack(side="left", padx=5)
        tk.Button(self.control_frame, text="A* Algorithm", command=self.run_a_star).pack(side="left", padx=5)
        tk.Label(self.control_frame, text="Ant count:").pack(side="left")
        tk.Label(self.control_frame, textvariable=self.ant_count).pack(side="left", padx=5)

    def make_grid(self):
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                cell = tk.Label(self.grid_frame, width=10, height=3, bg="white", relief="solid", borderwidth=1)
                cell.grid(row=r, column=c, padx=1, pady=1)
                cell.bind("<Button-1>", lambda e, row=r, col=c: self.cell_click(row, col))
                self.cells[(r, c)] = cell

    def cell_click(self, row, col):
        if self.mode == 'ant':
            self.toggle_ant(row, col)
        elif self.mode == 'obstacle':
            self.toggle_obstacle(row, col)
        elif self.mode == 'food':
            self.toggle_food(row, col)

    def set_mode_ant(self):
        self.mode = 'ant'

    def set_mode_obstacle(self):
        self.mode = 'obstacle'

    def set_mode_food(self):
        self.mode = 'food'

    def toggle_ant(self, row, col):
        if (row, col) in self.ants:
            self.ants.remove((row, col))
            self.cells[(row, col)].config(bg="white")
            self.ant_count.set(len(self.ants))
        else:
            if len(self.ants) >= MAX_ANTS:
                return
            self.ants.append((row, col))
            self.cells[(row, col)].config(bg="black")
            self.ant_count.set(len(self.ants))

    def toggle_obstacle(self, row, col):
        cell = self.cells[(row, col)]
        if cell.cget("bg") == "grey":
            cell.config(bg="white")
        else:
            cell.config(bg="grey")

    def toggle_food(self, row, col):
        cell = self.cells[(row, col)]
        if cell.cget("bg") == "green":
            cell.config(bg="white")
        else:
            cell.config(bg="green")

    def clear_grid(self):
        for cell in self.cells.values():
            cell.config(bg="white")
        self.ants.clear()
        self.ant_count.set(0)

    def place_random_ants(self):
        self.clear_grid()
        placed = 0
        while placed < MAX_ANTS:
            r = random.randint(0, GRID_SIZE - 1)
            c = random.randint(0, GRID_SIZE - 1)
            if (r, c) not in self.ants and self.cells[(r, c)].cget("bg") == "white":
                self.ants.append((r, c))
                self.cells[(r, c)].config(bg="black")
                placed += 1
        self.ant_count.set(len(self.ants))

    def run_a_star(self):
        if not self.ants:
            return
        start = self.ants[0]
        goal = None
        for pos, cell in self.cells.items():
            if cell.cget("bg") == "green":
                goal = pos
                break
        if not goal:
            return

        path = self.a_star(start, goal)
        if path:
            self.animate_ant(path)

    def animate_ant(self, path, index=0):
        if index >= len(path):
            return

        if index > 0 and self.cells[path[index - 1]].cget("bg") not in ("green",):
          self.cells[path[index - 1]].config(bg="yellow")

        if self.cells[path[index]].cget("bg") != "green":
            self.cells[path[index]].config(bg="black")

        self.master.after(200, lambda: self.animate_ant(path, index + 1))

    def a_star(self, start, goal):
        def heuristic(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        open_set = {start}
        came_from = {}
        g_score = {cell: float('inf') for cell in self.cells}
        g_score[start] = 0
        f_score = {cell: float('inf') for cell in self.cells}
        f_score[start] = heuristic(start, goal)
        while open_set:
            current = min(open_set, key=lambda cell: f_score[cell])
            if current == goal:
                return self.reconstruct_path(came_from, current)
            open_set.remove(current)
            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                    open_set.add(neighbor)
        return []

    def reconstruct_path(self, came_from, current):
        total_path = [current]
        while current in came_from:
            current = came_from[current]
            total_path.append(current)
        return total_path[::-1]

    def get_neighbors(self, cell):
        neighbors = []
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        for dr, dc in directions:
            nr, nc = cell[0] + dr, cell[1] + dc
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                if self.cells[(nr, nc)].cget("bg") != "grey":
                    neighbors.append((nr, nc))
        return neighbors

if __name__ == "__main__":
    root = tk.Tk()
    app = AntPathApp(root)
    root.mainloop()
