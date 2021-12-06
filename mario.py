from pico2d import *
import game_framework
# import game_world
import time

import game_world
import object
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

RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SPACE_DOWN, GAME_OVER, LANDING, RUNNING, DROP, CLEAR = range(10)

DEFAULT_MARIO, BIG_MARIO, FIRE_MARIO = range(3)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE_DOWN,
}

mario_size = [(35, 40), (45, 75), (45, 75)]
mario_start = [(2, 125, 240, 50), (50, 150, 290, 90), (50, 150, 290, 90)]
mario_wh = [(50, 50), (100, 100), (100, 100)]

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
            Mario.jump_sound.play()
            Mario.jumpv = 25
            Mario.jumping = True
            Mario.jumpTime += game_framework.frame_time
            Mario.y += Mario.jumpv * Mario.jumpTime + (GRAVITY_PPSS * Mario.jumpTime ** 2 / 2)
            Mario.jumpTime = 0.0

    def do(Mario):
        Mario.frame = (Mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

    def draw(Mario):
        if Mario.dir > 0:
            Mario.image[Mario.state].clip_draw(mario_start[Mario.state][0], mario_size[Mario.state][1], mario_size[Mario.state][0], mario_size[Mario.state][1], Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)
        else:
            Mario.image[Mario.state].clip_composite_draw(mario_start[Mario.state][0], mario_size[Mario.state][1], mario_size[Mario.state][0], mario_size[Mario.state][1], 0, 'h', Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)


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
            Mario.jump_sound.play()
            Mario.jumpv = 25
            Mario.jumpTime += game_framework.frame_time
            Mario.y += Mario.jumpv * Mario.jumpTime + (GRAVITY_PPSS * Mario.jumpTime ** 2 / 2)
            Mario.jumpTime = 0.0
        elif event == GAME_OVER:
            Mario.jumpv = 20

    def do(Mario):
        Mario.frame = (Mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        Mario.x += Mario.velocity * game_framework.frame_time

        for coin in server.obstacles.coins.copy():
            if collision.collide(Mario, coin):
                Mario.plus_coin()
                server.obstacles.coins.remove(coin)
                game_world.remove_object(coin)

        for obs in server.obstacles.obstacleBlock:
            if collision.collide(Mario, obs):
                if Mario.y > obs.y:
                    break
                if Mario.dir > 0:
                    Mario.x = clamp(0, Mario.x, obs.x - 50)
                else:
                    Mario.x = clamp(obs.x + 50, Mario.x, 1000)
                break

        for pipe in server.obstacles.pipes:
            if collision.collide(Mario, pipe):
                if Mario.y > pipe.y:
                    break
                print('pipe')
                if Mario.dir > 0:
                    Mario.x = clamp(0, Mario.x, pipe.x - 53)
                else:
                    Mario.x = clamp(pipe.x + 53, Mario.x, 1000)
                break
        for enemy in server.enemies.monster:
            if collision.collide(Mario, enemy):
                Mario.hit()
                if Mario.life <= 0:
                    Mario.add_event(GAME_OVER)

        for ground in server.obstacles.ground:
            if collision.collide(Mario, ground):
                if Mario.y < ground.y + 25:
                    if Mario.dir > 0:
                        Mario.x = clamp(0, Mario.x, ground.x - 50)
                    else:
                        Mario.x = clamp(ground.x + 50, Mario.x, 1000)
                    break

        if Mario.y > 100:
            landing = False
            for ground in server.obstacles.ground + server.obstacles.block2s + server.obstacles.block3s + server.obstacles.randombox + server.obstacles.pipes:
                if collision.collide(Mario, ground):
                    landing = True
            for obs in server.obstacles.obstacleBlock:
                if collision.collide(Mario, obs):
                    if Mario.y > obs.y:
                        landing = True
                        continue
                    else:
                        landing = True
                        if Mario.dir > 0:
                            Mario.x = clamp(0, Mario.x, obs.x - 50)
                        else:
                            Mario.x = clamp(obs.x + 50, Mario.x, 1000)
            if not landing:
                Mario.add_event(DROP)


    def draw(Mario):
        if Mario.dir > 0:
            if int(Mario.frame) < 3:
                Mario.image[Mario.state].clip_draw(mario_start[Mario.state][1]+ int(Mario.frame) * mario_size[Mario.state][0], mario_size[Mario.state][1], mario_size[Mario.state][0], mario_size[Mario.state][1], Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)
            else:
                Mario.image[Mario.state].clip_draw(mario_start[Mario.state][1] + (4 - int(Mario.frame)) * mario_size[Mario.state][0], mario_size[Mario.state][1], mario_size[Mario.state][0], mario_size[Mario.state][1], Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)
        else:
            if int(Mario.frame) < 3:
                Mario.image[Mario.state].clip_composite_draw(mario_start[Mario.state][1] + int(Mario.frame) * mario_size[Mario.state][0], mario_size[Mario.state][1], mario_size[Mario.state][0], mario_size[Mario.state][1], 0, 'h', Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)
            else:
                Mario.image[Mario.state].clip_composite_draw(mario_start[Mario.state][1] + (4 - int(Mario.frame)) * mario_size[Mario.state][0], mario_size[Mario.state][1], mario_size[Mario.state][0], mario_size[Mario.state][1], 0, 'h', Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)


class JumpState:
    def enter(Mario, event):
        if event == RIGHT_DOWN:
            Mario.velocity += RUN_SPEED_PPS
            Mario.dir = clamp(-1, Mario.velocity, 1)
        elif event == LEFT_DOWN:
            Mario.velocity -= RUN_SPEED_PPS
            Mario.dir = clamp(-1, Mario.velocity, 1)
        elif event == RIGHT_UP:
            Mario.velocity -= RUN_SPEED_PPS
            Mario.dir = clamp(-1, Mario.velocity, 1)
        elif event == LEFT_UP:
            Mario.velocity += RUN_SPEED_PPS
            Mario.dir = clamp(-1, Mario.velocity, 1)
        elif event == DROP:
            Mario.jumpTime = 0.0
            Mario.jumpv = 0.0

    def exit(Mario, event):
        Mario.dir = Mario.velocity
        pass

    def do(Mario):
        Mario.jumpTime += game_framework.frame_time
        Mario.x += Mario.velocity * game_framework.frame_time
        Mario.y += Mario.jumpv * Mario.jumpTime + (GRAVITY_PPSS * Mario.jumpTime ** 2 / 2)

        for coin in server.obstacles.coins.copy():
            if collision.collide(Mario, coin):
                Mario.plus_coin()
                server.obstacles.coins.remove(coin)
                game_world.remove_object(coin)

        for obs in server.obstacles.obstacleBlock:
            if collision.collide(Mario, obs):
                if Mario.y >= obs.y + 40:
                    Mario.y = obs.y + 50
                    Mario.jumpTime = 0.0
                    if Mario.velocity ** 2 > 0:
                        Mario.add_event(RUNNING)
                    else:
                        Mario.add_event(LANDING)
                    break
                else:
                    if Mario.dir > 0:
                        Mario.x = clamp(-1, Mario.x, obs.x - 50)
                    else:
                        Mario.x = clamp(obs.x + 50, Mario.x, 1000)

        for ground3 in server.obstacles.block3s:
            if collision.collide(Mario, ground3):
                if Mario.y > ground3.y + 40:
                    Mario.y = ground3.y + 50
                    Mario.jumpTime = 0.0
                    if Mario.velocity ** 2 > 0:
                        Mario.add_event(RUNNING)
                    else:
                        Mario.add_event(LANDING)
                    break
                else:
                    Mario.jumpv *= -1
                    break;

        for pipe in server.obstacles.pipes:
            if collision.collide(Mario, pipe):
                if Mario.y > pipe.y + 80:
                    Mario.y = pipe.y + 95
                    Mario.jumpTime = 0.0
                    if Mario.velocity ** 2 > 0:
                        Mario.add_event(RUNNING)
                    else:
                        Mario.add_event(LANDING)
                    break
                else:
                    if Mario.dir > 0:
                        Mario.x = clamp(-1, Mario.x, pipe.x - 53)
                    else:
                        Mario.x = clamp(pipe.x + 53, Mario.x, 1000)

        # for randomBox in server.obstacles.randombox:
        #     if collision.collide(Mario, randomBox):
        #         if Mario.y > randomBox.y + 40:
        #             Mario.y = randomBox.y + 50
        #             Mario.jumpTime = 0.0
        #             if Mario.velocity ** 2 > 0:
        #                 Mario.add_event(RUNNING)
        #             else:
        #                 Mario.add_event(LANDING)
        #             break
        #         else:
        #             if randomBox.state:
        #                 randomBox.get_item()
        #             Mario.jumpv *= -1
        #             break

        for ground2 in server.obstacles.block2s.copy() + server.obstacles.randombox.copy():
            if collision.collide(Mario, ground2):
                if Mario.y > ground2.y + 40:
                    Mario.y = ground2.y + 50
                    Mario.jumpTime = 0.0
                    if Mario.velocity ** 2 > 0:
                        Mario.add_event(RUNNING)
                    else:
                        Mario.add_event(LANDING)
                    break
                else:
                    if isinstance(ground2, object.RandomBox):
                        ground2.get_item()
                    Mario.jumpv *= -1
                    break

        for ground in server.obstacles.ground:
            if collision.collide(Mario, ground):
                if Mario.y >= ground.y:
                    Mario.y = ground.y + 50
                    Mario.jumpTime = 0.0
                    if Mario.velocity ** 2 > 0:
                        Mario.add_event(RUNNING)
                    else:
                        Mario.add_event(LANDING)
                    break
                else:
                    if Mario.dir > 0:
                        Mario.x = clamp(-1, Mario.x, ground.x - 50)
                    else:
                        Mario.x = clamp(ground.x + 50, Mario.x, 1000)

        for enemy in server.enemies.monster:
            if collision.collide(Mario, enemy):
                if Mario.y > enemy.y + 25:
                    server.enemies.monster.remove(enemy)
                    game_world.remove_object(enemy)
                else:
                    Mario.hit()
                    if Mario.life <= 0:
                        Mario.add_event(GAME_OVER)
        if server.obstacles.plag is not None:
            if collision.collide(Mario, server.obstacles.plag):
                Mario.x = server.obstacles.plag.x
                Mario.add_event(CLEAR)

    def draw(Mario):
        if Mario.dir > 0:
            Mario.image[Mario.state].clip_draw(mario_start[Mario.state][2], mario_size[Mario.state][1], mario_size[Mario.state][0], mario_size[Mario.state][1], Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)
        else:
            Mario.image[Mario.state].clip_composite_draw(mario_start[Mario.state][2], mario_size[Mario.state][1], mario_size[Mario.state][0], mario_size[Mario.state][1], 0, 'h', Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)

class EndState:
    def enter(Mario, event):
        Mario.timer.stop()
        if event == GAME_OVER:
            Mario.bgm.stop()
            Mario.gameover_sound.play()
        if event == CLEAR:
            pass

    def exit(Mario, event):
        pass

    def do(Mario):
        Mario.frame = (Mario.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if Mario.life <= 0:
            Mario.jumpTime += game_framework.frame_time
            Mario.y += Mario.jumpv * Mario.jumpTime + (GRAVITY_PPSS * Mario.jumpTime ** 2 / 2)
        else:
            Mario.y -= RUN_SPEED_PPS * game_framework.frame_time
            if Mario.y <= 150:
                Mario.y = 100
                Mario.x += RUN_SPEED_PPS * game_framework.frame_time
                if Mario.x >= 6800:
                    # game_framework.change_state()
                    Mario.x = 6800

    def draw(Mario):
        if Mario.life <= 0:
            Mario.image[Mario.state].clip_draw(mario_start[Mario.state][3], mario_size[Mario.state][1], mario_size[Mario.state][0], mario_size[Mario.state][1], Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)
        else:
            if Mario.y > 150:
                Mario.image[Mario.state].clip_draw(mario_start[Mario.state][3], 0, mario_size[Mario.state][0], mario_size[Mario.state][1], Mario.x - Mario.camera, Mario.y, Mario.w, Mario.h)
            else:
                if int(Mario.frame) < 3:
                    Mario.image[Mario.state].clip_draw(mario_start[Mario.state][1] + int(Mario.frame) * mario_size[Mario.state][0], mario_size[Mario.state][1], mario_size[Mario.state][0], mario_size[Mario.state][1], Mario.x - Mario.camera,
                                          Mario.y, Mario.w, Mario.h)
                else:
                    Mario.image[Mario.state].clip_draw(mario_start[Mario.state][1] + (4 - int(Mario.frame)) * mario_size[Mario.state][0], mario_size[Mario.state][1], mario_size[Mario.state][0], mario_size[Mario.state][1], Mario.x - Mario.camera,
                                          Mario.y, Mario.w, Mario.h)

next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState,
                GAME_OVER: EndState, SPACE_DOWN: JumpState, LANDING: IdleState, RUNNING: RunState, DROP: JumpState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,
               GAME_OVER: EndState, SPACE_DOWN: JumpState, LANDING: IdleState, RUNNING: RunState, DROP: JumpState},
    EndState: {RIGHT_UP: EndState, LEFT_UP: EndState, LEFT_DOWN: EndState, RIGHT_DOWN: EndState,
               GAME_OVER: EndState, SPACE_DOWN: EndState},
    JumpState: {RIGHT_UP: JumpState, LEFT_UP: JumpState, LEFT_DOWN: JumpState, RIGHT_DOWN: JumpState,
               GAME_OVER: EndState, SPACE_DOWN: JumpState, LANDING: IdleState, RUNNING: RunState, DROP: JumpState, CLEAR: EndState},
}


class Mario:
    def __init__(self, x = 100, y = 100):
        self.x = x
        self.y = y
        self.image = [load_image("./image/default_mario.png"), load_image("./image/big_mario.png"), load_image("./image/fire_mario.png")]
        self.font = load_font('ENCR10B.TTF', 32)
        self.frame = 0
        self.dir = 1
        self.velocity = 0
        self.jumping = True
        self.jumpv = 25
        self.jumpTime = 0.0
        self.space = 0.0
        self.camera = 0

        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.coin = 0
        self.coinImage = load_image('./image/coin.png')
        self.timer = timer.TimerObject(3)
        self.life = 100

        self.jump_sound = load_wav('./music/jump.wav')
        self.jump_sound.set_volume(16)

        self.state = DEFAULT_MARIO
        self.w, self.h = 50, 50

        self.gameover_sound = load_wav('./music/gameover.wav')
        self.gameover_sound.set_volume(32)

        self.bgm = load_music('./music/mariobgm.mp3')
        self.bgm.set_volume(32)
        self.bgm.repeat_play()

    def plus_coin(self):
        self.coin += 1

    def add_event(self, event):
        self.event_que.insert(0, event)

    def hit(self):
        self.life -= 1
        if self.state == FIRE_MARIO:
            self.state = DEFAULT_MARIO

    def update(self):
        self.set_camera()
        self.timer.update()
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)
        if self.y < -200:
            self.event_que.clear()
        if self.y < 100:
            self.y = 100

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
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

    def stop_bgm(self):
        self.bgm.stop()

    def grow(self):
        self.life += 1
        if self.state == DEFAULT_MARIO:
            self.state = BIG_MARIO

    def fire_grow(self):
        self.life += 1
        self.state = FIRE_MARIO

    def draw(self):
        self.cur_state.draw(self)
        # debug_print('Velocity: ' + str(self.velocity) + ' jumping: ' + str(self.jumping))
        # print(self.y)
        draw_rectangle(*self.get_bb())
        self.coinImage.clip_draw(0, 0, 120, 115, 20, get_canvas_height() - 50, 40, 40)
        self.font.draw(45, get_canvas_height() - 50, 'x%d' % self.coin, (255, 255, 255))
        self.timer.draw()