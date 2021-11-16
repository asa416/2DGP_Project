from pico2d import *

import game_framework
import game_world

class Camera:
    def __init__(self):
        self.x = 0

    def set_camera(self, x):
        self.x = x

    def draw(self):
        pass

    def update(self, target):
        if target > self.x + 400:
            self.x = target - 400
        elif target < self.x + 400 and self.x > 0:
            self.x = target - 400
    def get_camera(self):
        return self.x