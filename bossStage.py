from pico2d import *
import bossmap
import mario
import game_framework
import world

char = None
bossMapData = None
camera = 0

def enter():
    global char
    global bossMapData
    char = mario.Mario(10, 150)
    bossMapData = bossmap.BossMap()

def exit():
    global char
    global bossMapData
    del(char)
    del(bossMapData)


def handle_events():
    events = get_events()
    for event in events:
        char.handleEvent(event)
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.change_state(world)
            elif event.key == SDLK_LEFT:
                pass

def update():
    global camera
    char.update()
    bossMapData.update()
    cx = char.get_x()
    cdx = char.get_speed()
    if cx - camera > 400:
        camera += cdx
    if cx - camera < 400 and camera > 0:
        camera -= cdx
    char.set_camera(camera)
    bossMapData.set_camera(camera)
    delay(0.01)

def draw():
    clear_canvas()
    bossMapData.draw()
    char.draw()
    update_canvas()