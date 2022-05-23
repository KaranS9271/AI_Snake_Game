import pygame, random, sys, os

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
CELL_SIZE = 64
assert WINDOW_WIDTH % CELL_SIZE == 0;assert WINDOW_HEIGHT % CELL_SIZE == 0
WINDOW_CELL_ROW = int(WINDOW_WIDTH/CELL_SIZE)
WINDOW_CELL_COLUMN = int(WINDOW_HEIGHT/CELL_SIZE)

WHITE = (255, 255, 255)
BLUE = (84, 194, 205)
DARKBLUE = (93, 216, 228)
GREEN = (0,255,0)
DARKGREEN = (0,100,0)
RED = (220,20,60)
MAROON = (128,0,0)
BLACK = (0,0,0)
GRAY = (128,128,128)

FRAME_RATE = 45
FPS_CLOCK = pygame.time.Clock()

def set_font():
    pygame.init()
    global FONT_STYLE
    FONT_STYLE = pygame.font.Font("./assets/arial.ttf", 20)
    pygame.display.set_caption("Snake Game")

UP = 'up'
DOWN = 'down'
RIGHT = 'right'
LEFT = 'left'

def check(snake_body, snake_coord):
    for i in snake_coord:
        if snake_body == i:
            return True
    return False

def place_food(snake_coord):
    snake_body = {'x': random.randint(0, WINDOW_CELL_ROW - 1), 'y': random.randint(0, WINDOW_CELL_COLUMN - 1)}
    while check(snake_body, snake_coord):
        snake_body = {'x': random.randint(0, WINDOW_CELL_ROW - 1), 'y': random.randint(0, WINDOW_CELL_COLUMN - 1)}
    return snake_body

x_coord = random.randint(0, WINDOW_CELL_ROW - 5);y_coord = random.randint(0, WINDOW_CELL_COLUMN - 5)
snake_coord = [{'x':x_coord,'y':y_coord},
               {'x':x_coord - 1,'y':y_coord - 1}]
food = place_food(snake_coord)
direction = RIGHT
snake_moves = 0;snake_head = 0; START_LENGTH = len(snake_coord)

def get_snake_food():
    global x_coord, y_coord, snake_coord, snake_head, START_LENGTH
    x_coord = random.randint(0, WINDOW_CELL_ROW - 5);y_coord = random.randint(0, WINDOW_CELL_COLUMN - 5)
    snake_coord = [{'x':x_coord,'y':y_coord},
               {'x':x_coord - 1,'y':y_coord - 1}]
    START_LENGTH = len(snake_coord)
    food = place_food(snake_coord)

def hamiltonian(prev_direction, snake_head):
    if snake_head['x'] == 1:
        if snake_head['y'] == WINDOW_CELL_COLUMN - 1:
            return LEFT
        elif snake_head['y'] == 0:
            return RIGHT
        if prev_direction == LEFT:
            return DOWN
        elif prev_direction == DOWN:
            return RIGHT
    elif snake_head['x'] >= 1 and snake_head['x'] <= WINDOW_CELL_ROW-2:
        if prev_direction == RIGHT:
            return RIGHT
        elif prev_direction == LEFT:
            return LEFT
    elif snake_head['x'] == (WINDOW_CELL_ROW-1):
        if prev_direction == RIGHT:
            return DOWN
        elif prev_direction == DOWN:
            return LEFT
    elif snake_head['x'] == 0:
        if snake_head['y'] != 0:
            return UP
        else:
            return RIGHT

def game(): 
    global food, direction, snake_moves, new_snake_head
    snake_moves = 0; new_snake_head = snake_coord[0]
    DISPLAY_WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    get_snake_food()
    direction = RIGHT
    while True:
        if(sys.argv[1] == "basic"):
            pygame.display.set_caption("Basic Snake Game")
            previous_direction = direction
        elif(sys.argv[1] == "hamiltonian"):
            pygame.display.set_caption("Hamiltonian based Snake Game")
            direction = hamiltonian(direction, snake_coord[0])
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                stop()
            elif event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_UP or event.key == pygame.K_w) and direction != DOWN:
                    direction = UP
                elif(event.key == pygame.K_DOWN or event.key == pygame.K_s) and direction != UP:
                    direction = DOWN
                elif(event.key == pygame.K_LEFT or event.key == pygame.K_a) and direction != RIGHT:
                    direction = LEFT
                elif(event.key == pygame.K_RIGHT or event.key == pygame.K_d) and direction != LEFT:
                    direction = RIGHT 
                elif(event.key == pygame.K_ESCAPE):
                    stop()
        
        if snake_coord[snake_head] == food:
            if(len(snake_coord) == (WINDOW_CELL_COLUMN * WINDOW_CELL_ROW)):
                return game_over_screen(DISPLAY_WINDOW)
            else:
                food = place_food(snake_coord)
        else:
            del snake_coord[-1]

        if((snake_coord[snake_head]['x'] == -1) or (snake_coord[snake_head]['y'] == -1) or (snake_coord[snake_head]['x'] == WINDOW_CELL_ROW) or (snake_coord[snake_head]['y'] == WINDOW_CELL_COLUMN)):
            return game_over_screen(DISPLAY_WINDOW)
        for sb in snake_coord[1:]:
            if sb == snake_coord[snake_head]:
                return game_over_screen(DISPLAY_WINDOW)
        
        if(sys.argv[0] == "basic_snake_game"):
            if not verify_direction(previous_direction, direction):
                direction = previous_direction
        if direction == UP:
            new_snake_head = {'x': snake_coord[snake_head]['x'], 'y': snake_coord[snake_head]['y'] - 1}
        elif direction == DOWN:
            new_snake_head = {'x': snake_coord[snake_head]['x'], 'y': snake_coord[snake_head]['y'] + 1}
        elif direction == LEFT:
            new_snake_head = {'x': snake_coord[snake_head]['x'] - 1, 'y': snake_coord[snake_head]['y']}
        elif direction == RIGHT:
            new_snake_head = {'x': snake_coord[snake_head]['x'] + 1, 'y': snake_coord[snake_head]['y']}
        snake_coord.insert(0, new_snake_head)
        draw_grid(DISPLAY_WINDOW)
        draw_snake(DISPLAY_WINDOW)
        draw_food(DISPLAY_WINDOW)
        draw_score(DISPLAY_WINDOW)
        pygame.display.update()
        FPS_CLOCK.tick(FRAME_RATE)
    
