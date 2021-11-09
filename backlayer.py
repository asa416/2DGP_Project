from pico2d import *

class Tree:
    def __init__(self):
        self.image = load_image('./image/tree.png')

    def draw(self, x):
        self.image.draw(x, 140)

class GoalIn:
    def __init__(self):
        self.image = load_image('./image/goalin.png')

    def draw(self, x):
        self.image.draw(x, 230, 400, 300)

class Grass:
    def __init__(self):
        self.image = load_image('./image/grass.png')

    def draw(self, x):
        self.image.draw(x, 105)

class Fire:
    def __init__(self):
        self.image = load_image('./image/fire.png')

    def draw(self, x):
        self.image.draw(x, 40)

class Cloud:
    def __init__(self):
        self.image = load_image('./image/back.png')

    def draw(self, x):
        self.image.clip_draw(100, 365, 100, 60, x, 400)
