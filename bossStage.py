from pico2d import *
from mario import Mario
import game_framework
import world
import game_world
import obstacledata
from camera import Camera

name = "BossStage"
char = None
cam = None
obstacles = None
stagefont = None

def enter():
    global char
    global cam
    global obstacles
    global stagefont
    stagefont = load_font('ENCR10B.TTF', 24)
    cam = Camera()
    char = Mario(50, 350)
    obstacles = obstacledata.BossObstacle()
    game_world.add_objects(obstacles.ground, 1)
    game_world.add_object(char, 3)

def exit():
    global cam
    del(cam)
    game_world.clear()

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(world)
        else:
            char.handleEvent(event)

def update():
    global cam
    for game_object in game_world.all_objects():
        game_object.update()
    mx = char.get_x()
    cx = cam.get_camera()
    if mx > 400:
        cx = mx - 400
    cam.set_camera(cx)
    for game_object in game_world.all_objects():
        game_object.set_camera(cx)
    print(cx)
    delay(0.01)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    stagefont.draw(get_canvas_width() / 2, get_canvas_height() - 30, name, (255, 255, 255))
    update_canvas()