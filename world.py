from pico2d import *
import mario

def handle_events():
    global running
    global stage_index
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_LEFT:
                if stage_index > 1:
                    stage_index -= 1
            elif event.key == SDLK_RIGHT:
                if stage_index < 3:
                    stage_index += 1
open_canvas()

stage_list= []

stage_list.append((100, 600 - 170))
# stage_list.append((210, 600 - 170))
stage_list.append((210, 600 - 60))
stage_list.append((420, 600 - 60))
stage_list.append((530, 600 - 60))

stage_index = 0

mario = mario.Mario(stage_list[stage_index][0], stage_list[stage_index][1])
worldmap = load_image('map.png')

running = True

while running:
    handle_events()
    mario.worldMapMove(stage_list[stage_index][0], stage_list[stage_index][1])
    clear_canvas()
    worldmap.draw(400, 300, 800, 600)
    mario.draw()
    update_canvas()
    delay(0.05)

close_canvas()
