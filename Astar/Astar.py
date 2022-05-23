import pygame

import random
import numpy as np

pygame.init()

done = False
x = 0
y = 0
ev = 'r'
fl = 0
clock = pygame.time.Clock()
color = (0, 128, 255)
sp = {0: (x, y)}
size = 1
points = 0
snake_moves = 0

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
DISPLAY_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CELL_SIZE = 64
assert WINDOW_WIDTH % CELL_SIZE == 0;assert WINDOW_HEIGHT % CELL_SIZE == 0
WINDOW_CELL_ROW = int(WINDOW_WIDTH/CELL_SIZE)
WINDOW_CELL_COLUMN = int(WINDOW_HEIGHT/CELL_SIZE)


#Color
WHITE = (255, 255, 255)
BLUE = (84, 194, 205)
DARKBLUE = (93, 216, 228)
GREEN = (0,255,0)
DARKGREEN = (0,100,0)
RED = (220,20,60)
MAROON = (128,0,0)
BLACK = (0,0,0)
GRAY = (128,128,128)

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def return_path(current_node):
    path = []
    current = current_node
    while current is not None:
        path.append(current.position)
        current = current.parent
    return path[::-1] 

def draw_grid():
    for x in range(0,WINDOW_CELL_ROW):
            for y in range(0,WINDOW_CELL_COLUMN):
                if(x + y) % 2 == 0:
                    even = pygame.Rect((y*CELL_SIZE, x*CELL_SIZE), (CELL_SIZE,CELL_SIZE))
                    pygame.draw.rect(DISPLAY_WINDOW, DARKBLUE, even)
                else:
                    odd = pygame.Rect((y*CELL_SIZE, x*CELL_SIZE), (CELL_SIZE,CELL_SIZE))
                    pygame.draw.rect(DISPLAY_WINDOW, BLUE, odd)
    draw_score()

