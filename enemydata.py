import enemy
from stagepos import *

class Stage1Enemy:
    def __init__(self):
        self.monster = [enemy.Goom(Pos1.goomPos[i], 100) for i in range(len(Pos1.goomPos))] + [enemy.Turtle(Pos1.turtlePos[i], 100) for i in range(len(Pos1.turtlePos))]

class Stage2Enemy:
    def __init__(self):
        self.monster = [enemy.Goom(Pos2.goomPos[i], 100) for i in range(len(Pos2.goomPos))] + [enemy.Turtle(Pos2.turtlePos[i], 100) for i in range(len(Pos2.turtlePos))]

class BossStageEnemy:
    def __init__(self):
        self.monster = [enemy.Boss(5000, 300)]