import pygame
import sys
import random

# this initialises pygame, dont forget this.
pygame.init()

# defining the parameters of the display
WIDTH = 600
HEIGHT = 600

# inserting the settings above into the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

#  some other variables we use
RED = (255,0,0)
BLACK = (0,0,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
GREEN = (43,226,22)

PLAYER_SIZE = 50
PLAYER_POS = [WIDTH/2, HEIGHT-2*PLAYER_SIZE]

enemy_size = 50
enemy_pos = [random.randint(0,WIDTH-enemy_size), 0]
enemy_list = [enemy_pos]

speed = 10

score = 0

# if the game is not over..
game_over = False

clock = pygame.time.Clock()

myFont = pygame.font.SysFont("monospace", 35)
def set_level(score, speed):
    if score < 20:
        speed = 5
    elif score < 40:
        speed = 8
    elif score < 60:
        speed = 10
    else:
        speed = 15
    return speed


def drop_enemies(enemy_list):
    delay = random.random()
    if len(enemy_list) < 10 and delay < 0.05:
        x_pos = random.randint(0, WIDTH-enemy_size)
        y_pos = 0
        enemy_list.append([x_pos, y_pos])

def  draw_enemies(enemy_list):
    for enemy_pos in enemy_list:
        pygame.draw.rect(screen, BLUE, (enemy_pos[0], enemy_pos[1], enemy_size, enemy_size))

def update_enemy_pos(enemy_list, score):
    for idx, enemy_pos in enumerate(enemy_list):
        if enemy_pos[1] >= 0 and enemy_pos[1] < HEIGHT:
            enemy_pos[1] += speed
        else:
            enemy_list.pop(idx)
            score += 1
    return score

def collision_check(enemy_list, PLAYER_POS):
    for enemy_pos in enemy_list:
        if detect_collision(enemy_pos,PLAYER_POS):
            return True
    return False

def detect_collision(player_pos, enemy_pos):
    p_x = player_pos[0]
    p_y = player_pos[1]

    e_x = enemy_pos[0]
    e_y = enemy_pos[1]

    if (e_x >= p_x and e_x < (p_x + PLAYER_SIZE)) or (p_x >= e_x and p_x < (e_x+enemy_size)):
        if (e_y >= p_y and e_y < (p_y + PLAYER_SIZE)) or (p_y >= e_y and p_y < (e_y+ enemy_size)):
            return True
    return False

# Game mainloop

while not game_over:
    for event in pygame.event.get():
        # this is the code to enable the window to be closed
        if event.type == pygame.QUIT:
            sys.exit()

        # this is the code to track key(down) presses and what they do to our "player"
        if event.type == pygame.KEYDOWN:

            x = PLAYER_POS[0]
            y = PLAYER_POS[1]

            if event.key == pygame.K_LEFT:
                x -= 25
            elif event.key == pygame.K_RIGHT:
                x += 25

            PLAYER_POS = [x, y]

    screen.fill(BLACK)


    if detect_collision(PLAYER_POS, enemy_pos):
        game_over = True
        break

    drop_enemies(enemy_list)
    score = update_enemy_pos(enemy_list, score)
    speed = set_level(score, speed)


    text1 = "Block Drop v1.0"
    label1 = myFont.render(text1, 1, YELLOW)
    screen.blit(label1,(WIDTH-550, HEIGHT-590))

    text = "Score: " + str(score)
    label = myFont.render(text, 1, YELLOW)
    screen.blit(label,(WIDTH-200, HEIGHT-40))

    if collision_check(enemy_list, PLAYER_POS):
        game_over = True
        break
    draw_enemies(enemy_list)
    pygame.draw.rect(screen, GREEN, (PLAYER_POS[0], PLAYER_POS[1], PLAYER_SIZE, PLAYER_SIZE))


    clock.tick(30)

    pygame.display.update()