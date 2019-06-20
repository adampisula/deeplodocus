import tkinter as tk
import numpy as np
import time
import matplotlib.pyplot as plt
import json

k = 2
win_width = 600 * k
win_height = 150 * k
fps = 30

class Frame:
    dino_altitude = 0 * k
    dino = None

    def draw(self, canvas):
        self.dino = GDino(canvas, self.dino_altitude)
        self.dino.draw()

    def clean(self):
        if self.dino != None:
            self.dino.clean()

    def export(self):
        return json.dumps({ "dino_altitude": self.dino_altitude / k})

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

mvmnt = np.sin(np.arange(0, np.pi, 0.05)) * 50 * k # Sine function
# mvmnt = [v * 75 * k for v in [(x / 100) ** 2 for x in range(100)] + [(x / 100) ** 2 for x in list(range(100))[::-1]]] # Square function

delay = int((1 / fps) * 1000)

f = Frame()

def loop(frame_count):
    f.dino_altitude = mvmnt[frame_count % len(mvmnt)]

    f.clean()
    f.draw(app.canvas)

    root.update_idletasks()
    root.update()

    root.after(delay, loop, frame_count + 1)

root.after(delay, loop, 0)
root.mainloop()