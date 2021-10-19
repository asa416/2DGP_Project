from pico2d import *

class Block:
    def __init__(self):
        self.image = load_image('block.png')

    def draw(self, x, y):
        self.image.draw(x, y, 30, 30)