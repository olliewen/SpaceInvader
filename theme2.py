import pygame
import random
import math
import os
from time import sleep
from pygame import mixer

# setting window position
x = 500
y = 250
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x, y)

# Game loop
# def runGame():
# Initialize pygame
pygame.init()

# Setting the size of the window
screen = pygame.display.set_mode((900, 675))

# Caption and icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("alien.png")
pygame.display.set_icon(icon)

# Splash screen
splash = pygame.image.load("splash.png").convert()
screen.blit(splash, [0, 0])
pygame.display.update()
sleep(2)

# background color
background_color = (128, 128, 128)

# Background music
mixer.music.load("background.wav")
mixer.music.play(-1)

# Player initial position
playerImg = pygame.image.load("player2.png")


def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = random.randint(5, 20)

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load("enemy2.png"))
    enemyX.append(random.randint(10, 860))
    enemyY.append(random.randint(10, 150))
    # enemy speed
    enemyX_change.append(5)
    enemyY_change.append(40)

# Bullet
# ready - you can't see bullet on the screen
# fire = the bullet is currently moving
bulletImg = pygame.image.load("bullet2.png")
bulletX = 0
bulletY = 480

# bullet speed
bulletY_change = 10
bullet_state = "ready"

# Score

score_font = pygame.font.Font("Stars Fighters.ttf", 15)
# score board coordinates
scoreX = 10
scoreY = 10

# Game over text
game_over_font = pygame.font.Font("Stars Fighters.ttf", 32)


def show_score(x, y):
    score = score_font.render("Score: " + str(score_value), True, (50, 50, 50))
    screen.blit(score, (x, y))


def game_over_text():
    game_over = game_over_font.render("GAME OVER", True, (50, 50, 50))
    screen.blit(game_over, (230, 230))
    game_over_voice = mixer.Sound("game over.wav")
    game_over_voice.play(0, 0)
    restart = game_over_font.render("RESTART? (r/q)", True, (50, 50, 50))
    screen.blit(restart, (150, 330))


def enemy(x, y, i):
    assert isinstance(screen, object)
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 9, y - 25))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    if distance < 27:
        return True
    else:
        return False


def crashEnemy(enemyX, enemyY, playerX, playerY):
    player_to_enemy = math.sqrt((enemyX - playerX) ** 2 + (enemyY - playerY) ** 2)
    if player_to_enemy < 27:
        return True
    else:
        return False


score_value = 0
playerX = 430
playerY = 630
playerX_change = 0
playerY_change = 0
running = True
while running:
    screen.fill(background_color)
    # background image appear on the top left corner
    # If window is closed, kill the program. This prevents the window to hang in a while loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # If keystroke is pressed, check whether its right or left
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            playerX_change = -1
        if event.key == pygame.K_RIGHT:
            playerX_change = 1
        if event.key == pygame.K_UP:
            playerY_change = -1
        if event.key == pygame.K_DOWN:
            playerY_change = 1
        if event.key == pygame.K_SPACE:
            if bullet_state == "ready":
                bullet_Sound = mixer.Sound("laser.wav")
                bullet_Sound.play()
                # get current x and y coordinates of the spaceship
                # bullet will continue to use the x coordinate when the spaceship moves
                bulletX = playerX
                bulletY = playerY
                fire_bullet(bulletX, bulletY)
        if event.key == pygame.K_q:
            running = False

        if event.key == pygame.K_r:
            running = False
            os.system("python3 theme2.py")


    # stop continuous movement when releasing arrow keys
    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            playerX_change = 0
        if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            playerY_change = 0

    playerX += playerX_change
    playerY += playerY_change

    # Setting boundary for player
    if playerX <= 10:
        playerX = 10
    elif playerX >= 860:
        playerX = 860

    if playerY <= 10:
        playerY = 10
    elif playerY >= 630:
        playerY = 630

    # enemy movement
    # using [i] for all enemy coordinates so that the for loop knows which enemy to target
    for i in range(num_of_enemies):

        enemyX[i] += enemyX_change[i]

        # Setting boundary for enemies
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 860:
            enemyX_change[i] = -0.5
            enemyY[i] += enemyY_change[i]

        if enemyY[i] <= 10:
            enemyY_change[i] = 0.5
        elif enemyY[i] >= 200:
            enemyY_change[i] = -0.5

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        crash = crashEnemy(enemyX[i], enemyY[i], playerX, playerY)

        # if the bullet collides with the enemy, change the reset the bullet position and add a score of 5
        if collision:
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 5

            enemyX[i] = random.randint(10, 860)
            enemyY[i] = random.randint(10, 150)
            # comment this out if want to respawn enemy after hit
            num_of_enemies -= 1

        if crash:
            num_of_enemies = 0
            game_over_text()

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    # if the bullet is not in "fire" state the bullet will not appear on the screen
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if num_of_enemies == 0:
        game_over_text()

    player(playerX, playerY)
    show_score(scoreX, scoreY)
    pygame.display.update()

# runGame()
