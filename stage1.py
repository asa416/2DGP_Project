import mario
import enemy
import object

from pico2d import *

def handle_events():
    global running
    events = get_events()
    for event in events:
        mario.handleEvent(event)
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_LEFT:
                pass

open_canvas()

mario = mario.Mario(400, 80)
# turtle = enemy.Turtle(500, 100)
# goom = enemy.Goom(300, 100)
blocks1 = [object.Block() for i in range(31)]
block_list1 = []
for i in range(31):
    block_list1.append((i * 30, 15))
blocks2 = [object.Block() for i in range(31)]
block_list2 = []
for i in range(31):
    block_list2.append((i * 30, 45))

running = True

while running:
    handle_events()
    # turtle.update()
    # goom.update()
    mario.update()
    clear_canvas()
    i = 0
    for block in blocks1:
        block.draw(block_list1[i][0], block_list1[i][1])
        i += 1
    i = 0
    for block in blocks2:
        block.draw(block_list2[i][0], block_list2[i][1])
        i += 1
    mario.draw()
    # turtle.draw()
    # goom.draw()
    update_canvas()

    delay(0.01)

close_canvas()