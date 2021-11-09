from pico2d import *
import game_framework
import stage1
import stage2
import stage3
import bossStage

name = "WolrdMap"
image = None
mario = None
stage_list = []
stage_index = 0

def enter():
    global image
    global mario
    global stage_list
    global stage_index
    mario = load_image('./image/mario.png')
    image = load_image('./image/map.png')
    stage_index = 0
    stage_list.append((100, 600 - 170))
    stage_list.append((210, 600 - 60))
    stage_list.append((420, 600 - 60))
    stage_list.append((530, 600 - 60))

def exit():
    global image
    global mario
    del(image)
    del(mario)

def handle_events():
    # global running
    global stage_index
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            elif event.key == SDLK_LEFT:
                if stage_index > 1:
                    stage_index -= 1
            elif event.key == SDLK_RIGHT:
                if stage_index < 3:
                    stage_index += 1
            elif event.key == SDLK_SPACE:
                if stage_index == 1:
                    game_framework.change_state(stage1)
                elif stage_index == 2:
                    game_framework.change_state(stage2)
                elif stage_index == 3:
                    game_framework.change_state(stage3)
                else:
                    game_framework.change_state(bossStage)
def update():
    delay(0.01)

def draw():
    clear_canvas()
    image.draw(400, 300, 800, 600)
    mario.clip_draw(2, 339 + 380, 40, 40, stage_list[stage_index][0], stage_list[stage_index][1], 50, 50)
    update_canvas()

