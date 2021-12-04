from pico2d import *
import game_framework
import server
import collision
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode

PIXEL_PER_METER = (10.0 / 0.1)
ENEMY_SPEED_KMPS = 5.0
ENEMY_SPEED_PPS = (ENEMY_SPEED_KMPS * 1000.0 / 60.0 / 60.0 * PIXEL_PER_METER)

TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION_TURTLE = 2
FRAMES_PER_ACTION_GOOM = 2


class Turtle:
    image = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        if Turtle.image == None:
            Turtle.image = load_image('./image/turtle.png')
        self.frame = 0
        self.speed = 0
        self.x_max, self.x_min = self.x + 100, self.x - 100
        self.dir = 1
        self.timer = 1.0
        self.camera = 0
        self.w, self.h = 50, 50
        self.build_behavior_tree()

    def update(self):
        self.set_camera()
        self.bt.run()
        # self.x += self.velocity * game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION_TURTLE * ACTION_PER_TIME * game_framework.frame_time) % 2
        self.x += self.speed * game_framework.frame_time * self.dir
        # if self.x > self.x_max:
        #     self.velocity *= -1
        # elif self.x < self.x_min:
        #     self.velocity *= -1

    def wander(self):
        self.speed = ENEMY_SPEED_PPS
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.timer = 1.0
            self.dir *= -1
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        wnader_node = LeafNode("wander", self.wander)

        self.bt = BehaviorTree(wnader_node)

    def set_camera(self):
        self.camera = server.cam.get_camera()

    def get_bb(self):
        return self.x - self.camera - self.w / 2, self.y - self.h / 2, self.x - self.camera + self.w / 2, self.y + self.h / 2

    def draw(self):
        if self.dir > 0:
            self.image.clip_composite_draw(120 + int(self.frame) * 60, 135, 60, 60, 0, 'h', self.x - self.camera, self.y, self.w, self.h)
        else:
            self.image.clip_draw(120 + int(self.frame) * 60, 135, 60, 60, self.x - self.camera, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())



class Goom:
    image = None

    def __init__(self, x, y):
        self.x, self.y = x, y
        if Goom.image == None:
            Goom.image = load_image('./image/goom.png')
        self.frame = 0
        self.speed = 0
        self.x_max = self.x + 100
        self.x_min = self.x - 100
        self.camera = 0
        self.timer = 1.0
        self.dir = 1
        self.w, self.h = 50, 50
        self.build_behavior_tree()

    def update(self):
        self.set_camera()
        self.bt.run()
        self.x += self.speed * game_framework.frame_time * self.dir
        self.frame = (self.frame + FRAMES_PER_ACTION_GOOM * ACTION_PER_TIME * game_framework.frame_time) % 2

    def wander(self):
        self.speed = ENEMY_SPEED_PPS
        self.timer -= game_framework.frame_time
        if self.timer <= 0:
            self.timer = 1.0
            self.dir *= -1
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        wander_node = LeafNode("wander", self.wander)
        self.bt = BehaviorTree(wander_node)

    def set_camera(self):
        self.camera = server.cam.get_camera()

    def get_bb(self):
        return self.x - self.camera - self.w / 2, self.y - self.h / 2, self.x - self.camera + self.w / 2, self.y + self.h / 2

    def draw(self):
        self.image.clip_draw(int(self.frame) * 45 + 1, 0, 45, 45, self.x - self.camera, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())


class Boss:
    def __init__(self):
        self.image = load_image('./image/boss.png')
        self.x = 600
        self.y = 165
        self.w, self.h = 80, 80
        self.frame = 0
        self.dir = 1
        self.speed = 1
        self.camera = 0

    def set_camera(self, c):
        self.camera = c

    def findCharacter(self):
        if self.x - self.camera < 400:
            self.dir = 1
        else:
            self.dir = -1

    def update(self):
        self.findCharacter()
        # self.x += self.dir * self.speed
        self.frame = (self.frame + 1) % 40

    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(80 * (self.frame // 10), 40, 80, 70, self.x - self.camera, self.y, self.w, self.h)
        else:
            self.image.clip_draw(80 * (self.frame // 10), 150, 80, 70, self.x - self.camera, self.y, self.w, self.h)