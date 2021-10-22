from pico2d import *

class GroundBlock:
    def __init__(self):
        self.image = load_image('block.png')

    def draw(self, x, y):
        self.image.draw(x, y)

class Tree:
    def __init__(self):
        self.image = load_image('tree.png')

    def draw(self, x, y):
        self.image.draw(x, 80)

class GoalIn:
    def __init__(self):
        self.image = load_image('goalin.png')

    def draw(self, x, y):
        self.image.draw(x, y, 400, 300)

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self, x):
        self.image.draw(x, 80)