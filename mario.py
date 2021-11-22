from pico2d import *
import game_framework
# import game_world
import time
import timer
import server
import collision

g = -10.0
ACCEL = 0.2
MAX_JUMP = 10
JUMP_TIME = 0

PIXEL_PER_METER = (10.0 / 0.1)
GRAVITY_MPSS = -1.0
GRAVITY_PPSS = GRAVITY_MPSS * PIXEL_PER_METER
RUN_SPEED_KMPH = 15.0 # 20.0 test more
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER) # 약 4.1
MAX_SPEED = RUN_SPEED_PPS

JUMP_SPEED_MPS = 0.1
JUMP_SPEED_PPS = (JUMP_SPEED_MPS * PIXEL_PER_METER)

TIME_PER_ACTION = 0.2
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE_DOWN, SPACE_UP, GAME_OVER = range(7)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN,
    (SDL_KEYUP, SDLK_SPACE): SPACE_UP
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
        if event == SPACE_DOWN:
            Mario.jumping = True
            Mario.jumpTime += game_framework.frame_time
            Mario.y += Mario.jumpv * Mario.jumpTime + (GRAVITY_PPSS * Mario.jumpTime ** 2 / 2)

    def do(Mario):
        Mario.frame = (Mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if Mario.jumping:
            Mario.jumpTime += game_framework.frame_time
            Mario.y += Mario.jumpv * Mario.jumpTime + (GRAVITY_PPSS * Mario.jumpTime ** 2 / 2)

    def draw(Mario):
        if Mario.dir > 0:
            if Mario.jumping:
                Mario.image.clip_draw(250, 339 + 380, 35, 40, Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)
            else:
                Mario.image.clip_draw(2, 339 + 380, 40, 40, Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)
        else:
            if Mario.jumping:
                Mario.image.clip_draw(60, 335, 35, 40, Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)
            else:
                Mario.image.clip_composite_draw(2, 339 + 380, 40, 40, 0, 'h', Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)



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
        if event == SPACE_DOWN:
            Mario.jumping = True
            Mario.jumpTime += game_framework.frame_time
            Mario.y += Mario.jumpv * Mario.jumpTime + (GRAVITY_PPSS * Mario.jumpTime ** 2 / 2)
        elif event == GAME_OVER:
            Mario.jumpv = 20

    def do(Mario):
        Mario.frame = (Mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        Mario.x += Mario.velocity * game_framework.frame_time
        if Mario.jumping:
            Mario.jumpTime += game_framework.frame_time
            Mario.y += Mario.jumpv * Mario.jumpTime + (GRAVITY_PPSS * Mario.jumpTime ** 2 / 2)

    def draw(Mario):
        if Mario.dir > 0:
            if Mario.jumping:
                Mario.image.clip_draw(250, 339 + 380, 35, 40, Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)
            else:
                if int(Mario.frame) < 3:
                    Mario.image.clip_draw(130 + int(Mario.frame) * 35, 339 + 380, 35, 40, Mario.x - Mario.camera, Mario.y,
                                          Mario.w, Mario.h)
                else:
                    Mario.image.clip_draw(130 + (4 - int(Mario.frame)) * 35, 339 + 380, 35, 40, Mario.x - Mario.camera,
                                          Mario.y, Mario.w, Mario.h)
        else:
            if Mario.jumping:
                Mario.image.clip_draw(60, 335, 35, 40, Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)
            else:
                if int(Mario.frame) < 3:
                    Mario.image.clip_draw(185 - int(Mario.frame) * 35, 335, 35, 40, Mario.x - Mario.camera, Mario.y, Mario.w,
                                          Mario.h)
                else:
                    Mario.image.clip_draw(185 - (4 - int(Mario.frame)) * 35, 335, 35, 40, Mario.x - Mario.camera, Mario.y,
                                          Mario.w, Mario.h)


class EndState:
    def enter(Mario, event):
        Mario.timer.stop()
        pass

    def exit(Mario, event):
        pass

    def do(Mario):
        Mario.jumpTime += game_framework.frame_time
        Mario.y += Mario.jumpv * Mario.jumpTime + (GRAVITY_PPSS * Mario.jumpTime ** 2 / 2)

    def draw(Mario):
        Mario.image.clip_draw(50, 339 + 380, 40, 40, Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)


next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                GAME_OVER: EndState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               GAME_OVER: EndState},
    EndState: {RIGHT_UP: EndState, LEFT_UP: EndState, LEFT_DOWN: EndState, RIGHT_DOWN: EndState,
               GAME_OVER: EndState}
}


class Mario:
    def __init__(self, x = 100, y = 100):
        self.x = x
        self.y = y
        self.image = load_image("./image/mario.png")
        self.font = load_font('ENCR10B.TTF', 32)
        self.frame = 0
        self.dir = 1
        self.velocity = 0
        self.jumping = True
        self.jumpv = JUMP_SPEED_PPS
        self.jumpTime = 0.0
        self.space = 0.0
        self.frame = 0
        self.camera = 0
        self.w, self.h = 50, 50
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.coin = 0
        self.coinImage = load_image('./image/coin.png')
        self.timer = timer.TimerObject(5)
        self.life = 1

    def plus_coin(self):
        self.coin += 1

    def add_event(self, event):
        self.event_que.insert(0, event)

    def hit(self):
        self.life -= 1
        if self.life == 0:
            self.add_event(GAME_OVER)

    def update(self):
        self.timer.update()
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        if self.y < -200:
            self.event_que.clear()

        server.cam.set_camera(self.x)


    def get_bb(self):
        if self.dir > 0:
            return self.x - self.camera - 20, self.y - self.h / 2, self.x - self.camera + 20, self.y + self.h / 2
        else:
            return self.x - self.camera - 20, self.y - self.h / 2, self.x - self.camera + 20, self.y + self.h / 2

    def get_x(self):
        return self.x

    def landing(self, y):
        self.jumping = False
        self.jumpTime = 0.0
        self.y = y

    def get_speed(self):
        return self.velocity

    def set_camera(self):
        self.camera = server.cam.get_camera()

    def is_jumping(self):
        return self.jumping

    def handleEvent(self, event):
        global JUMP_SPEED_MPS
        global JUMP_SPEED_PPS
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            if key_event == SPACE_DOWN:
                self.space = time.time()
            elif key_event == SPACE_UP:
                now = time.time()
                self.space = now - self.space
                self.jumping = True
                JUMP_SPEED_MPS = clamp(0.2, self.space, 0.25)
                JUMP_SPEED_PPS = JUMP_SPEED_MPS * PIXEL_PER_METER
                self.jumpv = JUMP_SPEED_PPS
            else:
                self.add_event(key_event)

    def draw(self):
        self.cur_state.draw(self)
        # debug_print('Velocity: ' + str(self.velocity) + ' jumping: ' + str(self.jumping))
        # print(self.y)
        draw_rectangle(*self.get_bb())
        self.coinImage.clip_draw(0, 0, 120, 115, 20, get_canvas_height() - 50, 40, 40)
        self.font.draw(45, get_canvas_height() - 50, 'x%d' % self.coin, (255, 255, 255))
        self.timer.draw()