import game_world
from mario import Mario
import game_framework
import world
import bgdata
import enemydata
import obstacledata
from camera import Camera

from pico2d import *
import server

name = "Stage2"


def enter():
    server.stagefont = load_font('ENCR10B.TTF', 24)
    server.char = Mario()
    server.BG = bgdata.Stage2BG()
    server.enemies = enemydata.Stage2Enemy()
    server.obstacles = obstacledata.Stage2Obstacle()
    server.cam = Camera()
    game_world.add_object(server.char, 4)
    game_world.add_objects(server.enemies.monster, 3)
    game_world.add_objects(server.obstacles.ground, 2)
    game_world.add_objects(server.obstacles.block2s, 2)
    game_world.add_objects(server.obstacles.block3s, 2)
    game_world.add_objects(server.obstacles.obstacleBlock, 1)
    game_world.add_objects(server.obstacles.pipes, 2)
    game_world.add_objects(server.obstacles.coins, 2)
    game_world.add_objects(server.obstacles.randombox, 2)
    game_world.add_object(server.obstacles.plag, 2)
    game_world.add_object(server.BG, 0)
    game_world.add_object(server.cam, 0)


def exit():
    game_world.clear()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(world)
        else:
            server.char.handleEvent(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()

def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    server.stagefont.draw(get_canvas_width() / 2, get_canvas_height() - 30, name, (255, 255, 255))
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