from pico2d import *

class Back:
    def __init__(self):
        self.image = load_image('back.png')
        self.x, self.y = 200, 400

    def update(self):
        self.x -= 1
        if self.x < -500:
            self.x = 900

    def draw(self):
        self.image.clip_draw(100, 365, 100, 60, self.x, self.y)
        self.image.clip_draw(100, 365, 100, 60, self.x + 400, self.y - 20)
        # self.image.clip_draw(140, 270, 160, 85, self.x + 300, 70, 400, 200)