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


class GroundBlock:
    image = None

    def __init__(self, x):
        self.x, self.y = x, 50
        self.w, self.h = 50, 50
        self.camera = 0
        if GroundBlock.image == None:
            GroundBlock.image = load_image('./image/block.png')

    def set_camera(self, c):
        self.camera = c

    def update(self):
        pass

    def get_bb(self):
        return self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2

    def draw(self):
        self.image.draw(self.x - self.camera, self.y - 50, self.w, self.h)
        self.image.draw(self.x - self.camera, self.y, self.w, self.h)
        draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2)


class RandomBox:
    image = None

    def __init__(self, x, y):
        if RandomBox.image == None:
            RandomBox.image = load_image('./image/randombox.png')
        self.x, self.y = x, y
        state = True
        self.num = 1
        self.camera = 0
        self.w, self.h = 50, 50
        # self.item = 1

    def set_camera(self, c):
        self.camera = c

    def update(self):
        if self.num != 0:
            pass

    def draw(self):
        self.image.draw(self.x - self.camera, self.y, self.w, self.h)
        draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2)


class UneasyBlock:
    image = None

    def __init__(self, x, y):
        if UneasyBlock.image == None:
            UneasyBlock.image = load_image('./image/block2.png')
        self.x, self.y = x, y
        self.w, self.h = 50, 50
        self.frame = 0
        self.camera = 0

    def set_camera(self, c):
        self.camera = c

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x - self.camera, self.y, self.w, self.h)
        draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2)


class EasyBlock:
    image = None

    def __init__(self, x, y):
        if EasyBlock.image == None:
            EasyBlock.image = load_image('./image/block3.png')
        self.x, self.y = x, y
        self.w, self.h = 50, 50
        self.camera = 0

    def set_camera(self, c):
        self.camera = c

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x - self.camera, self.y, self.w, self.h)
        draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2)


class BossBlock(Block):
    def __init__(self, x, y):
        self.image = load_image('./image/bossblock.png')
        self.w, self.h = 30, 50
        self.x, self.y = x, y


class BossGround:
    def __init__(self, x, y):
        self.image = load_image('./image/bossground.png')
        self.x, self.y = x, y
        self.camera = 0

    def set_camera(self, c):
        self.camera = c

    def draw(self):
        self.image.draw(self.x - self.camera, self.y)


class Pipe:
    image = None

    def __init__(self, x):
        if Pipe.image == None:
            Pipe.image = load_image('./image/pipeline.png')
        self.x = x
        self.y = 145
        self.xsize, self.ysize = 66, 140
        self.camera = 0

    def set_camera(self, c):
        self.camera = c

    def update(self):
        pass

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
    state = 0 # 0 small 1 big

    def __init__(self, x, y, s):
        self.image = load_image('./image/coin.png')
        self.x, self.y = x, y
        self.state = s
        if self.state == 0:
            self.w, self.h = 30, 30
        else:
            self.w, self.h = 50, 50

    def set_camera(self, c):
        self.camera = c

    def update(self):
        self.frame = (self.frame + 1) % 60

    def get_bb(self):
        return self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2

    def draw(self):
        self.image.clip_draw(120 * (self.frame // 10), 0, 120, 115, self.x - self.camera, self.y, self.w, self.h)
        draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2)


class Ax:
    def __init__(self, x, y):
        self.image = load_image('./image/ax.png')
        self.x, self.y = x, y
        self.w, self.h = 50, 50
        self.camera = 0

    def set_camera(self, c):
        self.camera = c

    def get_bb(self):
        return self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2

    def draw(self):
        self.image.draw(self.x - self.camera, self.y, self.w, self.h)
        draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera,
                       self.y + self.h / 2)

class Plag:
    def __init__(self, x):
        self.image = load_image('./image/goal.png')
        self.w, self.h = 60, 450
        self.x, self.y = x, 297
        self.camera = 0

    def set_camera(self, c):
        self.camera = c

    def update(self):
        pass

    def draw(self):
        self.image.draw(self.x - self.camera, self.y, self.w, self.h)
        draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2)