from os import DirEntry
from types import CellType
import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np

pygame.init()
font = pygame.font.Font('./assets/arial.ttf', 25)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
    
Point = namedtuple('Point', 'x, y')

WHITE = (255, 255, 255)
GREEN = (0,255,0)
DARKGREEN = (0,100,0)
RED = (220,20,60)
MAROON = (128,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GRAY = (128,128,128)
BLUE = (84, 194, 205)
DARKBLUE = (93, 216, 228)

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
CELL_SIZE = 64
assert WINDOW_WIDTH % CELL_SIZE == 0;assert WINDOW_HEIGHT % CELL_SIZE == 0
WINDOW_CELL_ROW = int(WINDOW_WIDTH/CELL_SIZE)
WINDOW_CELL_COLUMN = int(WINDOW_HEIGHT/CELL_SIZE)
DISPLAY_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

BLOCK_SIZE = CELL_SIZE
SPEED = 30

class SnakeGame:
    
    def __init__(self, w=WINDOW_WIDTH, h=WINDOW_HEIGHT):
        self.w = w
        self.h = h
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption("Deep Q Learning Snake Game")
        self.clock = pygame.time.Clock()
        self.reset()
        
    def reset(self):
        self.direction = Direction.RIGHT
        
        self.head = Point(self.w/2, self.h/2)
        self.snake = [self.head, 
                      Point(self.head.x-BLOCK_SIZE, self.head.y),
                      Point(self.head.x-(2*BLOCK_SIZE), self.head.y)]
        
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_ieration = 0
        
    def _place_food(self):
        x = random.randint(0, (self.w-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.h-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self._place_food()
        
    def draw_grid(self):
        for x in range(0,WINDOW_CELL_ROW):
                for y in range(0,WINDOW_CELL_COLUMN):
                    if(x + y) % 2 == 0:
                        even = pygame.Rect((y*CELL_SIZE, x*CELL_SIZE), (CELL_SIZE,CELL_SIZE))
                        pygame.draw.rect(DISPLAY_WINDOW, DARKBLUE, even)
                    else:
                        odd = pygame.Rect((y*CELL_SIZE, x*CELL_SIZE), (CELL_SIZE,CELL_SIZE))
                        pygame.draw.rect(DISPLAY_WINDOW, BLUE, odd)

    def play_step(self, action):
        self.frame_ieration +=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        self._move(action)
        self.snake.insert(0, self.head)
        
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_ieration > 50 * len(self.snake):
            game_over = True
            reward = -10
            return reward, game_over, self.score
        
        if self.head == self.food:
            self.score += 1
            reward = 10
            self._place_food()
        else:
            self.snake.pop()
        
        self._update_ui()
        self.clock.tick(SPEED)
        return reward, game_over, self.score
    
    def is_collision(self, pt = None):
        if pt is None:
            pt = self.head
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        if pt in self.snake[1:]:
            return True
        
        return False
        
    def _update_ui(self):
        self.draw_grid()
        
        for pt in self.snake:
            pygame.draw.rect(self.display, GRAY, pygame.Rect(self.snake[0].x, self.snake[0].y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, BLACK, pygame.Rect(self.snake[0].x+int(BLOCK_SIZE * 0.1), self.snake[0].y+int(BLOCK_SIZE * 0.1), (BLOCK_SIZE - int(BLOCK_SIZE * 0.2)), (BLOCK_SIZE - int(BLOCK_SIZE * 0.2))))
            pygame.draw.rect(self.display, DARKGREEN, pygame.Rect(pt.x, pt.y, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(self.display, GREEN, pygame.Rect(pt.x+int(BLOCK_SIZE * 0.1), pt.y+int(BLOCK_SIZE * 0.1), (BLOCK_SIZE - int(BLOCK_SIZE * 0.2)), (BLOCK_SIZE - int(BLOCK_SIZE * 0.2))))
            
        pygame.draw.rect(self.display, MAROON, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x+int(BLOCK_SIZE * 0.1), self.food.y+int(BLOCK_SIZE * 0.1), (BLOCK_SIZE - int(BLOCK_SIZE * 0.2)), (BLOCK_SIZE - int(BLOCK_SIZE * 0.2))))
        
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()
        
    def _move(self, action):

        clockwise = [Direction.RIGHT, Direction.DOWN, Direction.LEFT, Direction.UP]
        idx = clockwise.index(self.direction)

        if np.array_equal(action, [1,0,0]):
            new_dir = clockwise[idx]
        elif np.array_equal(action, [0,1,0]):
            next_idx = (idx+1)%4
            new_dir = clockwise[next_idx] 
        else:
            next_idx = (idx-1)%4
            new_dir = clockwise[next_idx]

        self.direction = new_dir

        x = self.head.x
        y = self.head.y
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE
            
        self.head = Point(x, y)
            