import mario
import game_framework
import world
import Map1

from pico2d import *

name = "Stage1"
char = None
mapdata = None
camera = 0
clear = False

def enter():
    global char
    global mapdata
    char = mario.Mario(100, 100)
    mapdata = Map1.Map1()

def exit():
    global char
    global mapdata
    global camera
    del(char)
    del(mapdata)
    camera = 0

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

def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb, bb, rb, tb = b.get_bb()

    if la > rb: return False
    if ra < lb: return False
    if ta < ba: return False
    if ba > tb: return False

    return True


def stand(a, y):
    la, ba, ra, ta = a.get_bb()

    if ba < y: return True
    return False

def update():
    global camera
    mapdata.update()
    char.update()
    # char.check_stand(stand(char, 90), 91)
    cx = char.get_x()
    cdx = char.get_speed()
    if cx - camera > 400:
        camera += cdx
    if cx - camera < 400 and camera > 0:
        camera -= cdx
    char.set_camera(camera)
    mapdata.set_camera(camera)
    for gb in mapdata.get_ground():
        if collide(char, gb):
            print('gb')
    delay(0.01)

def draw():
    clear_canvas()
    mapdata.draw()
    char.draw()
    update_canvas()



# open_canvas()
# background = load_image('sky.png')
# pipe = object.Pipe(400, 70)
# back = back.Back()
# mario = mario.Mario(400, 80)
# boss = enemy.Boss()
# turtle = enemy.Turtle(500, 85)
# goom = enemy.Goom(300, 75)
# block_list1 = []
# for i in range(31):
#     block_list1.append((i * 30, 15))
# blocks1 = [object.Block(block_list1[i][0], block_list1[i][1]) for i in range(31)]
# block_list2 = []
# for i in range(31):
#     block_list2.append((i * 30, 45))
# blocks2 = [object.Block(block_list2[i][0], block_list2[i][1]) for i in range(31)]
#
#
# running = True
#
# while running:
#     handle_events()
#     turtle.update()
#     goom.update()
#     back.update()
#     mario.update()
#     x = mario.get_x()
#     boss.update(x)
#
#     clear_canvas()
#     background.draw(400, 300, 800, 600)
#     back.draw()
#     i = 0
#     for block in blocks1:
#         block.draw()
#         i += 1
#     i = 0
#     for block in blocks2:
#         block.draw()
#         i += 1
#     pipe.draw()
#     mario.draw()
#     boss.draw()
#     turtle.draw()
#     goom.draw()
#     update_canvas()
#
#     delay(0.01)
#
# close_canvas()