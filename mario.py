from pico2d import *
import game_framework
# import game_world
# import time

PIXEL_PER_METER = (10.0 / 0.1)
RUN_SPEED_KMPH = 100.0 # 10.0 test more
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

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
        if event == RIGHT_DOWN:
            Mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            Mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            Mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            Mario.velocity += RUN_SPEED_PPS

    def exit(Mario, event):
        pass

    def do(Mario):
        Mario.frame = (Mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    def draw(Mario):
        Mario.image.clip_draw(2, 339 + 380, 40, 40, Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)
        draw_rectangle(Mario.x - Mario.w / 2 - Mario.camera, Mario.y - Mario.h / 2, Mario.x + Mario.w / 2 - Mario.camera,
                       Mario.y + Mario.h / 2)


class RunState:
    def enter(Mario, event):
        if event == RIGHT_DOWN:
            Mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            Mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            Mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            Mario.velocity += RUN_SPEED_PPS
        Mario.dir = clamp(-1, Mario.velocity, 1)

    def exit(Mario, event):
        pass

    def do(Mario):
        Mario.frame = (Mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        Mario.x += Mario.velocity * game_framework.frame_time

    def draw(Mario):
        if Mario.dir > 0:
            if int(Mario.frame) < 3:
                Mario.image.clip_draw(130 + int(Mario.frame) * 35, 339 + 380, 35, 40, Mario.x - Mario.camera, Mario.y,
                                     Mario.w, Mario.h)
                draw_rectangle(Mario.x - Mario.w / 2 - Mario.camera, Mario.y - Mario.h / 2,
                               Mario.x + Mario.w / 2 - Mario.camera, Mario.y + Mario.h / 2)
            else:
                Mario.image.clip_draw(130 + (4 - int(Mario.frame)) * 35, 339 + 380, 35, 40, Mario.x - Mario.camera,
                                     Mario.y, Mario.w, Mario.h)
                draw_rectangle(Mario.x - Mario.w / 2 - Mario.camera, Mario.y - Mario.h / 2,
                               Mario.x + Mario.w / 2 - Mario.camera, Mario.y + Mario.h / 2)
        else:
            if int(Mario.frame) < 3:
                Mario.image.clip_draw(185 - int(Mario.frame) * 35, 335, 35, 40, Mario.x - Mario.camera, Mario.y, Mario.w,
                                     Mario.h)
                draw_rectangle(Mario.x - Mario.w / 2 - Mario.camera, Mario.y - Mario.h / 2,
                               Mario.x + Mario.w / 2 - Mario.camera, Mario.y + Mario.h / 2)
            else:
                Mario.image.clip_draw(185 - (4 - int(Mario.frame)) * 35, 335, 35, 40, Mario.x - Mario.camera, Mario.y,
                                     Mario.w, Mario.h)
                draw_rectangle(Mario.x - Mario.w / 2 - Mario.camera, Mario.y - Mario.h / 2,
                               Mario.x + Mario.w / 2 - Mario.camera, Mario.y + Mario.h / 2)


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

next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SPACE: IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, SPACE: RunState}
}


class Mario:
    def __init__(self):
        self.x = 100
        self.y = 100
        self.image = load_image("./image/mario.png")
        self.frame = 0
        self.dir = 1
        self.velocity = 0
        self.fram = 0
        self.camera = 0
        self.w, self.h = 50, 50
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def get_bb(self):
        return self.x - self.w / 2, self.y - self.h / 2, self.x + self.w / 2, self.y + self.h / 2

    def get_x(self):
        return self.x

    def get_speed(self):
        return self.velocity

    def set_camera(self, c):
        self.camera = c

    def handleEvent(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def draw(self):
        self.cur_state.draw(self)