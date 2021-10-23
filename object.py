from pico2d import *

class Block:
    lmage = None
    x, y = 100, 100
    w, h = 50, 50
    state = False
    camera = 0

    def get_camera(self, c):
        self.camera = c

    def update(self):
        pass

    def get_bb(self):
        return self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2

    def draw(self):
        self.image.draw(self.x - self.camer, self.y - self.camera, self.w, self.h)
        draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2 - self.camera, self.x + self.w / 2 - self.camera, self.y + self.h / 2 - self.camera)

class RandomBox(Block):
    def __init__(self):
        self.image = load_image('randombox.png')
        state = True
        self.num = 1
        # self.item = 1

    def update(self):
        if self.num != 0:
            pass



class Pipe:
    def __init__(self, x, y):
        self.image = load_image('pipeline.png')
        self.x, self.y = x, y
        self.xsize, self.ysize = 66, 140
        self.camera = 0

    def get_camera(self, c):
        self.camera = c

    def get_bb(self):
        return self.x - self.xsize / 2, self.y - self.ysize / 2, self.x + self.xsize / 2, self.y + self.ysize / 2

    def draw(self):
        self.image.draw(self.x - self.camera, self.y - self.camera)
        draw_rectangle(self.x - self.xsize / 2 - self.camera, self.y - self.ysize / 2 - self.camera, self.x + self.xsize / 2 - self.camera, self.y + self.ysize / 2 - self.camera)