from pico2d import *
import object
import backlayer
import enemy
from stagepos import *
import server

class Stage1BG:
    def __init__(self):
        self.background = load_image('./image/sky.png')
        self.tree = backlayer.Tree()
        self.grass = backlayer.Grass()
        self.cloud = backlayer.Cloud()
        self.goalin = backlayer.GoalIn()
        self.camera = 0

    def set_camera(self):
        self.camera = server.cam.get_camera()

    def update(self):
        self.set_camera()


    def draw(self):
        self.background.draw(400, 300, 800, 600)
        for i in range(len(Pos1.trees)):
            self.tree.draw(Pos1.trees[i] - self.camera)
        for i in range(len(Pos1.grass)):
            self.grass.draw(Pos1.grass[i] - self.camera)
        for i in range(len(Pos1.clouds)):
            self.cloud.draw(Pos1.clouds[i] - self.camera)
        self.goalin.draw(6800 - self.camera)

class Stage2BG:
    def __init__(self):
        self.background = load_image('./image/sky.png')
        self.tree = backlayer.Tree()
        self.grass = backlayer.Grass()
        self.cloud = backlayer.Cloud()
        self.goalin = backlayer.GoalIn()
        self.camera = 0

    def set_camera(self):
        self.camera = server.cam.get_camera()

    def update(self):
        self.set_camera()

    def draw(self):
        self.background.draw(400, 300, 800, 600)
        for i in range(len(Pos2.trees)):
            self.tree.draw(Pos2.trees[i] - self.camera)
        for i in range(len(Pos2.grass)):
            self.grass.draw(Pos2.grass[i] - self.camera)
        for i in range(len(Pos2.clouds)):
            self.cloud.draw(Pos2.clouds[i] - self.camera)
        self.goalin.draw(6800 - self.camera)
