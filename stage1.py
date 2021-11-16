import game_world
from mario import Mario
import game_framework
import world
import bgdata
import enemydata
import obstacledata
from camera import Camera

from pico2d import *

name = "Stage1"
char = None
BG = None
enemies = None
obstacles = None
cam = None
clear = False
stagefont = None

collideDir = None


def collide_block(a, b):
    global collideDir
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False

    if left_a < left_b: collideDir = 'LEFT'
    elif right_a > right_b: collideDir = 'RIGHT'
    elif bottom_a < bottom_b: collideDir = 'UP'
    elif top_a > top_b: collideDir = 'DOWN'

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
    BG = bgdata.Stage1BG()
    enemies = enemydata.Stage1Enemy()
    obstacles = obstacledata.Stage1Obstacle()
    cam = Camera()
    game_world.add_object(char, 4)
    game_world.add_objects(enemies.monster, 3)
    game_world.add_objects(obstacles.ground, 1)
    game_world.add_objects(obstacles.block2s, 2)
    game_world.add_objects(obstacles.block3s, 2)
    game_world.add_objects(obstacles.obstacleBlock, 2)
    game_world.add_objects(obstacles.pipes, 2)
    game_world.add_objects(obstacles.coins, 2)
    game_world.add_objects(obstacles.randombox, 2)
    game_world.add_object(obstacles.plag, 2)
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
    for obs in game_world.all_objects_layer(2):
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
    for gb in game_world.all_objects_layer(1):
        if collide_block(char, gb):
            char.landing(100)
    # delay(0.01)

def draw():
    global font
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    stagefont.draw(get_canvas_width() / 2, get_canvas_height() - 30, name, (255, 255, 255))
    update_canvas()
