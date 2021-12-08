from pico2d import *
import game_framework
import game_world
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
FRAMES_PER_ACTION_BOSS = 4


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
    def __init__(self, x, y):
        self.image = load_image('./image/boss.png')
        self.x, self.y = x , y
        self.w, self.h = 80, 80
        self.dir = 1
        self.timer = 1.0
        self.frame = 0
        self.speed = 1
        self.jump_speed = 3
        self.camera = 0
        self.jump_time = 0.0
        self.fire = []
        self.jump_or_fire = "fire"
        self.build_behavior_tree()

    def wander(self):
        self.speed = ENEMY_SPEED_PPS
        self.timer -= game_framework.frame_time
        self.x += self.speed * game_framework.frame_time * self.dir
        if self.timer <= 0:
            self.timer = 1.0
            self.dir *= -1
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def jump(self):
        self.jump_time += game_framework.frame_time
        self.y += self.jump_speed * self.jump_time - 10 * self.jump_time ** 2 / 2
        for bridge in server.obstacles.bridge:
            if collision.collide(self, bridge):
                self.y = bridge.y + bridge.h / 2 + self.h / 2
                self.jump_time = 0.0
                self.jump_or_fire = 'fire'
                return BehaviorTree.SUCCESS
        return BehaviorTree.RUNNING

    def check_ground(self):
        for bridge in server.obstacles.bridge:
            if collision.collide(self, bridge):
                return BehaviorTree.FAIL
        return BehaviorTree.SUCCESS

    def die(self):
        self.y -= 20
        if self.y < 0:
            server.enemies.monster.clear()
            game_world.remove_object(self)
        else:
            return BehaviorTree.RUNNING

    def build_behavior_tree(self):
        wander_node = LeafNode("wander", self.wander)
        jump_node = LeafNode("jump", self.jump)
        fire_node = LeafNode("fire", self.fireball)

        die_node = LeafNode("die", self.die)
        check_ground_node = LeafNode("check", self.check_ground)
        check_die_node = SequenceNode("check die")
        check_die_node.add_children(check_ground_node, die_node)

        jump_fire_node = SelectorNode("jump or fire")
        jump_fire_node.add_children(check_die_node, fire_node, jump_node)

        main_node = SequenceNode("main")
        main_node.add_children(wander_node, jump_fire_node)

        self.bt = BehaviorTree(main_node)

    def fireball(self):
        if self.jump_or_fire == 'jump':
            return BehaviorTree.FAIL
        self.jump_or_fire = 'jump'
        server.enemies.fireball.append(FireBall(self.x, self.y))
        print("fire")
        return BehaviorTree.SUCCESS

    def set_camera(self):
        self.camera = server.cam.get_camera()

    def update(self):
        self.set_camera()
        self.bt.run()
        self.frame = (self.frame + FRAMES_PER_ACTION_BOSS * ACTION_PER_TIME * game_framework.frame_time) % 2

    def get_bb(self):
        return self.x - self.camera - self.w / 2, self.y - self.h / 2, self.x - self.camera + self.w / 2, self.y + self.h / 2

    def draw(self):
        self.image.clip_draw(80 * int(self.frame), 150, 80, 70, self.x - self.camera, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())

class FireBall:
    image = None
    def __init__(self, x, y):
        if FireBall.image is None:
            FireBall.image = load_image('./image/fireball.png')

        game_world.add_object(self, 3)
        self.x, self.y = x, y
        self.speed = 500
        self.camera = 0
        self.w, self.h = 55, 17
        self.frame = 0

    def update(self):
        self.set_camera()
        self.x -= self.speed * game_framework.frame_time
        self.frame = (self.frame + FRAMES_PER_ACTION_GOOM * ACTION_PER_TIME * game_framework.frame_time) % 2
        if self.x < 3000:
            server.enemies.fireball.remove(self)
            game_world.remove_object(self)

    def set_camera(self):
        self.camera = server.cam.get_camera()

    def get_bb(self):
        return self.x - self.camera - self.w / 2, self.y - self.h / 2, self.x - self.camera + self.w / 2, self.y + self.h / 2

    def draw(self):
        self.image.clip_draw(int(self.frame) * 45 + 1, 0, 45, 45, self.x - self.camera, self.y, self.w, self.h)
        draw_rectangle(*self.get_bb())
