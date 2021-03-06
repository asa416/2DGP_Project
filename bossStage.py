from pico2d import *
from mario import Mario
import game_framework
import world
import game_world
import bgdata
import enemydata
import obstacledata
from camera import Camera
import server

name = "BossStage"
bg = None

def enter():
    global bg
    bg = load_image('./image/bossbg.png')
    server.stagefont = load_font('ENCR10B.TTF', 24)
    server.char = Mario(50, 350)
    server.BG = bgdata.Stage1BG()
    server.enemies = enemydata.BossStageEnemy()
    server.obstacles = obstacledata.BossObstacle()
    server.cam = Camera()
    game_world.add_objects(server.enemies.monster, 3)
    game_world.add_objects(server.obstacles.ground, 2)
    game_world.add_objects(server.obstacles.fire, 1)
    game_world.add_object(server.obstacles.ax, 3)
    game_world.add_objects(server.obstacles.bridge, 1)
    game_world.add_object(server.char, 4)
    server.char.bossbgm.repeat_play()

def exit():
    global bg
    del(bg)
    game_world.clear()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            server.char.stop_bgm()
            game_framework.change_state(world)
        else:
            server.char.handleEvent(event)

def update():
    for game_object in game_world.all_objects():
        game_object.update()

def draw():
    clear_canvas()
    bg.draw(400, 300, 800, 600)
    for game_object in game_world.all_objects():
        game_object.draw()
    server.stagefont.draw(get_canvas_width() / 2, get_canvas_height() - 30, name, (255, 255, 255))
    update_canvas()