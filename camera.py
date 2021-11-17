from pico2d import *

import game_framework
import game_world

class Camera:
    def __init__(self):
        self.x = 0
        self.velocity = 1

    def set_camera(self, x):
        self.x = x

    def draw(self):
        pass

    def update(self, target):
        if target > 400:
            self.x = 0.8 * self.x + 0.2 * (target - 400)


    def get_camera(self):
        return self.x