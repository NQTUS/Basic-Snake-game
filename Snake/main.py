import pygame, sys, random
from pygame.math import Vector2

class FRUIT:
    def __init__(self):
        self.randomize()
    
    def draw_fruit(self, screen):
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size ,cell_size, cell_size)
        #pygame.draw.rect(screen, (255,100,100) ,fruit_rect)
        screen.blit(apple, fruit_rect)
    
    def randomize(self):
        self.x = random.randint(0,cell_number-1)
        self.y = random.randint(0,int(cell_number/2)-1)
        self.pos = Vector2(self.x, self.y)

class SNAKE:
    
    def __init__(self):
        self.body = [Vector2(5,5), Vector2(4,5),Vector2(3,5)]
        self.direction = Vector2(1,0)
        self.new_block = False 
        
        self.cur1 = pygame.image.load('Snake/cur1.png').convert_alpha()
        self.cur2 = pygame.image.load('Snake/cur2.png').convert_alpha()
        self.cur3 = pygame.image.load('Snake/cur3.png').convert_alpha()
        self.cur4 = pygame.image.load('Snake/cur4.png').convert_alpha()
        
        self.bodyhor = pygame.image.load('Snake/bodyhor.png').convert_alpha()
        self.bodyver = pygame.image.load('Snake/bodyver.png').convert_alpha()
        
        self.headup = pygame.image.load('Snake/headup.png').convert_alpha()
        self.headdown = pygame.image.load('Snake/headdown.png').convert_alpha()
        self.headright = pygame.image.load('Snake/headright.png').convert_alpha()
        self.headleft = pygame.image.load('Snake/headleft.png').convert_alpha()
        
        self.tailup = pygame.image.load('Snake/tailup.png').convert_alpha()
        self.taildown = pygame.image.load('Snake/taildown.png').convert_alpha()
        self.tailright = pygame.image.load('Snake/tailright.png').convert_alpha()
        self.tailleft = pygame.image.load('Snake/tailleft.png').convert_alpha()
    
    def draw_snake(self, screen):
        
        self.update_head()
        self.update_tail()
        
        for i, block in enumerate(self.body):
            x_pos = block.x * cell_size
            y_pos = block.y * cell_size
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            
            if i == 0:
                screen.blit(self.head, block_rect)
            elif i == len(self.body)-1:
                screen.blit(self.tail, block_rect)
            else:
                pre = self.body[i + 1] - block
                next = self.body[i - 1] - block
                if pre.x == next.x:
                    screen.blit(self.bodyver, block_rect)
                if pre.y == next.y:
                    screen.blit(self.bodyhor, block_rect)
                else:
                    if pre.x == -1 and next.y == -1 or pre.y == -1 and next.x == -1:
                        screen.blit(self.cur4, block_rect)
                    elif pre.x == -1 and next.y == 1 or pre.y == 1 and next.x == -1:
                        screen.blit(self.cur3, block_rect)
                    elif pre.x == 1 and next.y == -1 or pre.y == -1 and next.x == 1:
                        screen.blit(self.cur1, block_rect)
                    elif pre.x == 1 and next.y == 1 or pre.y == 1 and next.x == 1:
                        screen.blit(self.cur2, block_rect)
            
    def update_head(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0): self.head = self.headleft
        elif head_relation == Vector2(-1,0): self.head = self.headright
        elif head_relation == Vector2(0,1): self.head = self.headup
        elif head_relation == Vector2(0,-1): self.head = self.headdown
    
    def update_tail(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0): self.tail = self.tailleft
        elif tail_relation == Vector2(-1,0): self.tail = self.tailright
        elif tail_relation == Vector2(0,1): self.tail = self.tailup
        elif tail_relation == Vector2(0,-1): self.tail = self.taildown
        
    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
        
    
    def add_block(self):
        self.new_block = True

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
    
    def update(self):
        self.snake.move_snake()
        self.colision()
        self.check_fail()
    
    def draw(self):
        self.draw_grass(screen)
        self.fruit.draw_fruit(screen)
        self.snake.draw_snake(screen)
        
    def colision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
    
    def check_fail(self):
        if not 0  <= self.snake.body[0].x <= (cell_number - 1) or not 0 <= self.snake.body[0].y < cell_number/2:
            self.game_over()
        
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    
    def game_over(self):
        pygame.quit()
        sys.exit()
    
    def draw_grass(self, screen):
        grass_color = (167, 209, 61)
        
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col*cell_size,row * cell_size,cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            
            else:
                for col in range(cell_number):
                    if col % 2 == 1:
                        grass_rect = pygame.Rect(col*cell_size,row * cell_size,cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
                
        
        

cell_size = 40
cell_number = 25

screen = pygame.display.set_mode((cell_number*cell_size, cell_size*cell_number/2))
clock = pygame.time.Clock()
apple = pygame.image.load('Snake/apple.png').convert_alpha()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            
            if main_game.snake.direction.y != 1:
                if event.key == pygame.K_UP:
                    main_game.snake.direction = Vector2(0, -1)
            
            if main_game.snake.direction.y != -1:
                if event.key == pygame.K_DOWN:
                    main_game.snake.direction = Vector2(0, 1)
                    
            if main_game.snake.direction.x != -1:
                if event.key == pygame.K_RIGHT:
                    main_game.snake.direction = Vector2(1, 0)
            
            if main_game.snake.direction.x != 1:
                if event.key == pygame.K_LEFT:
                    main_game.snake.direction = Vector2(-1, 0)
            
    #draw all elements
    screen.fill((175,215,78))
    main_game.draw()
    pygame.display.update()
    clock.tick(60)