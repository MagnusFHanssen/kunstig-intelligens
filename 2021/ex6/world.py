import numpy as np
from enum import Enum
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import colors
import matplotlib.figure
import PySimpleGUI as sg


class Terrain(Enum):
    NORMAL = 1
    BLOCK = 2
    START = 3
    GOAL = 4
    TRAP = 5


class World:
    cmap = colors.ListedColormap(['white', 'black', 'purple', 'yellow', 'red'])
    fig = matplotlib.figure.Figure(figsize=(5, 4))
    plt = fig.subplots()
    layout = [
        [sg.Text("Plot test")],
        [sg.Canvas(key="-CANVAS-")],
        [sg.Button("Ok")]
    ]
    blocks = set()
    traps = set()

    def __init__(self, height=4, width=5):
        self.height = height
        self.width = width
        self.map = np.ones((self.height, self.width))
        self.start = (0, 0)
        self.goal = (self.height-1, self.width-1)
        self.map[self.start[0]][self.start[1]] = 3
        self.map[self.goal[0]][self.goal[1]] = 4

    def set_start(self, row, col):
        self.map[self.start[0]][self.start[1]] = 1
        self.start = (row, col)
        self.map[self.start[0]][self.start[1]] = 3

    def set_goal(self, row, col):
        self.map[self.goal[0]][self.goal[1]] = 1
        self.goal = (row, col)
        self.map[self.goal[0]][self.goal[1]] = 4

    def add_block(self, row, col):
        if self.start is (row, col) or self.goal is (row, col):
            return False
        self.map[row][col] = 2
        self.blocks.add((row, col))

    def show_map(self):
        self.plt.pcolor(self.map, cmap=self.cmap, edgecolors='grey', linewidths=1)
        self.fig.gca().invert_yaxis()

        window = sg.Window(
            "Testing map in window",
            self.layout,
            location=(0, 0),
            finalize=True,
            element_justification="center",
            font="Helvetica 18"
        )

        draw_figure(window["-CANVAS-"].TKCanvas, self.fig)

        event, values = window.read()

        window.close()


def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side="top", fill="both", expand=1)
    return figure_canvas_agg