def astar(maze, start, end):
    star = start
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0
    open_list = []
    closed_list = []
    open_list.append(start_node)
    cou = 0
    outer_iterations = 0
    max_iterations = (len(maze) // 2) ** 2

    adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0),)
    while len(open_list) > 0:
        pygame.event.get()
        cou += 1
        r1 = random.randrange(255)
        g1 = random.randrange(255)
        b1 = random.randrange(255)
        if (cou > 500):
            return -1

        outer_iterations += 1
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        open_list.pop(current_index)
        closed_list.append(current_node)

        if current_node == end_node:
            return return_path(current_node)
        children = []

        for new_position in adjacent_squares: 

            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            a1, b1 = node_position
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (
                    len(maze[len(maze) - 1]) - 1) or node_position[1] < 0:
                continue

            if maze[node_position[0]][node_position[1]] != 0:
                continue

            new_node = Node(current_node, node_position)
            children.append(new_node)
        for child in children:
            if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                continue
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + (
                    (child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h
            if len([open_node for open_node in open_list if child == open_node and child.g > open_node.g]) > 0:
                continue
            open_list.append(child)


pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 15)


def drawbox(x, y, hx, hy):
    pygame.draw.rect(DISPLAY_WINDOW, GREEN, pygame.Rect(x, y, 64, 64))
    pygame.draw.rect(DISPLAY_WINDOW, DARKGREEN, pygame.Rect(x, y, 64, 64),5)
    pygame.draw.rect(DISPLAY_WINDOW, BLACK, pygame.Rect(hx, hy, 64, 64))
    pygame.draw.rect(DISPLAY_WINDOW, GRAY, pygame.Rect(hx, hy, 64, 64),5)


def randomSnack():
    rx1 = random.randrange((WINDOW_HEIGHT - CELL_SIZE) / CELL_SIZE)
    ry1 = random.randrange((WINDOW_WIDTH - CELL_SIZE) / CELL_SIZE)
    rx2, ry2 = rx1 * CELL_SIZE, ry1 * CELL_SIZE
    for i in range(0, size):
        a, b = sp[i]
        if a == rx2 and b == ry2:
            return randomSnack()

    return rx1 * CELL_SIZE, ry1 * CELL_SIZE


rx, ry = randomSnack()

def genMatrix(sp):
    mat = np.zeros(shape=(2 + WINDOW_HEIGHT // CELL_SIZE, 2 + WINDOW_WIDTH // CELL_SIZE))
    for i in range(0, 2 + WINDOW_HEIGHT // CELL_SIZE):
        mat[0, i] = 1
        mat[i, 0] = 1
        mat[1 + WINDOW_HEIGHT // CELL_SIZE, i] = 1
        mat[i, 1 + WINDOW_HEIGHT // CELL_SIZE] = 1

    for i in sp:
        a, b = sp[i]
        mat[1 + a // CELL_SIZE, 1 + b // CELL_SIZE] = 1
    a, b = sp[0]
    mat[1 + a // CELL_SIZE, 1 + b // CELL_SIZE] = 0
    start = (1 + a // CELL_SIZE, 1 + b // CELL_SIZE)
    end = (1 + rx // CELL_SIZE, 1 + ry // CELL_SIZE)
    path = astar(mat, start, end)
    return path

def draw_score():
    global snake_moves
    if points==0:
        snake_moves = 0
    pygame.init()
    pygame.display.set_caption("A* Snake Game")
    FONT_STYLE = pygame.font.Font("./assets/arial.ttf", 20)
    if snake_moves==0:
            s = FONT_STYLE.render("Score: "+str(points) +"  Moves: "+str(snake_moves),True, WHITE)
    else:
            s = FONT_STYLE.render("Score: "+str(points) +"  Moves: "+str(snake_moves),True, WHITE)
    s.get_rect().topleft = (WINDOW_WIDTH - int(WINDOW_WIDTH/5), 10)
    snake_moves = snake_moves + 1
    DISPLAY_WINDOW.blit(s,s.get_rect())

draw_grid()
con = 0
while not done:
    fl = 0
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                r1 = random.randrange(255)
                g1 = random.randrange(255)
                b1 = random.randrange(255)
                color = (r1, g1, b1)
            pressed = pygame.key.get_pressed()

    path = genMatrix(sp)
    if path == -1:
        rx, ry = randomSnack()
        path = genMatrix(sp)
        con += 1
        if con > 10:
            size = 1
            points = 0
            x, y = 0, 0
            sp = {}
            sp[0] = (x, y)

            ev = 'r'

        continue
    con = 0
    if path is None:
        size = 1
        points = 0
        x, y = 0, 0
        sp = {0: (x, y)}
        continue
    for j in path:
        fl = 0
        draw_grid()
        pygame.draw.rect(DISPLAY_WINDOW, RED, pygame.Rect(rx, ry, 64, 64))
        pygame.draw.rect(DISPLAY_WINDOW, MAROON, pygame.Rect(rx, ry, 64, 64),5)
        pygame.display.flip()
        nx, ny = sp[0]
        nx1, ny1 = j
        sp[0] = ((nx1 - 1) * CELL_SIZE, (ny1 - 1) * CELL_SIZE)
        nx1, ny1 = ((nx1 - 1) * CELL_SIZE, (ny1 - 1) * CELL_SIZE)
        sp[1] = (nx, ny)
        headx, heady = sp[0]
        for i in range(size - 1, 0, -1):
            headx, heady = sp[0]
            nx, ny = sp[i]
            drawbox(nx, ny, headx, heady)
            tx, ty = sp[i - 1]
            sp[i] = (tx, ty)
        drawbox(nx1, ny1, headx, heady)
        pygame.display.flip()
        clock.tick(10)
        x, y = sp[0]
        if x == rx and y == ry:
            sp[size] = (rx + 1, ry + 1)
            rx, ry = randomSnack()
            if size < 5000:
                size += 1
            points += 1