from pico2d import *
import object

class Map1:
    def __init__(self, x, y):
        self.blocks1 = [object.Block() for i in range(31)]
        block_list1 = []
        for i in range(31):
            block_list1.append((i * 30, 15))
        self.blocks2 = [object.Block() for i in range(31)]
        block_list2 = []
        for i in range(31):
            block_list2.append((i * 30, 45))

    def draw(self):
