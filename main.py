import pygame
import math
import random
from pygame import mixer

pygame.init()

# Create Window
window = pygame.display.set_mode((800, 600))

# Background image
background = pygame.image.load("background.png")

# Background music
mixer.music.load('background.wav')
mixer.music.play(-1)

# Window Display and Icons
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("spaceship.png")  # loading the image
pygame.display.set_icon(icon)  # displaying the image

# Player
playerImg = pygame.image.load("spacearcade.png")
co_ordX = 370
co_ordY = 480
co_ordX_change = 0

# Enemy and multiple enemies
enemyImg = []
Enemy_co_ordX = []
Enemy_co_ordY = []
Enemy_cordX_change = []
Enemy_cordY_change = []
num_of_enemies = 6

# Enemy bullet
enemy_bullet_img = pygame.image.load('enemy_laser.png')
enemy_b_X = 0
enemy_b_Y = 50

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("invader.png"))
    Enemy_co_ordX.append(random.randint(0, 735))
    Enemy_co_ordY.append(random.randint(50, 150))
    Enemy_cordX_change.append(4)
    Enemy_cordY_change.append(40)

# Bullet
bulletImg = pygame.image.load("bullet.png")
Bullet_co_ordX = 0
Bullet_co_ordY = 480
Bullet_cordX_change = 0
Bullet_cordY_change = 10
bullet_state = "ready"


# score
score_value = 0
font = pygame.font.Font("HAMBH___.TTF", 40)
scoreX = 10
scoreY = 10


def show_score(x, y):
    score = font.render("Score :" + str(score_value), True, (51, 255, 255))
    window.blit(score, (x, y))


def player(x, y):
    window.blit(playerImg, (x, y))


def enemy(x, y, i):
    window.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    window.blit(bulletImg, (x + 16, y + 10))


def collides(Enemy_co_ordX, Enemy_co_ordY, Bullet_co_ordX, Bullet_co_ordY):
    distance = math.sqrt(math.pow(Enemy_co_ordX - Bullet_co_ordX, 2) + (math.pow(Enemy_co_ordY - Bullet_co_ordY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    # window background color
    window.fill((0, 0, 0))
    # background image to appear over the black screen
    window.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if statement to check if the key was pressed
        if event.type == pygame.KEYDOWN:
            # if statement to check if the key pressed is a left key
            if event.key == pygame.K_LEFT:
                co_ordX_change = -5
            # if statement to check if the key pressed is a right key
            if event.key == pygame.K_RIGHT:
                co_ordX_change = 5
            # if statement to fire a bullet when space bar is pressed
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    # Getting the current x-coordinate of the player and storing it in a bullet variable
                    Bullet_co_ordX = co_ordX
                    fire_bullet(Bullet_co_ordX, Bullet_co_ordY)
        # if statement to check if the key was released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                co_ordX_change = 0

    # Player
    co_ordX += co_ordX_change
    # if statement to limit player movement beyond boundaries
    if co_ordX < 0:
        co_ordX = 0
    elif co_ordX >= 736:
        co_ordX = 736

    # Enemy and multiple enemies
    for i in range(num_of_enemies):
        Enemy_co_ordX[i] += Enemy_cordX_change[i]
        # if statement to limit enemy movement from left to right snf from right to left
        if Enemy_co_ordX[i] < 0:
            Enemy_cordX_change[i] = 4
            # enemy moving down when it touches the left boundary
            Enemy_co_ordY[i] += Enemy_cordY_change[i]
        elif Enemy_co_ordX[i] >= 736:
            Enemy_cordX_change[i] = -4
            # enemy moving down when it touches the right boundary
            Enemy_co_ordY[i] += Enemy_cordY_change[i]

        # collision
        collision = collides(Enemy_co_ordX[i], Enemy_co_ordY[i], Bullet_co_ordX, Bullet_co_ordY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            Bullet_co_ordY = 480
            bullet_state = "ready"
            score_value += 1
            Enemy_co_ordX[i] = random.randint(0, 735)
            Enemy_co_ordY[i] = random.randint(50, 150)

        enemy(Enemy_co_ordX[i], Enemy_co_ordY[i], i)

    # Multiple bullet fire
    if Bullet_co_ordY <= 0:
        Bullet_co_ordY = 480
        bullet_state = "ready"
    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(Bullet_co_ordX, Bullet_co_ordY)
        Bullet_co_ordY -= Bullet_cordY_change

    player(co_ordX, co_ordY)
    show_score(scoreX, scoreY)
    pygame.display.update()
