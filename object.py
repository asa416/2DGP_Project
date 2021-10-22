from pico2d import *

class Block:
    def __init__(self, x, y):
        self.image = load_image('block.png')
        self.x, self.y = x, y

    def get_bb(self):
        return self.x - 15, self.y - 15, self.x + 15, self.y + 15

    def draw(self):
        self.image.draw(self.x, self.y, 30, 30)

class RandomBox:
    def __init__(self):
        self.image = load_image('randombox.png')

class Pipe:
    def __init__(self, x, y):
        self.image = load_image('pipeline.png')
        self.x, self.y = x, y
        self.xsize, self.ysize = 33, 70

    def get_bb(self):
        return self.x - self.xsize / 2, self.y - self.ysize / 2, self.x + self.xsize / 2, self.y + self.ysize

    def draw(self):
        self.image.draw(self.x, self.y)