def stop():
    pygame.quit()
    sys.exit()

def verify_direction(previous_direction, direction):
    if (previous_direction == UP and direction == DOWN) or (previous_direction == DOWN and direction == UP) or (previous_direction == LEFT and direction == RIGHT) or (previous_direction == RIGHT and direction == LEFT):
        return False
    return True

def draw_grid(DISPLAY_WINDOW):
    for x in range(0,WINDOW_CELL_ROW):
            for y in range(0,WINDOW_CELL_COLUMN):
                if(x + y) % 2 == 0:
                    even = pygame.Rect((y*CELL_SIZE, x*CELL_SIZE), (CELL_SIZE,CELL_SIZE))
                    pygame.draw.rect(DISPLAY_WINDOW, DARKBLUE, even)
                else:
                    odd = pygame.Rect((y*CELL_SIZE, x*CELL_SIZE), (CELL_SIZE,CELL_SIZE))
                    pygame.draw.rect(DISPLAY_WINDOW, BLUE, odd)

def draw_color(x, y, in_color, out_color, DISPLAY_WINDOW):
    snake_outer = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
    snake_inner = pygame.Rect(x + 4, y + 4, CELL_SIZE - 8, CELL_SIZE - 8)
    pygame.draw.rect(DISPLAY_WINDOW, out_color, snake_outer)
    pygame.draw.rect(DISPLAY_WINDOW, in_color, snake_inner)

def draw_snake(DISPLAY_WINDOW):
    x, y = snake_coord[snake_head]['x'] * CELL_SIZE, snake_coord[snake_head]['y'] * CELL_SIZE
    draw_color(x, y, BLACK, GRAY, DISPLAY_WINDOW)
    for i in range(1, len(snake_coord)):
        x, y = snake_coord[i]['x'] * CELL_SIZE, snake_coord[i]['y'] * CELL_SIZE
        draw_color(x, y, GREEN, DARKGREEN, DISPLAY_WINDOW)
        
def draw_food(DISPLAY_WINDOW):
    x, y = food['x'] * CELL_SIZE, food['y'] * CELL_SIZE
    draw_color(x, y, RED, MAROON, DISPLAY_WINDOW)

def draw_score(DISPLAY_WINDOW):
    global snake_moves
    pygame.init()
    FONT_STYLE = pygame.font.Font("./assets/arial.ttf", 20)
    if snake_moves==0:
            s = FONT_STYLE.render("Score: "+str(len(snake_coord) - START_LENGTH)+"  Moves: "+str(snake_moves),True, WHITE)
    else:
            s = FONT_STYLE.render("Score: "+str(len(snake_coord) - START_LENGTH)+"  Moves: "+str(snake_moves - 1),True, WHITE)
    s.get_rect().topleft = (WINDOW_WIDTH - int(WINDOW_WIDTH/5), 10)
    DISPLAY_WINDOW.blit(s,s.get_rect())
    snake_moves=snake_moves + 1

def draw_text(text, location, DISPLAY_WINDOW):
    text_font = pygame.font.Font("./assets/arial.ttf",50).render(text, True, WHITE)
    result = text_font.get_rect()
    result.midtop = location
    DISPLAY_WINDOW.blit(text_font, result)

def check_key():
    quit_game = len(pygame.event.get(pygame.QUIT))
    if(quit_game>0):
        stop()
    else:
        key = pygame.event.get(pygame.KEYUP)
        if(len(key) == 0):
            return None
        elif key[0].key == pygame.K_ESCAPE:
            stop()

def game_over_screen(DISPLAY_WINDOW):
    game_over = "Game Over"
    draw_text(game_over, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2), DISPLAY_WINDOW)
    text = "Press Any Key"
    draw_text(text, (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + WINDOW_HEIGHT/4), DISPLAY_WINDOW)
    pygame.display.update()
    pygame.time.wait(1500)
    if check_key():
        pygame.event.get()
        return
    pygame.display.update()
    FPS_CLOCK.tick(FRAME_RATE)

if __name__ == "__main__":
    if(sys.argv[1] == "bfs"):
        os.system('python ./BFS/BFS.py')
    elif(sys.argv[1] == "astar"):
        os.system('python ./Astar/Astar.py')
    elif(sys.argv[1] == "astar2"):
        os.system('python ./Astar2/Astar2.py')
    elif(sys.argv[1] == "dql"):
        os.system('python ./Deep_Q_Learning/agents.py')
    elif(sys.argv[1] == "a2c"):
        os.system('python ./Actor_Critic/simulate.py --model-path Actor_Critic/models/model --x 10 --y 10 --seed 123 --sleep 10 --autoplay')
    else:
        set_font()
        while True:
            game()