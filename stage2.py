import game_world
from mario import Mario
import game_framework
import world
import bgdata
import enemydata
import obstacledata
from camera import Camera

from pico2d import *

name = "Stage2"
char = None
BG = None
enemies = None
obstacles = None
cam = None
clear = False
stagefont = None
collideDir = None


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    return True


def collide_block(a, b):
    global collideDir
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    if bottom_a < bottom_b: collideDir = 'UP'
    elif top_a > top_b: collideDir = 'DOWN'
    elif left_a < left_b: collideDir = 'LEFT'
    elif right_a > right_b: collideDir = 'RIGHT'

    return True


def collide_monster(a, b):
    global collideDir
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    if bottom_a < bottom_b:
        collideDir = 'UP'
    elif top_a > top_b:
        collideDir = 'DOWN'
    elif left_a < left_b: collideDir = 'LEFT'
    elif right_a > right_b: collideDir = 'RIGHT'

    return True


def enter():
    global char
    global BG
    global cam
    global enemies
    global obstacles
    global stagefont
    stagefont = load_font('ENCR10B.TTF', 24)
    char = Mario()
    BG = bgdata.Stage2BG()
    enemies = enemydata.Stage2Enemy()
    obstacles = obstacledata.Stage2Obstacle()
    cam = Camera()
    game_world.add_object(char, 4)
    game_world.add_objects(enemies.monster, 3)
    game_world.add_objects(obstacles.ground, 1)
    game_world.add_objects(obstacles.block2s, 1)
    game_world.add_objects(obstacles.block3s, 1)
    # game_world.add_objects(obstacles.obstacleBlock, 1)
    game_world.add_objects(obstacles.pipes, 1)
    game_world.add_objects(obstacles.coins, 1)
    game_world.add_objects(obstacles.randombox, 1)
    game_world.add_object(obstacles.plag, 1)
    game_world.add_object(BG, 0)


def exit():
    global cam
    del(cam)
    game_world.clear()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(world)
        else:
            char.handleEvent(event)


def update():
    global cam
    for game_object in game_world.all_objects():
        game_object.update()
    mx = char.get_x()
    cam.update(mx)
    cx = cam.get_camera()
    for game_object in game_world.all_objects():
        game_object.set_camera(cx)
    for enemy in game_world.all_objects_layer(3):
        if collide_monster(char, enemy):
            if collideDir == 'DOWN' or collideDir == 'UP':
                enemies.monster.remove(enemy)
                game_world.remove_object(enemy)
            else:
                char.hit()
    # for obs in obstacles.obstacleBlock:
    #     if collide_block(char, obs):
    #         if collideDir == 'UP':
    #             char.jumpv *= -1
    #         elif collideDir == 'DOWN':
    #             char.landing(obs.y + 50)
    #             char.jumping = True
    #             char.jumpv = 0.0
    #         elif collideDir == 'LEFT':
    #             char.x = clamp(-1, char.x, obs.x - obs.w)
    #         else:
    #             char.x = clamp(obs.x + obs.w, char.x, get_canvas_width())
    for obs in obstacles.block3s:
        if collide_block(char, obs):
            if collideDir == 'UP':
                char.jumpv *= -1
            elif collideDir == 'DOWN':
                char.landing(obs.y + 50)
                char.jumping = True
                char.jumpv = 0.0
            elif collideDir == 'LEFT':
                char.x = clamp(-1, char.x, obs.x - obs.w)
            else:
                char.x = clamp(obs.x + obs.w, char.x, get_canvas_width())
    for obs in obstacles.block2s:
        if collide_block(char, obs):
            if collideDir == 'UP':
                char.jumpv *= -1
            elif collideDir == 'DOWN':
                char.landing(obs.y + 50)
                char.jumping = True
                char.jumpv = 0.0
            elif collideDir == 'LEFT':
                char.x = clamp(-1, char.x, obs.x - obs.w)
            else:
                char.x = clamp(obs.x + obs.w, char.x, get_canvas_width())
    for obs in obstacles.randombox:
        if collide_block(char, obs):
            if collideDir == 'UP':
                char.jumpv *= -1
            elif collideDir == 'DOWN':
                char.landing(obs.y + 50)
                char.jumping = True
                char.jumpv = 0.0
            elif collideDir == 'LEFT':
                char.x = clamp(-1, char.x, obs.x - obs.w)
            else:
                char.x = clamp(obs.x + obs.w, char.x, get_canvas_width())
    for pipe in obstacles.pipes:
        if collide_block(char, pipe):
            if collideDir == 'DOWN':
                char.landing(obs.y + 40)
                char.jumping = True
                char.jumpv = 0.0
            elif collideDir == 'LEFT':
                char.x = clamp(-1, char.x, pipe.x - pipe.w)
            else:
                char.x = clamp(pipe.x + pipe.w, char.x, get_canvas_width())
    for coin in obstacles.coins:
        if collide(char, coin):
            char.plus_coin()
            obstacles.coins.remove(coin)
            game_world.remove_object(coin)
    for gb in game_world.all_objects_layer(1):
        if collide_block(char, gb):
            char.landing(100)
    # delay(0.01)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    stagefont.draw(get_canvas_width() / 2, get_canvas_height() - 30, name, (255, 255, 255))
    update_canvas()



# open_canvas()
# background = load_image('sky.png')
# pipe = object.Pipe(400, 70)
# back = back.Back()
# mario = mario.Mario(400, 80)
# boss = enemy.Boss()
# turtle = enemy.Turtle(500, 85)
# goom = enemy.Goom(300, 75)
# block_list1 = []
# for i in range(31):
#     block_list1.append((i * 30, 15))
# blocks1 = [object.Block(block_list1[i][0], block_list1[i][1]) for i in range(31)]
# block_list2 = []
# for i in range(31):
#     block_list2.append((i * 30, 45))
# blocks2 = [object.Block(block_list2[i][0], block_list2[i][1]) for i in range(31)]
#
#
# running = True
#
# while running:
#     handle_events()
#     turtle.update()
#     goom.update()
#     back.update()
#     mario.update()
#     x = mario.get_x()
#     boss.update(x)
#
#     clear_canvas()
#     background.draw(400, 300, 800, 600)
#     back.draw()
#     i = 0
#     for block in blocks1:
#         block.draw()
#         i += 1
#     i = 0
#     for block in blocks2:
#         block.draw()
#         i += 1
#     pipe.draw()
#     mario.draw()
#     boss.draw()
#     turtle.draw()
#     goom.draw()
#     update_canvas()
#
#     delay(0.01)
#
# close_canvas()