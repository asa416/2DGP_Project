from pico2d import *
import server
import game_framework
import collision

ITEM_SPEED_PPS = 100.0
GRAVITY_PPSS = -1.0

class Mushroom:
    def __init__(self, x, y):
        self.image = load_image('./image/mush.png')
        self.x, self.y = x, y
        self.w, self.h = 30, 30
        self.camera = 0
        self.showing = False
        self.jumpTime = 0.0
        self.dir = 1
        self.speed = ITEM_SPEED_PPS
        self.landing = False

    def show_mush(self):
        self.showing = True
        self.jumpTime = 0.0

    def get_bb(self):
        return self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2

    def set_camera(self):
        self.camera = server.cam.get_camera()

    def update(self):
        self.set_camera()
        if self.showing:
            self.x += self.speed * game_framework.frame_time * self.dir
            self.jumpTime += game_framework.frame_time
            landing = False
            for ground in server.obstacles.ground.copy() + server.obstacles.block2s.copy() + server.obstacles.block3s.copy() + server.obstacles.randombox.copy() + server.obstacles.pipes.copy() + server.obstacles.obstacleBlock.copy():
                if collision.collide(self, ground):
                    if self.y > ground.y + ground.h / 2:
                        landing = True
                        # self.y = ground.y + 50
                        self.jumpTime = 0.0
                    else:
                        self.dir *= -1
                    break
            if not landing:
                self.y += (GRAVITY_PPSS * self.jumpTime ** 2 / 2)
            for obs in server.obstacles.pipes.copy() + server.obstacles.obstacleBlock.copy():
                if collision.collide(self,obs):
                    self.dir *= -1
                    break
            if collision.collide(self, server.char):
                self.showing = False
                server.char.fire_grow()

    def draw(self):
        if self.showing:
            self.image.draw(self.x - self.camera, self.y, self.w, self.h)
            if game_framework.DebugingMode == 1:
                draw_rectangle(*self.get_bb())