import game_world
from mario import Mario
import game_framework
import world
import bgdata
import enemydata
import obstacledata
from camera import Camera

from pico2d import *
import server


name = "Stage1"

def enter():
    global music_bgm
    server.stagefont = load_font('ENCR10B.TTF', 24)
    server.char = Mario()
    server.BG = bgdata.Stage1BG()
    server.enemies = enemydata.Stage1Enemy()
    server.obstacles = obstacledata.Stage1Obstacle()
    server.cam = Camera()
    game_world.add_object(server.char, 4)
    game_world.add_objects(server.enemies.monster, 3)
    game_world.add_objects(server.obstacles.ground, 2)
    game_world.add_objects(server.obstacles.block2s, 2)
    game_world.add_objects(server.obstacles.block3s, 2)
    game_world.add_objects(server.obstacles.obstacleBlock, 1)
    game_world.add_objects(server.obstacles.pipes, 2)
    game_world.add_objects(server.obstacles.coins, 2)
    game_world.add_objects(server.obstacles.randombox, 2)
    game_world.add_object(server.obstacles.plag, 2)
    game_world.add_object(server.BG, 0)
    game_world.add_object(server.cam, 0)



def exit():
    game_world.clear()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(world)
        else:
            server.char.handleEvent(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()

    # delay(0.01)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    server.stagefont.draw(get_canvas_width() / 2, get_canvas_height() - 30, name, (255, 255, 255))
    update_canvas()
