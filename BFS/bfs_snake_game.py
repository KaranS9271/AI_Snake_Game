import pygame
from Config import *
from copy import deepcopy
from random import randrange

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 640
CELL_SIZE = 64
WINDOW_CELL_ROW = int(WINDOW_WIDTH/CELL_SIZE)
WINDOW_CELL_COLUMN = int(WINDOW_HEIGHT/CELL_SIZE)
DARKGREEN = (0,100,0)
BLACK= (0,0,0)
MAROON = (128,0,0)
GRAY = (128,128,128)
RED =(255,0,0)
tm=0

class Square:
    def __init__(self, pos, surface, is_apple=False):
        self.pos = pos
        self.surface = surface
        self.is_apple = is_apple
        self.is_tail = False
        self.is_head= False
        self.dir = [-1, 0]

        if self.is_apple:
            self.dir = [0, 0]

    def draw(self, clr=SNAKE_CLR):
        x, y = self.pos[0], self.pos[1]
        ss, gs = SQUARE_SIZE, GAP_SIZE

        if self.dir == [-1, 0]:
            if self.is_tail:
                pygame.draw.rect(self.surface, DARKGREEN, (x * ss, y * ss, ss, ss))
                pygame.draw.rect(self.surface, clr, ((x * ss) + gs, (y * ss) + gs, ss - 2*gs, ss - 2*gs))
            elif self.is_head:
                pygame.draw.rect(self.surface, GRAY, (x * ss, y * ss, ss, ss))
                pygame.draw.rect(self.surface, clr, ((x * ss) + gs, (y * ss) + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, DARKGREEN, (x * ss, y * ss, ss, ss))
                pygame.draw.rect(self.surface, clr, ((x * ss) + gs, (y * ss) + gs, ss - 2*gs, ss - 2*gs))

        if self.dir == [1, 0]:
            if self.is_tail:
                pygame.draw.rect(self.surface, DARKGREEN, (x * ss, y * ss, ss, ss))
                pygame.draw.rect(self.surface, clr, ((x * ss) + gs, (y * ss) + gs, ss - 2*gs, ss - 2*gs))
            elif self.is_head:
                pygame.draw.rect(self.surface, GRAY, (x * ss, y * ss, ss, ss))
                pygame.draw.rect(self.surface, clr, ((x * ss) + gs, (y * ss) + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, DARKGREEN, (x * ss, y * ss, ss, ss))
                pygame.draw.rect(self.surface, clr, ((x * ss) + gs, (y * ss) + gs, ss - 2*gs, ss - 2*gs))

        if self.dir == [0, 1]:
            if self.is_tail:
                pygame.draw.rect(self.surface, DARKGREEN, (x * ss, y * ss, ss, ss))
                pygame.draw.rect(self.surface, clr, ((x * ss) + gs, (y * ss) + gs, ss - 2*gs, ss - 2*gs))
            elif self.is_head:
                pygame.draw.rect(self.surface, GRAY, (x * ss, y * ss, ss, ss))
                pygame.draw.rect(self.surface, clr, ((x * ss) + gs, (y * ss) + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, DARKGREEN, (x * ss, y * ss, ss, ss))
                pygame.draw.rect(self.surface, clr, ((x * ss) + gs, (y * ss) + gs, ss - 2*gs, ss - 2*gs))

        if self.dir == [0, -1]:
            if self.is_tail:
                pygame.draw.rect(self.surface, DARKGREEN, (x * ss, y * ss, ss, ss))
                pygame.draw.rect(self.surface, clr, ((x * ss) + gs, (y * ss) + gs, ss - 2*gs, ss - 2*gs))
            elif self.is_head:
                pygame.draw.rect(self.surface, GRAY, (x * ss, y * ss, ss, ss))
                pygame.draw.rect(self.surface, clr, ((x * ss) + gs, (y * ss) + gs, ss - 2*gs, ss - 2*gs))
            else:
                pygame.draw.rect(self.surface, DARKGREEN, (x * ss, y * ss, ss, ss))
                pygame.draw.rect(self.surface, clr, ((x * ss) + gs, (y * ss) + gs, ss - 2*gs, ss - 2*gs))

        if self.is_apple:
            pygame.draw.rect(self.surface, MAROON, (x * ss, y * ss, ss, ss))
            pygame.draw.rect(self.surface, RED, ((x * ss) + gs, (y * ss) + gs, ss - 2*gs, ss - 2*gs))

    def movement(self, direction):
        self.dir = direction
        self.pos[0] += self.dir[0]   
        self.pos[1] += self.dir[1]

    def wall_collison(self):
        if (self.pos[0] <= -1) or (self.pos[0] >= ROWS) or (self.pos[1] <= -1) or (self.pos[1] >= ROWS):
            return True
        else:
            return False


class Snake:
    def __init__(self, surface):
        self.surface = surface
        self.is_dead = False
        self.squares_start_pos = [[ROWS // 2 + i, ROWS // 2] for i in range(INITIAL_SNAKE_LENGTH)]
        self.turns = {}
        self.dir = [-1, 0]
        self.score = 0
        self.moves_without_eating = 0
        self.apple = Square([randrange(ROWS), randrange(ROWS)], self.surface, is_apple=True)

        self.squares = []
        for pos in self.squares_start_pos:
            self.squares.append(Square(pos, self.surface))

        self.head = self.squares[0]
        self.tail = self.squares[-1]
        self.tail.is_tail = True

        self.path = []
        self.is_virtual_snake = False
        self.total_moves = 0
        self.won_game = False

    def draw(self):
        self.apple.draw(APPLE_CLR)
        self.head.draw(HEAD_CLR)
        self.head.is_head= True
        for sqr in self.squares[1:]:
            if self.is_virtual_snake:
                sqr.draw(VIRTUAL_SNAKE_CLR)
            else:
                sqr.draw()

    def direction_setter(self, direction):
        if direction == 'left':
            if not self.dir == [1, 0]:
                self.dir = [-1, 0]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "right":
            if not self.dir == [-1, 0]:
                self.dir = [1, 0]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "up":
            if not self.dir == [0, 1]:
                self.dir = [0, -1]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir
        if direction == "down":
            if not self.dir == [0, -1]:
                self.dir = [0, 1]
                self.turns[self.head.pos[0], self.head.pos[1]] = self.dir

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            keys = pygame.key.get_pressed()

            for _ in keys:
                if keys[pygame.K_LEFT]:
                    self.direction_setter('left')

                elif keys[pygame.K_RIGHT]:
                    self.direction_setter('right')

                elif keys[pygame.K_UP]:
                    self.direction_setter('up')

                elif keys[pygame.K_DOWN]:
                    self.direction_setter('down')

    def movement(self):
        for j, sqr in enumerate(self.squares):
            p = (sqr.pos[0], sqr.pos[1])
            if p in self.turns:
                turn = self.turns[p]
                sqr.movement([turn[0], turn[1]])
                if j == len(self.squares) - 1:
                    self.turns.pop(p)
            else:
                sqr.movement(sqr.dir)
        self.moves_without_eating += 1

    def add_tail(self):
        self.squares[-1].is_tail = False
        tail = self.squares[-1]

        direction = tail.dir
        if direction == [1, 0]:
            self.squares.append(Square([tail.pos[0] - 1, tail.pos[1]], self.surface))
        if direction == [-1, 0]:
            self.squares.append(Square([tail.pos[0] + 1, tail.pos[1]], self.surface))
        if direction == [0, 1]:
            self.squares.append(Square([tail.pos[0], tail.pos[1] - 1], self.surface))
        if direction == [0, -1]:
            self.squares.append(Square([tail.pos[0], tail.pos[1] + 1], self.surface))

        self.squares[-1].dir = direction
        self.squares[-1].is_tail = True 

    def reset(self):
        self.__init__(self.surface)

    def hitting_self(self):
        for sqr in self.squares[1:]:
            if sqr.pos == self.head.pos:
                return True

    def generate_apple(self):
        self.apple = Square([randrange(WINDOW_CELL_ROW), randrange(WINDOW_CELL_COLUMN)], self.surface, is_apple=True)
        if not self.is_position_free(self.apple.pos):
            self.generate_apple()

    def eating_apple(self):
        if self.head.pos == self.apple.pos and not self.is_virtual_snake and not self.won_game:
            self.generate_apple()
            self.moves_without_eating = 0
            self.score += 1
            return True

    def go_to(self, position): 
        if self.head.pos[0] - 1 == position[0]:
            self.direction_setter('left')
        if self.head.pos[0] + 1 == position[0]:
            self.direction_setter('right')
        if self.head.pos[1] - 1 == position[1]:
            self.direction_setter('up')
        if self.head.pos[1] + 1 == position[1]:
            self.direction_setter('down')

    def is_position_free(self, position):
        if position[0] >= ROWS or position[0] < 0 or position[1] >= ROWS or position[1] < 0:
            return False
        for sqr in self.squares:
            if sqr.pos == position:
                return False
        return True

    def bfs(self, s, e):
        q = [s] 
        visited = {tuple(pos): False for pos in GRID}

        visited[s] = True
        prev = {tuple(pos): None for pos in GRID}

        while q:  
            node = q.pop(0)
            neighbors = ADJACENCY_DICT[node]
            for next_node in neighbors:
                if self.is_position_free(next_node) and not visited[tuple(next_node)]:
                    q.append(tuple(next_node))
                    visited[tuple(next_node)] = True
                    prev[tuple(next_node)] = node

        path = list()
        p_node = e

        start_node_found = False
        while not start_node_found:
            if prev[p_node] is None:
                return []
            p_node = prev[p_node]
            if p_node == s:
                path.append(e)
                return path
            path.insert(0, p_node)

        return []

    def create_virtual_snake(self): 
        v_snake = Snake(self.surface)
        for i in range(len(self.squares) - len(v_snake.squares)):
            v_snake.add_tail()

        for i, sqr in enumerate(v_snake.squares):
            sqr.pos = deepcopy(self.squares[i].pos)
            sqr.dir = deepcopy(self.squares[i].dir)

        v_snake.dir = deepcopy(self.dir)
        v_snake.turns = deepcopy(self.turns)
        v_snake.apple.pos = deepcopy(self.apple.pos)
        v_snake.apple.is_apple = True
        v_snake.is_virtual_snake = True

        return v_snake

    def get_path_to_tail(self):
        tail_pos = deepcopy(self.squares[-1].pos)
        self.squares.pop(-1)
        path = self.bfs(tuple(self.head.pos), tuple(tail_pos))
        self.add_tail()
        return path

    def get_available_neighbors(self, pos):
        valid_neighbors = []
        neighbors = get_neighbors(tuple(pos))
        for n in neighbors:
            if self.is_position_free(n) and self.apple.pos != n:
                valid_neighbors.append(tuple(n))
        return valid_neighbors

    def longest_path_to_tail(self):
        neighbors = self.get_available_neighbors(self.head.pos)
        path = []
        if neighbors:
            dis = -9999
            for n in neighbors:
                if distance(n, self.squares[-1].pos) > dis:
                    v_snake = self.create_virtual_snake()
                    v_snake.go_to(n)
                    v_snake.movement()
                    if v_snake.eating_apple():
                        v_snake.add_tail()
                    if v_snake.get_path_to_tail():
                        path.append(n)
                        dis = distance(n, self.squares[-1].pos)
            if path:
                return [path[-1]]

    def any_safe_move(self):
        neighbors = self.get_available_neighbors(self.head.pos)
        path = []
        if neighbors:
            path.append(neighbors[randrange(len(neighbors))])
            v_snake = self.create_virtual_snake()
            for move in path:
                v_snake.go_to(move)
                v_snake.movement()
            if v_snake.get_path_to_tail():
                return path
            else:
                return self.get_path_to_tail()

    def get_moves(self):
        return self.total_moves, self.score

    def set_path(self):
        # If there is only 1 apple left for snake to win and it's adjacent to head
        if self.score == SNAKE_MAX_LENGTH - 1 and self.apple.pos in get_neighbors(self.head.pos):
            winning_path = [tuple(self.apple.pos)]
            print('Snake is about to win..')
            return winning_path

        v_snake = self.create_virtual_snake()
        path_1 = v_snake.bfs(tuple(v_snake.head.pos), tuple(v_snake.apple.pos))
        path_2 = []

        if path_1:
            for pos in path_1:
                v_snake.go_to(pos)
                v_snake.movement()

            v_snake.add_tail()
            path_2 = v_snake.get_path_to_tail()

        if path_2:
            return path_1 
        if self.longest_path_to_tail() and\
                self.score % 2 == 0 and\
                self.moves_without_eating < MAX_MOVES_WITHOUT_EATING / 2:
            return self.longest_path_to_tail()
        if self.any_safe_move():
            return self.any_safe_move()
        if self.get_path_to_tail():
            return self.get_path_to_tail()
        print('No available path, snake in danger!')

    def update(self):
        self.handle_events()

        self.path = self.set_path()
        if self.path:
            self.go_to(self.path[0])

        self.draw()
        self.movement()

        if self.score == ROWS * ROWS - INITIAL_SNAKE_LENGTH:
            self.won_game = True

            print("Snake won the game after {} moves"
                  .format(self.total_moves))

            pygame.time.wait(1000 * WAIT_SECONDS_AFTER_WIN)
            return 1

        self.total_moves += 1
        pygame.display.set_caption("BFS Snake Game")

        if self.hitting_self() or self.head.wall_collison():
            print("Snake is dead, trying again..")
            self.is_dead = True
            self.reset()

        if self.moves_without_eating == MAX_MOVES_WITHOUT_EATING:
            self.is_dead = True
            print("Snake got stuck, trying again..")
            self.reset()

        if self.eating_apple():
            self.add_tail()