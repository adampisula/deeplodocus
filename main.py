import tkinter as tk
import numpy as np
import time
import json

k = 2
win_width = 600 * k
win_height = 150 * k
fps = 30

class Frame:
    dino_altitude = 0 * k
    nearest_obstacle = 0 * k
    obstacle_width = 0 * k
    obstacle_height = 0 * k
    obstacle_altitude = 0 * k

    dino = None
    obstacle = None

    _canvas = None

    def __init__(self, canvas):
        self._canvas = canvas

    def draw(self):
        self.dino = GDino(self._canvas, self.dino_altitude)
        self.obstacle = GObstacle(self._canvas, self.obstacle_width, self.obstacle_height, self.obstacle_altitude)
        self.obstacle.x = self.nearest_obstacle + self.dino.x + self.dino.dino_width

        self.dino.draw()
        self.obstacle.draw()

    def clean(self):
        if self.dino != None:
            self.dino.clean()

        if self.obstacle != None:
            self.obstacle.clean()

    def export(self):
        return json.dumps({ "dino_altitude": self.dino_altitude / k, "nearest_obstacle": self.nearest_obstacle, "obstacle_width": self.obstacle_width, "obstacle_height": self.obstacle_height, "obstacle_altitude": self.obstacle_altitude})

class GDino:
    dino_width = 25 * k
    dino_height = 40 * k
    x = 30 * k
    y = win_height - dino_height

    _background = 'blue'
    _canvas = None
    _id = None

    def __init__(self, canvas, dino_altitude):
        self._canvas = canvas
        self.y -= dino_altitude

    def draw(self):
        self._id = self._canvas.create_rectangle(self.x, self.y, self.x + self.dino_width, self.y + self.dino_height, fill = self._background)

    def clean(self):
        if self._id != None:
            self._canvas.delete(self._id)
            self._canvas.delete(self._canvas.create_rectangle(self.x, self.y, self.x + self.dino_width, self.y + self.dino_height, fill = Window.canvas_background))

class GObstacle:
    obstacle_width = 0
    obstacle_height = 0
    obstacle_altitude = 0
    x = 0
    y = win_height

    _background = 'red'
    _canvas = None
    _id = None

    def __init__(self, canvas, obstacle_width, obstacle_height, obstacle_altitude):
        self._canvas = canvas
        self.obstacle_width = obstacle_width
        self.obstacle_height = obstacle_height
        self.obstacle_altitude = obstacle_altitude

        self.y -= (self.obstacle_altitude + self.obstacle_height)

    def draw(self):
        self._id = self._canvas.create_rectangle(self.x, self.y, self.x + self.obstacle_width, self.y + self.obstacle_height, fill = self._background)

    def clean(self):
        if self._id != None:
            self._canvas.delete(self._id)
            self._canvas.delete(self._canvas.create_rectangle(self.x, self.y, self.x + self.obstacle_width, self.y + self.obstacle_height, fill = Window.canvas_background))

class Window(tk.Frame):
    canvas = None
    canvas_background = 'white'

    def __init__(self, master = None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title('Deeplodocus')
        self.master.resizable(False, False)
        self.master.geometry(f'{win_width}x{win_height}')

        # Canvas
        self.canvas = tk.Canvas(root, width = win_width, height = win_height, bg = self.canvas_background)
        self.canvas.pack()

    def client_exit(self):
        exit()

root = tk.Tk()
app = Window(root)

# Dino movement
mvmntD = np.sin(np.arange(0, np.pi, 0.05)) * 50 * k # Sine function
# mvmntD = [v * 75 * k for v in [(x / 100) ** 2 for x in range(100)] + [(x / 100) ** 2 for x in list(range(100))[::-1]]] # Square function

# Obstacle movement
mvmntO = [v + 100*k for v in ([x**2 * k * 0.1 for x in range(-50, 50)] + [x**2 * k * 0.1 for x in list(range(-50, 50))[::-1]])]

delay = int((1 / fps) * 1000)

f = Frame(app.canvas)

def loop(frame_count):
    f.dino_altitude = mvmntD[frame_count % len(mvmntD)]
    f.nearest_obstacle = mvmntO[frame_count % len(mvmntO)]
    f.obstacle_width = 40 * k
    f.obstacle_height = 15 * k
    f.obstacle_altitude = 35 * k

    f.clean()
    f.draw()

    root.update_idletasks()
    root.update()

    root.after(delay, loop, frame_count + 1)

root.after(delay, loop, 0)
root.mainloop()