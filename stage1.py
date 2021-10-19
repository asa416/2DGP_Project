import mario
import enemy
import object

from pico2d import *

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN:
            if event.key == SDLK_ESCAPE:
                running = False
            elif event.key == SDLK_LEFT:
                pass

open_canvas()

mario = mario.Mario(400, 100)
turtle = enemy.Turtle(500, 100)
goom = enemy.Goom(300, 100)
blocks = [object.Block() for i in range(21)]
block_list = []
for i in range(21):
    block_list.append((i * 30, 15))


running = True

while running:
    handle_events()
    turtle.update()
    goom.update()
    clear_canvas()
    i = 0
    for block in blocks:
        block.draw(block_list[i][0], block_list[i][1])
        i += 1
    mario.draw()
    turtle.draw()
    goom.draw()
    update_canvas()

    delay(0.01)

close_canvas()