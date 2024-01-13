import pygame
from pygame.locals import KEYDOWN, K_ESCAPE, K_SPACE, K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT
import random

random.seed()

pygame.init()

clock = pygame.time.Clock()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

BLOCK_SIZE = 25
BORDER_WIDTH = 3

ROWS = 15
COLS = 15

HEIGHT = ROWS*BLOCK_SIZE+(ROWS-1)*BORDER_WIDTH
WIDTH = COLS*BLOCK_SIZE+(COLS-1)*BORDER_WIDTH

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((0, 0, 0))

X_POS = (SCREEN_WIDTH-WIDTH)//2
Y_POS = SCREEN_HEIGHT-HEIGHT-X_POS

GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

V = BLOCK_SIZE+BORDER_WIDTH

v_x = V
v_y = 0

total = 0
highest = 0

pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(X_POS-8, Y_POS-8, WIDTH+16, HEIGHT+16))
pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(X_POS, Y_POS, WIDTH, HEIGHT))
for row in range(1, ROWS):
    pygame.draw.rect(screen, GRAY, pygame.Rect(X_POS, row*BLOCK_SIZE+(row-1)*BORDER_WIDTH+Y_POS, WIDTH, BORDER_WIDTH))
for col in range(1, COLS):
    pygame.draw.rect(screen, GRAY, pygame.Rect(col*BLOCK_SIZE+(col-1)*BORDER_WIDTH+X_POS, Y_POS, BORDER_WIDTH, HEIGHT))

font = pygame.font.SysFont('Sans', 50, False, False)
total_text = font.render("total: ", True, (255, 255, 255))
TEXT_X_POS = total_text.get_width()+50
screen.blit(total_text, (50, 50))

text = font.render(str(total), True, (255, 255, 255))
screen.blit(text, (TEXT_X_POS, 50))

font2 = pygame.font.SysFont('Sans', 20, False, False)
highest_text = font2.render("highest: ", True, (255, 255, 255))
HIGHEST_X_POS = highest_text.get_width()+460
screen.blit(highest_text, (460, 20))

text2 = font2.render(str(highest), True, (255, 255, 255))
screen.blit(text2, (HIGHEST_X_POS, 20))

def get_position(x: int, y: int) -> tuple:
    global BLOCK_SIZE, BORDER_WIDTH, X_POS, Y_POS
    return (X_POS+x*(BLOCK_SIZE+BORDER_WIDTH), Y_POS+y*(BLOCK_SIZE+BORDER_WIDTH))

position = get_position(5, 5)
position2 = get_position(4, 5)
player = [pygame.Rect(position[0], position[1], BLOCK_SIZE, BLOCK_SIZE),
          pygame.Rect(position2[0], position2[1], BLOCK_SIZE, BLOCK_SIZE)]

for i in player:
    pygame.draw.rect(screen, GREEN, i)

def set_food_position():
    global X_POS, Y_POS, COLS, ROWS, BLOCK_SIZE, food, player, RED
    while pygame.Rect.collidelist(food, player) > -1:
        x = random.randint(0, COLS-1)
        y = random.randint(0, ROWS-1)
        pos = get_position(x, y)
        food.left, food.top = pos
    screen.blit(food_image, food)

food_image = pygame.image.load("apple.png")

food = food_image.get_rect(left=player[0].left, top=player[0].top)

#food = pygame.Rect(player[0].left, player[0].top, BLOCK_SIZE, BLOCK_SIZE)
set_food_position()

def reset():
    global player, food, alive, total, v_x, v_y, X_POS, Y_POS, V, HIGHEST_X_POS, text2, highest
    for i in player[1:]:
        pygame.draw.rect(screen, (0, 0, 0), i)
    pygame.draw.rect(screen, (0, 0, 0), food)
    player = player[:2]
    player[0].topleft = (X_POS+V*5, Y_POS+V*5)
    player[1].topleft = (X_POS+V*4, Y_POS+V*5)
    v_x = V
    v_y = 0
    for i in player:
        pygame.draw.rect(screen, GREEN, i)
    set_food_position()
    if total > highest:
        highest = total
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(HIGHEST_X_POS, 20, text2.get_width(), text2.get_height()))
        text2 = font2.render(str(highest), True, (255, 255, 255))
        screen.blit(text2, (HIGHEST_X_POS, 20))
    total = 0
    update_total()
    alive = True

def update_total():
    global TEXT_X_POS, text, total
    pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(TEXT_X_POS, 50, text.get_width(), text.get_height()))
    text = font.render(str(total), True, (255, 255, 255))
    screen.blit(text, (TEXT_X_POS, 50))


def update(keys):
    global player, X_POS, Y_POS, WIDTH, HEIGHT, BLOCK_SIZE, V, alive, v_x, v_y, total
    tail = player[-1].copy()
    
    for i in range(len(player)-1, 0, -1):
        player[i].topleft = player[i-1].topleft
    
    if keys[K_UP]:
        turn(0, -V)
    elif keys[K_DOWN]:
        turn(0, V)
    elif keys[K_LEFT]:
        turn(-V, 0)
    elif keys[K_RIGHT]:
        turn(V, 0)
    
    player[0].move_ip(v_x, v_y)
    
    
    if pygame.Rect.colliderect(player[1], food):
        player.append(tail)
        set_food_position()
        total += 1
        update_total()
    else:
        pygame.draw.rect(screen, (0, 0, 0), tail)
    
    index = pygame.Rect.collidelist(player[0], player[1:])
    if player[0].left >= X_POS and player[0].right <= X_POS+WIDTH and player[0].top >= Y_POS and player[0].bottom <= Y_POS+HEIGHT and index == -1:
        pygame.draw.rect(screen, GREEN, player[0])
    else:
        alive = False

def turn(new_v_x, new_v_y):
    global v_x, v_y
    if abs(new_v_x) != abs(v_x):
        v_x, v_y = new_v_x, new_v_y

running = True
alive = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_SPACE:
                if not alive:
                    reset()
    if alive:
        update(pygame.key.get_pressed())
        pygame.display.flip()
    
    clock.tick(5)

