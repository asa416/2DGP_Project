from pico2d import *

class TimerObject:
    def __init__(self, t):
        self.font = load_font('ENCR10B.TTF', 32)
        self.limitTime = t * 60 # min > sec
        self.leftTime = 0.0
        self.startTime = get_time()
        self.on = True
        self.m, self.sec = 0, 0

    def update(self):
        if self.on:
            self.leftTime = self.limitTime - (get_time() - self.startTime)
            self.m = int(self.leftTime)
            self.sec = (self.leftTime - self.m) * 100

    def stop(self):
        self.on = False

    def draw(self):

        self.font.draw(get_canvas_width() - 110, get_canvas_height() - 20, 'TIME', (255, 255, 255))
        self.font.draw(get_canvas_width() - 130, get_canvas_height() - 50, '%d:%d' % (self.m, self.sec), (255, 255, 255))
