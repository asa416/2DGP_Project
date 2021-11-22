from pico2d import *

import game_framework
import game_world

class Camera:
    def __init__(self):
        self.x = 0

    def set_camera(self, x):
        if x > 400:
            self.x = 0.8 * self.x + 0.2 * (x - 400)

    def draw(self):
        pass

    def update(self):
        pass

    def get_camera(self):
        return self.x