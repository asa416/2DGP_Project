from pico2d import *

import enemy
import object
import backlayer

xPos = [0, 0, 0, 30, 60, 90, 120, 150, 180, 210, 210, 210]
yPos = [100, 50, 0, 0, 0, 0, 0, 0, 0, 0, 50, 100]
gPos = [265, 325, 405, 485, 565, 645, 680]


class BossMap:
    def __init__(self):
        self.boss = enemy.Boss()
        self.fire = backlayer.Fire()
        self.blocks = [object.BossBlock(xPos[i], yPos[i]) for i in range(len(xPos))]
        self.camera = 0
        self.bossgrounds = [object.BossGround(gPos[i], 110) for i in range(len(gPos))]

    def update(self):
        self.boss.update()

    def set_camera(self, c):
        self.camera = c
        self.boss.set_camera(c)
        for block in self.blocks:
            block.set_camera(c)
        for ground in self.bossgrounds:
            ground.set_camera(c)

    def draw(self):
        for i in range(5):
            self.fire.draw(260 + 100 * i - self.camera)
        for block in self.blocks:
            block.draw()
        for ground in self.bossgrounds:
            ground.draw()
        self.boss.draw()


