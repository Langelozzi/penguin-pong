import random
import pygame
from constants import LIMITS, COLOURS, WINDOW_HEIGHT, WINDOW_WIDTH


class Ball(pygame.sprite.Sprite):
    """
    Model of a (bouncing) ball.
    If gravity is True, the ball will obey to gravity (aka fall down).
    """

    def __init__(self, gravity=False, size=20):
        """Constructor"""
        super().__init__()

        self.size = size
        # The ball is a circle
        image = pygame.image.load("imgs/fish.png")
        self.image = pygame.transform.scale(image, (WINDOW_WIDTH/48 ,WINDOW_HEIGHT/34))

        self.rect = self.image.get_rect()

        # Spawn in the middle of the screen
        self.rect.x = LIMITS["right"] // 2
        self.rect.y = LIMITS["down"] // 2

        self.p1_score = 0
        self.p2_score = 0
        self.scorer = None

        # Start without moving
        self.hspeed = 0
        self.vspeed = 0

        # Gravity and off limits booleans
        self.respect_gravity = gravity
        self.off_limits = False

    def launch(self, direction=None, hspeed=2.5, vspeed=-5):
        """Launches the ball up in the air"""
        self.hspeed = hspeed
        if direction == "left":
            self.hspeed = -self.hspeed
        self.vspeed = vspeed

    def update(self):
        """Convenience method"""

        # The vertical speed decreases over time when subject to gravity
        if self.respect_gravity:
            self.vspeed += 1

        # If the ball is not off limits, make it move
        if not self.off_limits:
            self.rect.x += self.hspeed
            self.rect.y += self.vspeed

        # Check the ball did not go off limits
        if self.rect.x > LIMITS["right"] - self.size:
            self.rect.x = LIMITS["right"] // 2
            self.rect.y = LIMITS["down"] // 2
            self.off_limits = True
            self.p1_score += 1
            self.scorer = "p1"

            pygame.mixer.music.load("sounds/oof.mp3")
            pygame.mixer.music.play()
        
        elif self.rect.x < LIMITS["left"]:
            self.rect.x = LIMITS["right"] // 2
            self.rect.y = LIMITS["down"] // 2
            self.off_limits = True
            self.p2_score += 1
            self.scorer = "p2"

            pygame.mixer.music.load("sounds/oof.mp3")
            pygame.mixer.music.play()

        else:
            self.scorer = None

        # Check whether we need to bounce the ball off the wall
        if self.rect.y > LIMITS["down"] - self.size:
            self.rect.y = LIMITS["down"] - self.size
            self.bounce("vertical")

            pygame.mixer.music.load("sounds/bonk.mp3")
            pygame.mixer.music.play()

        elif self.rect.y < LIMITS["up"]:
            self.rect.y = LIMITS["up"]
            self.bounce("vertical")

            pygame.mixer.music.load("sounds/bonk.mp3")
            pygame.mixer.music.play()

        # Prevent the ball from bouncing for ever when on the ground
        if (
            self.respect_gravity
            and -1 < self.vspeed < 1
            and self.rect.y >= LIMITS["down"] - (self.size + 5)
        ):
            self.vspeed = 0

        return self.p1_score, self.p2_score, self.scorer

    def bounce(self, direction=None, power=False):
        """Bounce the ball"""

        # Horizontal bounces 
        if direction in ("right", "left", "horizontal"):
            self.hspeed = -self.hspeed*(random.choice([1.0, 1.1, 1.2, 1.3, 1.4, 1.5]))

        # Vertical bounces 
        if direction in ("up", "down", "vertical"):
            self.vspeed = -self.vspeed*(random.choice([1.0, 1.1]))

        # Power bounce: increase the speed of the ball
        if power:
            self.hspeed *= 3.3
            self.vspeed *= 1.1
