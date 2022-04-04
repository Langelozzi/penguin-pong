# Author: Lucas Angelozzi
# Date: 03/28/22
# Purpose: Paddle class for pong

# Imports
import pygame
from constants import LIMITS, WINDOW_WIDTH, WINDOW_HEIGHT

class Paddle(pygame.sprite.Sprite):
    """Paddle class"""

    def __init__(self, position):
        super().__init__()

        # Default size
        self.size = (WINDOW_WIDTH/20, int(WINDOW_HEIGHT/5.6))

        # Default speed and velocity
        self.speed = 0

        # Load images, set rectangle and starting positions
        # Left penguin
        if position == "left":
            image = pygame.image.load("imgs/penguin_left.png")
            self.image = pygame.transform.scale(image, self.size)
            self.rect = self.image.get_rect()
            self.rect.x = LIMITS["left"]
        # Right Penguin
        elif position == "right":
            image = pygame.image.load("imgs/penguin_right.png")
            self.image = pygame.transform.scale(image, self.size)
            self.rect = self.image.get_rect()
            self.rect.x = LIMITS["right"] - self.size[0]
            
        # Set both penguins in the vertical middle
        self.rect.y = LIMITS["down"] // 2

    def refresh_rect(self, color):
        """Updates the sprite / rect based on self.size"""
        self.image = pygame.Surface(self.size)
        self.image.fill(color)
        self.rect = self.image.get_rect()

    def up(self):
        """Move the paddle up"""
        self.rect.y += self.speed

        if self.rect.y < LIMITS["up"]:
            self.rect.y = LIMITS["up"]

    def down(self):
        """Move the paddle down"""
        self.rect.y += self.speed

        if self.rect.y > LIMITS["down"] - self.size[1]:
            self.rect.y = LIMITS["down"] - self.size[1]
