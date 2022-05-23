import argparse
import random
import sys
import numpy

import sdl2
import sdl2.ext as lib
import sdl2.sdlgfx as gfx

import tensorflow as tf

import numpy as np

from snake import Snake
from ACN import ACN
from TensorAgent import TensorAgent

parser = argparse.ArgumentParser(description='Simulate a snake match using an agent')
parser.add_argument('--x', type=int, default=4, metavar='X',
                help='number of tiles in horizontal direction (default: 4)')
parser.add_argument('--y', type=int, default=4, metavar='Y',
                help='number of tiles in vertical direction (default: 4)')
parser.add_argument('--visibility-range', type=int, default=4, metavar='VR',
                help='visibility range in each direction for the snake (default: 4)')
parser.add_argument('--seed', type=int, default=42, metavar='N',
                    help='random seed (default: 42)')
parser.add_argument('--neurons', type=int, default=512, metavar='NE',
                    help='how many neurons in each layer (default: 512)')
parser.add_argument('--model-path', type=str, default='./model.pt', metavar='MP',
                    help='path to trained model (default: ./model.pt)')
parser.add_argument('--sleep', type=int, default=100, metavar='MP',
                    help='how long to sleep between frames/steps')
parser.add_argument('--autoplay', dest='autoplay', action='store_const',
                    const=True, default=False,
                    help='automatically play in an endless loop')
args = parser.parse_args()

np.random.seed(args.seed)
tf.random.set_seed(args.seed)
random.seed(args.seed)

n_grid_x = args.x
n_grid_y = args.y
window_width = 640 + 1
grid_cell_size = int(640/n_grid_x)
window_height = n_grid_y*grid_cell_size + 1

COLOR_SNAKE_BORDER = sdl2.ext.Color(0,100,0)
COLOR_SNAKE = sdl2.ext.Color(0,255,0)
COLOR_SNAKE_HEAD_BORDER = sdl2.ext.Color(128,128,128)
COLOR_SNAKE_HEAD = sdl2.ext.Color(0, 0, 0)
COLOR_FOOD = sdl2.ext.Color(220,20,60)
COLOR_FOOD_BORDER = sdl2.ext.Color(128,0,0)

#Color
BLUE = (84, 194, 205)
DARKBLUE = (93, 216, 228)

MAX_MOVES = 500

cl_list = []
for i in range(n_grid_x):
    for j in range(n_grid_y):
        data = (i, j)
        cl_list.append(data)

#Draw Board Grid
def draw_grid(renderer):
    for x in cl_list:
        if((x[0] % 2 == 0)):
            if((x[1] % 2 == 0)):
                fill_tile_border(renderer, x[0], x[1], DARKBLUE)
            else:
                fill_tile_border(renderer, x[0], x[1], BLUE)
        else:
            if((x[1] % 2 != 0)):
                fill_tile_border(renderer, x[0], x[1], DARKBLUE)
            else:
                fill_tile_border(renderer, x[0], x[1], BLUE)

def fill_tile_border(renderer, x, y, color):
    renderer.fill(((x*grid_cell_size+1, y*grid_cell_size+1, grid_cell_size-1, grid_cell_size-1)), color)

def fill_tile(renderer, x, y, color):
    renderer.fill(((x*grid_cell_size+1 + int(grid_cell_size * 0.1), y*grid_cell_size+1 + int(grid_cell_size * 0.1), grid_cell_size-1 - 2*int(grid_cell_size * 0.1), grid_cell_size-1 - 2*int(grid_cell_size * 0.1))), color)

def run():
    lib.init()
    window = lib.Window('Actor Critic Snake Game', size=(window_width, window_height))
    window.show()

    renderer = lib.Renderer(window)
    fontManager = sdl2.ext.FontManager(font_path = "./assets/arial.ttf", size = 20)
    factory = sdl2.ext.SpriteFactory(renderer=renderer)
    text = factory.from_text("Current score: ",fontmanager=fontManager)

    snake = Snake(n_grid_x, n_grid_y)
    snake.set_visibility_range(args.visibility_range)
    snake.reset()

    network = ACN(4, fc1_dims=args.neurons, fc2_dims=args.neurons)
    agent = TensorAgent(network)
    agent.load_weights(args.model_path)

    autoplay = args.autoplay
    moves = 0
    running = True
    game_over = False
    old_score = 0
    current_tiles = snake.get_tiles()
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break
            if event.type == sdl2.SDL_KEYDOWN:
                if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                    running = False
                    break
                if event.key.keysym.sym == 112:
                    autoplay = not autoplay
                if event.key.keysym.sym == 114:
                    snake.reset()
                    moves = 0
                    old_score = 0
                    game_over = False
                    current_tiles = snake.get_tiles()
                    break
                if not game_over:
                    if not autoplay:
                        if event.key.keysym.sym == sdl2.SDLK_SPACE:
                            action = agent.get_action(snake.get_view_obs())
                            _, game_over, _ = snake.step(action)
                            current_tiles = snake.get_tiles()
                            moves += 1

        if autoplay:
            action = agent.get_action(snake.get_view_obs())
            _, game_over, _ = snake.step(action)
            current_tiles = snake.get_tiles()
            moves += 1

        renderer.clear(sdl2.ext.Color(0, 0, 0))
        draw_grid(renderer)

        for x in range(len(current_tiles)):
            for y in range(len(current_tiles[x])):
                tile = current_tiles[x][y]
                if tile == 0:
                    continue
                if tile == 1:
                    continue
                if tile == 2:
                    fill_tile_border(renderer, int(x), int(y), COLOR_SNAKE_BORDER)
                    fill_tile(renderer, int(x), int(y), COLOR_SNAKE)
                if tile == 4:
                    fill_tile_border(renderer, int(x), int(y), COLOR_SNAKE_HEAD_BORDER)
                    fill_tile(renderer, int(x), int(y), COLOR_SNAKE_HEAD)
                if tile == 3:
                    fill_tile_border(renderer, int(x), int(y), COLOR_FOOD_BORDER)
                    fill_tile(renderer, int(x), int(y), COLOR_FOOD)

        if snake.get_score() > old_score:
            old_score = snake.get_score()

        text = factory.from_text("Score: " + str(snake.get_score()) + "  Moves: " + str(moves), fontmanager=fontManager)
        renderer.copy(text, dstrect=(0, 0, text.size[0],text.size[1]))

        renderer.present()

        sdl2.SDL_Delay(args.sleep)

        if autoplay and (game_over or moves >= MAX_MOVES):
            snake.reset()
            moves = 0
            old_score = 0
            game_over = False

    return 0

if __name__ == "__main__":
    sys.exit(run())
