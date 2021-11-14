import game_world
from mario import Mario
import game_framework
import world
import bgdata
import enemydata
import obstacledata
from camera import Camera

from pico2d import *

name = "Stage2"
char = None
BG = None
enemies = None
obstacles = None
cam = None
clear = False


def enter():
    global char
    global BG
    global cam
    global enemies
    global obstacles
    char = Mario()
    BG = bgdata.Stage2BG()
    enemies = enemydata.Stage2Enemy()
    obstacles = obstacledata.Stage2Obstacle()
    cam = Camera()
    game_world.add_object(char, 3)
    game_world.add_objects(enemies.gooms, 2)
    game_world.add_objects(enemies.turtles, 2)
    game_world.add_objects(obstacles.ground, 1)
    game_world.add_objects(obstacles.block2s, 1)
    game_world.add_objects(obstacles.block3s, 1)
    # game_world.add_objects(obstacles.obstacleBlock, 1)
    game_world.add_objects(obstacles.pipes, 1)
    game_world.add_objects(obstacles.coins, 1)
    game_world.add_objects(obstacles.randombox, 1)
    game_world.add_object(obstacles.plag, 1)
    game_world.add_object(BG, 0)


def exit():
    global cam
    del (cam)
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
    # delay(0.01)

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
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