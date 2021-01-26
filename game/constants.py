import pygame
import os

# GAME SETTINGS
WIN_WIDTH = 1920
WIN_HEIGHT = 1080
FPS = 30
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
WIN_MENU = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

# COLORS
RED = pygame.Color(255, 0, 0)
BLUE = pygame.Color(0, 0, 255)
ORANGE = pygame.Color(255, 127, 0)
YELLOW = pygame.Color(255, 255, 0)
PINK = pygame.Color(255, 0, 255)
WHITE = pygame.Color(255, 255, 255)
CYAN = pygame.Color(0, 255, 255)
LIME = pygame.Color(0, 255, 0)
ROAD = pygame.Color(75, 75, 75)
GRASS = pygame.Color(34, 177, 76)
BLACK = pygame.Color(0, 0, 0)
START_END = (WHITE, BLACK)

# IMAGES
BACKGROUND = pygame.image.load(os.path.join('images', 'background.bmp'))
path = os.path.join('images', 'background_menu.bmp')
BACKGROUND_MENU = pygame.image.load(path)
CARS = [
    (pygame.image.load(os.path.join('images', 'red_formula.png')), RED),
    (pygame.image.load(os.path.join('images', 'blue_formula.png')), BLUE),
    (pygame.image.load(os.path.join('images', 'orange_formula.png')), ORANGE),
    (pygame.image.load(os.path.join('images', 'yellow_formula.png')), YELLOW),
    (pygame.image.load(os.path.join('images', 'pink_formula.png')), PINK),
    (pygame.image.load(os.path.join('images', 'white_formula.png')), WHITE),
    (pygame.image.load(os.path.join('images', 'cyan_formula.png')), CYAN),
    (pygame.image.load(os.path.join('images', 'lime_formula.png')), LIME)
]

# CAR SETTINGS
SPEED = 10.0
ROTATION = 8.0

# CHECKPOINT COLORS
CHECKPOINTS = [
    (pygame.Color(0, 0, 255),),
    (pygame.Color(1, 0, 255),),
    (pygame.Color(2, 0, 255),),
    (pygame.Color(3, 0, 255),),
    (pygame.Color(4, 0, 255),),
    (pygame.Color(5, 0, 255),),
    START_END
]
