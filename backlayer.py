from pico2d import *

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

class Fire:
    def __init__(self):
        self.image = load_image('fire.png')

    def draw(self, x):
        self.image.draw(x, 40)

# class Mountain:
#     def __init__(self):
#         self.image = load_image('')