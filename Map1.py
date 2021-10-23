from pico2d import *
from ground import grounds
import object
import back
import backlayer
import enemy


treePos = [100, 600, 1100, 1800]
grassPos = [150, 650, 1150, 1850]
goomPos = [300, 3000, 3300, 6000, 7000, 7300, 8000]
turtlePos = [1000, 1100, 2300, 2400, 5500, 7500]
block2Pos = [500, 550, 600, 650]
pipePos = [3000, 5200]
coinPos = [500, 550, 600, 650]

class Map1:
    def __init__(self):
        self.groundNum = len(grounds)
        self.groundblock = backlayer.GroundBlock()
        self.back = back.Back()
        self.background = load_image('sky.png')
        self.tree = backlayer.Tree()
        self.grass = backlayer.Grass()
        self.goalin = backlayer.GoalIn()
        self.camera = 0
        self.treeNum = len(treePos)
        self.grassNum = len(grassPos)
        self.gooms = [enemy.Goom(goomPos[i], 105) for i in range(len(goomPos))]
        self.turtles = [enemy.Turtle(turtlePos[i], 115) for i in range(len(turtlePos))]
        self.block2s = [object.UneasyBlock(block2Pos[i], 250) for i in range(len(block2Pos))]
        self.pipes = [object.Pipe(pipePos[i]) for i in range(len(pipePos))]
        self.coins = [object.Coin(coinPos[i], 300) for i in range(len(coinPos))]

    def set_camera(self, c):
        self.camera = c
        for goom in self.gooms:
            goom.set_camera(self.camera)
        for turtle in self.turtles:
            turtle.set_camera(self.camera)
        for block2 in self.block2s:
            block2.set_camera(self.camera)
        for pipe in self.pipes:
            pipe.set_camera(self.camera)
        for coin in self.coins:
            coin.set_camera(self.camera)

    def update(self):
        for goom in self.gooms:
            goom.update()
        for turtle in self.turtles:
            turtle.update()
        for coin in self.coins:
            coin.update()
        self.back.update()

    def draw(self):
        self.background.draw(400, 300, 800, 600)
        for i in range(self.treeNum):
            self.tree.draw(treePos[i] - self.camera)
        for i in range(self.grassNum):
            self.grass.draw(grassPos[i] - self.camera)
        self.goalin.draw(9600 - self.camera)
        for i in range(self.groundNum):
            self.groundblock.draw(grounds[i] - self.camera)
        for goom in self.gooms:
            goom.draw()
        for turtle in self.turtles:
            turtle.draw()
        self.back.draw()
        for block2 in self.block2s:
            block2.draw()
        for pipe in self.pipes:
            pipe.draw()
        for coin in self.coins:
            coin.draw()

if __name__ == '__main__':
    open_canvas()
    num = len(grounds)
    groundblock = backlayer.GroundBlock()

    while True:
        clear_canvas()
        for i in range(num):
            groundblock.draw(grounds[i][0])
        update_canvas()