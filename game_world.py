
# layer 0: Background Objects
# layer 1: Ground Objects
# layer 2: Obstacle Objects
# layer 3: Enemy Objects
# layer 4: Player Objects
objects = [[], [], [], [], []]


def add_object(o, layer):
    objects[layer].append(o)


def add_objects(l, layer):
    objects[layer] += l


def remove_object(o):
    for i in range(len(objects)):
        if o in objects[i]:
            objects[i].remove(o)
            del o
            break


def clear():
    for o in all_objects():
        del o
    for l in objects:
        l.clear()


def destroy():
    clear()
    objects.clear()


def all_objects():
    for i in range(len(objects)):
        for o in objects[i]:
            yield o


def all_objects_layer(layer):
    for o in objects[layer]:
        yield o