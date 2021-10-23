from pico2d import *

class GroundBlock:
    def __init__(self):
        self.image = load_image('block.png')

    def draw(self, x):
        self.image.draw(x, 15, 50, 50)
        self.image.draw(x, 65, 50, 50)

class Tree:
    def __init__(self):
        self.image = load_image('tree.png')

    def draw(self, x):
        self.image.draw(x, 140)

class GoalIn:
    def __init__(self):
        self.image = load_image('goalin.png')

    def draw(self, x):
        self.image.draw(x, 230, 400, 300)

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')

    def draw(self, x):
        self.image.draw(x, 105)

# class Mountain:
#     def __init__(self):
#         self.image = load_image('')