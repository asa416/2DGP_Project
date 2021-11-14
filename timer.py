from pico2d import *

class TimerObject:
    def __init__(self, t):
        self.font = load_font('ENCR10B.TTF', 32)
        self.limitTime = t * 60 # min > sec
        self.leftTime = 0.0
        self.startTime = get_time()

    def update(self):
        pass

    def draw(self):
        self.leftTime = self.limitTime - (get_time() - self.startTime)
        m = int(self.leftTime)
        sec = (self.leftTime - m) * 100
        self.font.draw(get_canvas_width() - 110, get_canvas_height() - 20, 'TIME', (255, 255, 255))
        self.font.draw(get_canvas_width() - 130, get_canvas_height() - 50, '%d:%d' % (m, sec), (255, 255, 255))
