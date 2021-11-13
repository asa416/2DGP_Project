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

    def update(self):
        pass

    def get_camera(self):
        return self.x