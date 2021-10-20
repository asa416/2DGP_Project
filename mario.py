from pico2d import *

g = -1
MAX_SPEED = 8
ACCEL = 0.2

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image('mario.png')
        self.frame = 0
        self.running = False
        self.oldx, self.oldy = x, y
        self.dir = 0
        self.speed = 1
        self.jump = False
        self.t = 0

    def update(self):
        if self.dir != 0:
            self.running = True
            if self.speed < MAX_SPEED:
                self.speed = self.speed + ACCEL * 0.5
            self.x += self.dir * self.speed
            self.frame = (self.frame + 1) % 4
        if self.jump:
            ySpeed = 5
            self.y = self.y + ySpeed * self.t + (g * self.t * self.t) / 2
            self.t += 0.4
            if self.y < self.oldy:
                self.y = self.oldy
                self.jump = False

    def get_bb(self):
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def get_x(self):
        return self.x

    def worldMapMove(self, x, y):
        self.x = x
        self.y = y

    def handleEvent(self, e):
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_LEFT:
                self.dir -= 1
            elif e.key == SDLK_RIGHT:
                self.dir += 1
            elif e.key == SDLK_UP:
                if self.jump == False:
                    self.jump = True
                    self.t = 0
                    self.oldy = self.y
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:
                self.dir += 1
                self.speed = 1
                self.running = False
            elif e.key == SDLK_RIGHT:
                self.speed = 1
                self.dir -= 1
                self.running = False

    def draw(self):
        if self.running:
            if self.frame < 3:
                self.image.clip_draw(160 + self.frame * 40, 339, 40, 40, self.x, self.y, 50, 50)
            else:
                self.image.clip_draw(160 + (4 - self.frame) * 40, 339, 40, 40, self.x, self.y, 50, 50)
        else:
            self.image.clip_draw(2, 339, 40, 40, self.x, self.y, 50, 50)

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_LEFT:
                pass


running = True

if __name__ == '__main__':


    open_canvas()
    mario = Mario()

    while running:
        handle_events()
        mario.update()

        clear_canvas()
        mario.draw()
        update_canvas()
        delay(1)

    close_canvas()
