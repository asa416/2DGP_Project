from pico2d import *

class Turtle:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('turtle.png')
        self.frame = 0
        self.x_max, self.x_min = self.x + 20, self.x - 20
        self.dir = 1

    def update(self):
        self.x += self.dir
        self.frame = (self.frame + 1) % 2
        if self.x > self.x_max:
            self.dir = -1
        elif self.x < self.x_min:
            self.dir = 1

    def draw(self):
        self.image.clip_draw(120 + self.frame * 60, 135, 60, 60, self.x, self.y, 50, 50)

class Goom:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('goom.png')
        self.frame = 0
        self.dir = 1
        self.x_max = self.x + 20
        self.x_min = self.x - 20

    def update(self):
        self.x += self.dir * 1
        self.frame = (self.frame + 1) % 20
        if self.x > self.x_max:
            self.dir = -1
        elif self.x < self.x_min:
            self.dir = 1

    def draw(self):
        self.image.clip_draw((self.frame // 10) * 45 + 1, 0, 45, 45, self.x, self.y, 50, 50)

