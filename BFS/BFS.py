from bfs_snake_game import *
import bfs_snake_game
from os import environ

WHITE = (255, 255, 255)
BLUE = (84, 194, 205)
DARKBLUE = (93, 216, 228)
GREEN = (0,255,0)
DARKGREEN = (0,100,0)
RED = (220,20,60)
MAROON = (128,0,0)
BLACK = (0,0,0)
GRAY = (128,128,128)

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
CELL_SIZE = 64
try:
    assert WINDOW_WIDTH % CELL_SIZE == 0
except:
    print("assertion error")

try:
    assert WINDOW_HEIGHT % CELL_SIZE == 0
except:
    print("Assertion error")

WINDOW_CELL_ROW = int(WINDOW_WIDTH/CELL_SIZE)
WINDOW_CELL_COLUMN = int(WINDOW_HEIGHT/CELL_SIZE)

DISPLAY_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
WHITE = (255, 255, 255)
def draw_grid(snake_moves, score):
    FONT_STYLE = pygame.font.Font("./assets/arial.ttf", 20)
    for x in range(0,WINDOW_CELL_ROW):
            for y in range(0,WINDOW_CELL_COLUMN):
                if(x + y) % 2 == 0:
                    even = pygame.Rect((y*CELL_SIZE, x*CELL_SIZE), (CELL_SIZE,CELL_SIZE))
                    pygame.draw.rect(DISPLAY_WINDOW, DARKBLUE, even)
                else:
                    odd = pygame.Rect((y*CELL_SIZE, x*CELL_SIZE), (CELL_SIZE,CELL_SIZE))
                    pygame.draw.rect(DISPLAY_WINDOW, BLUE, odd)
    if snake_moves==0:
        s = FONT_STYLE.render("Score: "+str(score)+"  Moves: "+str(snake_moves),True, WHITE)
    else:
        s = FONT_STYLE.render("Score: "+str(score)+"  Moves: "+str(snake_moves),True, WHITE)
        s.get_rect().topleft = (WINDOW_WIDTH - int(WINDOW_WIDTH/5), 10)
        DISPLAY_WINDOW.blit(s,s.get_rect())

def game():
    pygame.init()
    environ['SDL_VIDEO_CENTERED'] = '1'
    game_surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    snake = Snake(game_surface)

    mainloop = True
    while mainloop:
        DISPLAY_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        snake_moves, score = snake.get_moves()
        draw_grid(snake_moves, score)
        snake.update()

        clock.tick(FPS)
        pygame.display.update()


if __name__ == '__main__':
    game()
