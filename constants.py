import pygame

WINDOW_HEIGHT = 850
WINDOW_WIDTH = 1200

LIMITS = {
    "up": 0,
    "down": WINDOW_HEIGHT,
    "left": 0,
    "right": WINDOW_WIDTH,
}

pygame.font.init()
FONTS = {
    "h1": pygame.font.SysFont('arial', int((WINDOW_HEIGHT + WINDOW_WIDTH)/15)),
    "h2": pygame.font.SysFont('arial', int((WINDOW_HEIGHT + WINDOW_WIDTH)/40), italic=True)
}

COLOURS = {
    "red": (255, 0, 0),
    "orange": (255, 127, 0),
    "yellow": (255, 255, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "purple": (148, 0, 211),
    "black": (0, 0, 0),
    "white": (255, 255, 255)
}
