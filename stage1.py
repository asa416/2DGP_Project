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
    game_world.add_object(char, 3)
    game_world.add_objects(enemies.gooms, 2)
    game_world.add_objects(enemies.turtles, 2)
    game_world.add_objects(obstacles.ground, 1)
    game_world.add_objects(obstacles.block2s, 1)
    game_world.add_objects(obstacles.block3s, 1)
    game_world.add_objects(obstacles.obstacleBlock, 1)
    game_world.add_objects(obstacles.pipes, 1)
    game_world.add_objects(obstacles.coins, 1)
    game_world.add_objects(obstacles.randombox, 1)
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
    cx = cam.get_camera()
    if mx > 400:
        cx = mx - 400
    cam.set_camera(cx)
    for game_object in game_world.all_objects():
        game_object.set_camera(cx)
    print(cx)
    delay(0.01)

def draw():
    global font
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    stagefont.draw(get_canvas_width() / 2, get_canvas_height() - 30, name, (255, 255, 255))
    update_canvas()
