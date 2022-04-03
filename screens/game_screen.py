import random
import pygame
import pygame.locals
from .base_screen import Screen
from models import Ball, Paddle
from constants import WINDOW_HEIGHT, WINDOW_WIDTH, FONTS, COLOURS


class GameScreen(Screen):
    """Example class for a Pong game screen"""

    def __init__(self, *args, **kwargs):
        # Call the parent constructor
        super().__init__(*args, **kwargs)

        # Set ice background
        bg = pygame.image.load("imgs/ice.jpg")
        self.bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))

        # Create objects
        self.ball = Ball()
        self.ball.launch()
        self.p1 = Paddle("left")
        self.p1_power = False
        self.p2 = Paddle("right")
        self.p2_power = False
        self.paddles = pygame.sprite.Group()
        self.paddles.add(self.p1, self.p2)

        self.mode = args[1]
        self.screen_shake = 0

    def process_event(self, event):
        # Right penguin controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.p2.speed -= 7
            if event.key == pygame.K_l:
                self.p2.speed += 7
            if event.key == pygame.K_o:
                self.p2_power = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_p:
                self.p2.speed += 7
            if event.key == pygame.K_l:
                self.p2.speed -= 7
            if event.key == pygame.K_o:
                self.p2_power = False

        # Left penguin controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                self.p1.speed -= 7
            if event.key == pygame.K_a:
                self.p1.speed += 7
            if event.key == pygame.K_w:
                self.p1_power = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_q:
                self.p1.speed += 7
            if event.key == pygame.K_a:
                self.p1.speed -= 7
            if event.key == pygame.K_w:
                self.p1_power = False

        

    def process_loop(self):
        # Relaunch ball when it goes off limits
        if self.ball.off_limits:
            self.ball.launch(random.choice(["left", "right"]))
            self.ball.off_limits = False
            self.screen_shake = 10
        
        # Moving the paddles
        self.p1.up()
        self.p1.down()
        self.p2.up()
        self.p2.down()

        # Update the ball position and get scores from return value
        p1_score, p2_score, scorer = self.ball.update()

        # Update the paddles' positions
        self.paddles.update()

        # Make the ball bounce off the left paddle but only the front side of it
        if (self.p1.rect.right-10 <= self.ball.rect.x <= self.p1.rect.right
            and self.p1.rect.bottom >= (self.ball.rect.top+self.ball.rect.bottom)/2 >= self.p1.rect.top):
            self.ball.bounce("right", power=self.p1_power)

            pygame.mixer.music.load("sounds/boing.mp3")
            pygame.mixer.music.play()

        # Make the ball bounce off right paddle but only the front side of it
        if (self.p2.rect.left+10 >= self.ball.rect.x + self.ball.size[0] >= self.p2.rect.left
            and self.p2.rect.bottom >= (self.ball.rect.top+self.ball.rect.bottom)/2 >= self.p2.rect.top):
            
            self.ball.bounce("left", power=self.p2_power)
            pygame.mixer.music.load("sounds/boing.mp3")
            pygame.mixer.music.play()

        if self.screen_shake > 0:
            self.screen_shake -= 1
        
        render_offset = [0 , 0]
        if self.screen_shake:
            render_offset[0] = random.randint(0, 8) - 4
            render_offset[1] = random.randint(0, 8) - 4
        
        self.window.blit(self.bg, render_offset)

        # Added features for ranked mode
        if self.mode == "ranked":
            # Display left score
            left_score = FONTS["h1"].render(f"{p1_score}", True, COLOURS["black"])
            left_score_rect = left_score.get_rect(center=(WINDOW_WIDTH/4, WINDOW_HEIGHT/8))
            self.window.blit(left_score, left_score_rect)

            # Display right score
            right_score = FONTS["h1"].render(f"{p2_score}", True, COLOURS["black"])
            right_score_rect = right_score.get_rect(center=(WINDOW_WIDTH/1.34, WINDOW_HEIGHT/8))
            self.window.blit(right_score, right_score_rect)
            
            # Display scorer text for p1
            if scorer == "p1" and self.screen_shake == 1:
                self.p1_point = FONTS["h1"].render(f"Point: Player 1", True, COLOURS["black"])
                self.p1_point_rect = self.p1_point.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
                self.window.blit(self.p1_point, self.p1_point_rect)
                pygame.display.update()
                pygame.time.wait(3000)
            
            # Display scorer text for p2
            elif scorer == "p2" and self.screen_shake == 1:
                self.p2_point = FONTS["h1"].render(f"Point: Player 2", True, COLOURS["black"])
                self.p2_point_rect = self.p2_point.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
                self.window.blit(self.p2_point, self.p2_point_rect)
                pygame.display.update()
                pygame.time.wait(3000)

            # Exit current match once someone hits 10
            if p1_score == 10 or p2_score == 10:
                self.running = False

        # Blit everything
        self.paddles.draw(self.window)
        self.window.blit(self.ball.image, self.ball.rect)

        # drawing the center line
        pygame.draw.aaline(self.window, COLOURS["black"], (WINDOW_WIDTH/2, 0), (WINDOW_WIDTH/2, WINDOW_HEIGHT))
        

        return p1_score, p2_score
