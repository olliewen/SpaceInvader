import pygame
import os
from time import sleep

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

# Choose theme

theme1 = pygame.image.load("theme1.png")
theme2 = pygame.image.load("theme2.png")
theme1_x = 0
theme1_y = 0
theme2_x = theme1_x + 450
theme2_y = theme1_y

screen.blit(theme1, (theme1_x, theme1_y))
screen.blit(theme2, (theme2_x, theme2_y))
pygame.display.update()

running = True
while running:
    # background image appear on the top left corner
    # If window is closed, kill the program. This prevents the window to hang in a while loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # If keystroke is pressed, check whether its right or left
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_q:
            running = False
        if event.key == pygame.K_r:
            continue
        if event.key == pygame.K_1:
            running = False
            os.system('python3 theme1.py')

        if event.key == pygame.K_2:
            running = False
            os.system('python3 theme2.py')


