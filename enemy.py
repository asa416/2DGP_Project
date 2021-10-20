from pico2d import *

class Turtle:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('turtle.png')
        self.frame = 0
        self.x_max, self.x_min = self.x + 50, self.x - 50
        self.dir = 1

    def update(self):
        self.x += self.dir
        self.frame = (self.frame + 1) % 20
        if self.x > self.x_max:
            self.dir = -1
        elif self.x < self.x_min:
            self.dir = 1

    def draw(self):
        self.image.clip_draw(120 + (self.frame // 10) * 60, 135, 60, 60, self.x, self.y, 50, 50)

class Goom:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.image = load_image('goom.png')
        self.frame = 0
        self.dir = 1
        self.x_max = self.x + 50
        self.x_min = self.x - 50

    def update(self):
        self.x += self.dir * 1
        self.frame = (self.frame + 1) % 20
        if self.x > self.x_max:
            self.dir = -1
        elif self.x < self.x_min:
            self.dir = 1

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def draw(self):
        self.image.clip_draw((self.frame // 10) * 45 + 1, 0, 45, 45, self.x, self.y, 50, 50)

class Boss:
    def __init__(self):
        self.image = load_image('boss.png')
        self.x = 600
        self.y = 95
        self.frame = 0
        self.dir = 1
        self.speed = 1

    def findCharacter(self, x):
        if self.x < x:
            self.dir = 1
        else:
            self.dir = -1

    def update(self, x):
        self.findCharacter(x)
        self.x += self.dir * self.speed
        self.frame = (self.frame + 1) % 40

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(80 * (self.frame // 10), 40, 80, 70, self.x, self.y)
        else:
            self.image.clip_draw(80 * (self.frame // 10), 150, 80, 70, self.x, self.y)