from pico2d import *
import game_world
# import time

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE = range(5)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}

class IdleState:
    def enter(Mario, event):
        pass

    def exit(Mario, event):
        pass

    def do(Mario):
        pass

    def draw(Mario):
        pass


class RunState:
    def enter(Mario, event):
        pass

    def exit(Mario, event):
        pass

    def do(Mario):
        pass

    def draw(Mario):
        pass


class JumpState:
    def enter(Mario, event):
        pass

    def exit(Mario, event):
        pass

    def do(Mario):
        pass

    def draw(Mario):
        pass


g = -10
MAX_SPEED = 8
ACCEL = 0.2
MAX_JUMP = 10
JUMP_TIME = 0


class Mario:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.image = load_image("./image/mario.png")
        self.frame = 0
        self.running = False
        self.oldx, self.oldy = self.x, self.y
        self.dir = 1
        self.velocity = 0
        self.fram = 0
        self.jump = False
        self.t = 0
        self.camera = 0
        self.w, self.h = 50, 50
        self.ySpeed = 0

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
        if self.dir != 0:
            self.running = True
            if self.speed < MAX_SPEED:
                self.speed = self.speed + ACCEL * 0.5
            self.x += self.dir * self.speed
            if self.x < 0:
                self.x = 20
            self.frame = (self.frame + 1) % 40
        if self.jump:
            self.y = self.y + self.ySpeed * self.t + (g * self.t * self.t) / 2
            self.t += 0.1
            #print(self.y)


    def get_bb(self):
        return self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2

    def get_x(self):
        return self.x

    def get_speed(self):
        return self.speed

    def set_camera(self, c):
        self.camera = c

    def check_stand(self, stand, y):
        if stand:
            self.jump = False
            self.y = y + self.h / 2

    def handleEvent(self, e):
        global JUMP_TIME
        if e.type == SDL_KEYDOWN:
            if e.key == SDLK_LEFT:
                self.dir -= 1
            elif e.key == SDLK_RIGHT:
                self.dir += 1
            elif e.key == SDLK_UP:
                if self.jump == False:
                    self.ySpeed = 15
                    self.jump = True
                    self.t = 0
                    self.oldy = self.y
                # JUMP_TIME = time.time()
        elif e.type == SDL_KEYUP:
            if e.key == SDLK_LEFT:
                self.dir += 1
                self.speed = 1
                self.running = False
            elif e.key == SDLK_RIGHT:
                self.speed = 1
                self.dir -= 1
                self.running = False
            elif e.key == SDLK_UP:
                pass
                # JUMP_TIME = time.time() - JUMP_TIME
                # print(JUMP_TIME)
                # self.ySpeed = JUMP_TIME * 30
                # if self.ySpeed > MAX_JUMP:
                    # self.ySpeed = MAX_JUMP
                # self.oldy = self.y
                # self.t = 0
                # self.jump = True


    def draw(self):
        if self.jump:
            if self.dir == 1:
                self.image.clip_draw(250, 339 + 380, 35, 40, self.x - self.camera, self.y, self.w, self.h)
                draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2,
                               self.x + self.w / 2 - self.camera, self.y + self.h / 2)
            else:
                self.image.clip_draw(60, 335, 35, 40, self.x - self.camera, self.y, self.w, self.h)
                draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2,
                               self.x + self.w / 2 - self.camera, self.y + self.h / 2)
        elif self.running:
            if self.dir == 1:
                if (self.frame // 10) < 3:
                    self.image.clip_draw(130 + (self.frame // 10) * 35, 339 + 380, 35, 40, self.x - self.camera, self.y, self.w, self.h)
                    draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2)
                else:
                    self.image.clip_draw(130 + (4 - (self.frame // 10)) * 35, 339 + 380, 35, 40, self.x - self.camera, self.y, self.w, self.h)
                    draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2)
            else:
                if (self.frame // 10) < 3:
                    self.image.clip_draw(185 - (self.frame // 10) * 35, 335, 35, 40, self.x - self.camera, self.y, self.w, self.h)
                    draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2)
                else:
                    self.image.clip_draw(185 - (4 - (self.frame // 10)) * 35, 335, 35, 40, self.x - self.camera, self.y, self.w, self.h)
                    draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2)
        else:
            self.image.clip_draw(2, 339 + 380, 40, 40, self.x - self.camera, self.y, self.w, self.h)
            draw_rectangle(self.x - self.w / 2 - self.camera, self.y - self.h / 2, self.x + self.w / 2 - self.camera, self.y + self.h / 2)

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
