from pico2d import *
import game_framework

import world

name = "over"
image = None


def enter():
    global image
    image = load_image('./image/game_over.png')


def exit():
    global image
    del(image)


def update():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            game_framework.change_state(world)


def draw():
    clear_canvas()
    image.draw(400, 300, 800, 600)
    update_canvas()