from pico2d import *

class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.image = load_image('mario.png')
        self.frame = 0
        self.running = False

    def update(self):
        self.frame = (self.frame + 1) % 4

    def worldMapMove(self, x, y):
        self.x = x
        self.y = y

    def draw(self):
        if self.running:
            if self.frame < 3:
                self.image.clip_draw(160 + self.frame * 40, 339, 40, 40, self.x, self.y, 50, 50)
            else:
                self.image.clip_draw(160 + (4 - self.frame) * 40, 339, 40, 40, self.x, self.y, 50, 50)
        else:
            self.image.clip_draw(2, 339, 40, 40, self.x, self.y, 50, 50)

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


running = True

if __name__ == '__main__':


    open_canvas()
    mario = Mario()

    while running:
        handle_events()
        mario.update()

        clear_canvas()
        mario.draw()
        update_canvas()
        delay(1)

    close_canvas()
