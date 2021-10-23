from pico2d import *

class Block:
    image = None
    x, y = 100, 100
    w, h = 50, 50
    state = False
    camera = 0

    def set_camera(self, c):
        self.camera = c

    def update(self):
        pass

    def get_bb(self):
        return self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2

    def draw(self):
        self.image.draw(self.x - self.camera, self.y, self.w, self.h)
        draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2)

class RandomBox(Block):
    def __init__(self, x, y):
        self.image = load_image('randombox.png')
        self.x, self.y = x, y
        state = True
        self.num = 1
        # self.item = 1

    def update(self):
        if self.num != 0:
            pass

class UneasyBlock(Block):
    def __init__(self, x, y):
        self.image = load_image('block2.png')
        self.x, self.y = x, y
        self.frame = 0

class EasyBlock(Block):
    def __init__(self):
        self.image = load_image('block3.png')

class Pipe:
    def __init__(self, x):
        self.image = load_image('pipeline.png')
        self.x = x
        self.y = 70
        self.xsize, self.ysize = 66, 140
        self.camera = 0

    def set_camera(self, c):
        self.camera = c

    def get_bb(self):
        return self.x - self.xsize / 2 - self.camera, self.y - self.ysize / 2, self.x + self.xsize / 2 - self.camera, self.y + self.ysize / 2

    def draw(self):
        self.image.draw(self.x - self.camera, self.y)
        draw_rectangle(self.x - self.xsize / 2 - self.camera, self.y - self.ysize / 2, self.x + self.xsize / 2 - self.camera, self.y + self.ysize / 2)

class Coin:
    image = None
    w, h = 30, 30
    camera = 0
    frame = 0

    def __init__(self, x, y):
        self.image = load_image('coin.png')
        self.x, self.y = x, y

    def set_camera(self, c):
        self.camera = c

    def update(self):
        self.frame = (self.frame + 1) % 60

    def get_bb(self):
        return self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2

    def draw(self):
        self.image.clip_draw(120 * (self.frame // 10), 0, 120, 115, self.x - self.camera, self.y, self.w, self.h)
        draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2)