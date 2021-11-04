from pico2d import *
#from ground import grounds
import object
import backlayer
import enemy
import stage2pos as Pos2



class Map2:
    def __init__(self):
        self.groundNum = len(Pos2.grounds)
        self.groundblock = [object.GroundBlock(Pos2.grounds[i]) for i in range(self.groundNum)]
        self.background = load_image('sky.png')
        # self.tree = backlayer.Tree()
        # self.grass = backlayer.Grass()
        # self.goalin = backlayer.GoalIn()
        self.camera = 0
        # self.treeNum = len(treePos)
        # self.grassNum = len(grassPos)
        self.gooms = [enemy.Goom(Pos2.goomPos[i], 100) for i in range(len(Pos2.goomPos))]
        self.turtles = [enemy.Turtle(Pos2.turtlePos[i], 100) for i in range(len(Pos2.turtlePos))]
        self.block2s = [object.UneasyBlock(Pos2.blockPos250[i], 250) for i in range(len(Pos2.blockPos250))]
        # self.obstacleBlock = [object.UneasyBlock(Pos2.obstaclePos[i][0], Pos2.obstaclePos[i][1]) for i in range(len(Pos2.obstaclePos))]
        self.pipes = [object.Pipe(Pos2.pipePos[i]) for i in range(len(Pos2.pipePos))]
        self.coins = [object.Coin(Pos2.coinPos[i][0], Pos2.coinPos[i][1], 1) for i in range(len(Pos2.coinPos))]

    def get_ground(self):
        return self.groundblock

    def set_camera(self, c):
        self.camera = c
        for goom in self.gooms:
            goom.set_camera(self.camera)
        for turtle in self.turtles:
            turtle.set_camera(self.camera)
        for block2 in self.block2s:
            block2.set_camera(self.camera)
        # for obs in self.obstacleBlock:
        #     obs.set_camera(self.camera)
        for pipe in self.pipes:
            pipe.set_camera(self.camera)
        for coin in self.coins:
            coin.set_camera(self.camera)
        for gb in self.groundblock:
            gb.set_camera(self.camera)

    def get_bb(self):
        for goom in self.gooms:
            goom.get_bb()

    def update(self):
        for goom in self.gooms:
            goom.update()
        for turtle in self.turtles:
            turtle.update()
        for coin in self.coins:
            coin.update()


    def draw(self):
        self.background.draw(400, 300, 800, 600)
        # for i in range(self.treeNum):
        #     self.tree.draw(treePos[i] - self.camera)
        # for i in range(self.grassNum):
        #     self.grass.draw(grassPos[i] - self.camera)
        # self.goalin.draw(9600 - self.camera)
        for gb in self.groundblock:
            gb.draw()
        for goom in self.gooms:
            goom.draw()
        for turtle in self.turtles:
            turtle.draw()
        for block2 in self.block2s:
            block2.draw()
        # for obs in self.obstacleBlock:
        #     obs.draw()
        for pipe in self.pipes:
            pipe.draw()
        for coin in self.coins:
            coin.draw()

if __name__ == '__main__':
    open_canvas()
    # num = len(grounds)
    # groundblock = backlayer.GroundBlock()

    while True:
        clear_canvas()
        # for i in range(num):
        #     pass
            # groundblock.draw(grounds[i][0])
        update_canvas()