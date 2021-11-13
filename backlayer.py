from pico2d import *

class Tree:
    image = None
    def __init__(self):
        if Tree.image == None:
            Tree.image = load_image('./image/tree.png')
        self.y = 125

    def draw(self, x):
        self.image.draw(x, self.y)

class GoalIn:
    def __init__(self):
        self.image = load_image('./image/goalin.png')

    def draw(self, x):
        self.image.draw(x, 210, 400, 300)

class Grass:
    image = None
    def __init__(self):
        if Grass.image == None:
            Grass.image = load_image('./image/grass.png')
        self.y = 95

    def draw(self, x):
        self.image.draw(x, self.y)

class Fire:
    image = None
    def __init__(self):
        if Fire.image == None:
            Fire.image = load_image('./image/fire.png')
        self.y = 40

    def draw(self, x):
        self.image.draw(x, self.y)

class Cloud:
    image = None
    def __init__(self):
        if Cloud.image == None:
            Cloud.image = load_image('./image/back.png')
        self.y = 400

    def draw(self, x):
        self.image.clip_draw(100, 365, 100, 60, x, self.y)
