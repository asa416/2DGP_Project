from pico2d import *
from ground import grounds
import object
import back
import backlayer

class Map1:
    def __init__(self):
        self.groundNum = len(grounds)
        self.groundblock = backlayer.GroundBlock()
        self.back = back.Back()
        self.background = load_image('sky.png')
        self.camera = 0

    def set_camera(self, c):
        self.camera = c

    def update(self):
        self.back.update()

    def draw(self):
        self.background.draw(400, 300, 800, 600)
        for i in range(self.groundNum):
            self.groundblock.draw(grounds[i][0] - self.camera, grounds[i][1])
        self.back.draw()

if __name__ == '__main__':
    open_canvas()
    num = len(grounds)
    groundblock = backlayer.GroundBlock()

    while True:
        clear_canvas()
        for i in range(num):
            groundblock.draw(grounds[i][0], grounds[i][1])
        update_canvas()