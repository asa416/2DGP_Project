from pico2d import *
import object
from stagepos import *

class Stage1Obstacle:
    def __init__(self):
        self.ground = [object.GroundBlock(Pos1.grounds[i]) for i in range(len(Pos1.grounds))]
        self.block2s = [object.UneasyBlock(Pos1.blockPos200[i], 200) for i in range(len(Pos1.blockPos200))]
        self.block3s = [object.UneasyBlock(Pos1.blockPos300[i], 350) for i in range(len(Pos1.blockPos300))]
        self.obstacleBlock = [object.Obstacle(Pos1.obstaclePos[i][0], Pos1.obstaclePos[i][1]) for i in range(len(Pos1.obstaclePos))]
        self.pipes = [object.Pipe(Pos1.pipePos[i]) for i in range(len(Pos1.pipePos))]
        self.coins = [object.Coin(Pos1.coinPos[i][0], Pos1.coinPos[i][1], 1) for i in range(len(Pos1.coinPos))]
        self.randombox = [object.RandomBox(Pos1.randomBoxPos[i], 200) for i in range(len(Pos1.randomBoxPos))]
        self.plag = object.Plag(Pos1.goalinPos)


class Stage2Obstacle:
    def __init__(self):
        self.ground = [object.GroundBlock(Pos2.grounds[i]) for i in range(len(Pos2.grounds))]
        self.block2s = [object.UneasyBlock(Pos2.blockPos200[i], 200) for i in range(len(Pos2.blockPos200))]
        self.block3s = [object.UneasyBlock(Pos2.blockPos350[i], 350) for i in range(len(Pos2.blockPos350))]
        self.obstacleBlock = [object.Obstacle(Pos2.obstaclePos[i][0], Pos2.obstaclePos[i][1]) for i in range(len(Pos2.obstaclePos))]
        self.pipes = [object.Pipe(Pos2.pipePos[i]) for i in range(len(Pos2.pipePos))]
        self.coins = [object.Coin(Pos2.coinPos[i][0], Pos2.coinPos[i][1], 1) for i in range(len(Pos2.coinPos))]
        self.randombox = [object.RandomBox(Pos2.randomBoxPos[i], 200) for i in range(len(Pos2.randomBoxPos))]
        self.plag = object.Plag(Pos2.goalinPos)


class BossObstacle:
    def __init__(self):
        self.ground = [object.BossBlock(PosBoss.grounds[i][0], PosBoss.grounds[i][1], 'floor') for i in range(len(PosBoss.grounds))]
        self.block2s = []
        self.block3s = []
        self.obstacleBlock = []
        self.pipes = []
        self.coins = []
        self.randombox = []
        self.plag = None