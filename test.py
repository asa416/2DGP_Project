from pico2d import *


def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

running = True

open_canvas(800, 600)

mario = load_image('mario.png')
frame = 0

while running:
    clear_canvas()

   # if frame == 0:
   #     mario.clip_draw(160, 340, 40, 40, 400, 300)
   # elif frame == 1 || frame == 3:
   #     mario.clip_draw(200, 340, )
    mario.clip_draw(120 + 40 * frame, 339, 40, 40, 400, 300)
    frame = (frame + 1) % 4


    update_canvas()

    handle_events()

    delay(0.05)