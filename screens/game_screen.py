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

        # Setting some starter variables
        self.mode = args[1]
        self.screen_shake = 0

    def process_event(self, event):
        # Right penguin controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.p2.speed -= 7
            if event.key == pygame.K_l:
                self.p2.speed += 7
            if event.key == pygame.K_o: # o key for power shot
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
            if event.key == pygame.K_w: # w key for power shot
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
            self.screen_shake = 10 # sets shake to 10 frames
        
        # Moving the paddles. Buttons simply control speed and when no key then speed is 0
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
            and 
            self.p1.rect.bottom >= (self.ball.rect.top+self.ball.rect.bottom)/2 >= self.p1.rect.top):
            
            self.ball.bounce("right", power=self.p1_power)
            pygame.mixer.music.load("sounds/boing.mp3")
            pygame.mixer.music.play()

        # Make the ball bounce off right paddle but only the front side of it
        if (self.p2.rect.left+10 >= self.ball.rect.x + self.ball.size[0] >= self.p2.rect.left
            and 
            self.p2.rect.bottom >= (self.ball.rect.top+self.ball.rect.bottom)/2 >= self.p2.rect.top):
            
            self.ball.bounce("left", power=self.p2_power)
            pygame.mixer.music.load("sounds/boing.mp3")
            pygame.mixer.music.play()

        # If the ball goes off limits then start counting down the frames that are shaking
        if self.screen_shake > 0:
            self.screen_shake -= 1
        
        # Start the screen shake for the next 10 frames and randomize the shake direction
        render_offset = [0 , 0]
        if self.screen_shake:
            render_offset[0] = random.randint(0, 8) - 4
            render_offset[1] = random.randint(0, 8) - 4
        
        # Blit the background onto the window
        self.window.blit(self.bg, render_offset)

        # Added features for ranked mode
        if self.mode == "ranked":
            # Display left score
            left_score, left_score_rect = self.text_object("h1", p1_score, (WINDOW_WIDTH/4, WINDOW_HEIGHT/8))
            self.window.blit(left_score, left_score_rect)

            # Display right score
            right_score, right_score_rect = self.text_object("h1", p2_score, (WINDOW_WIDTH/1.34, WINDOW_HEIGHT/8))
            self.window.blit(right_score, right_score_rect)
            
            # Display if player 1 got the point. Screen shake is so that it shakes screen before displaying
            if scorer == "p1" and self.screen_shake == 1:
                self.p1_point, self.p1_point_rect = self.text_object("h1", "Point: Player 1", (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
                self.window.blit(self.p1_point, self.p1_point_rect)
                pygame.display.update()
                pygame.time.wait(3000)
            
            # Display if player 2 won the point. Screen shake is so that it shakes screen before displaying
            elif scorer == "p2" and self.screen_shake == 1:
                self.p2_point, self.p2_point_rect = self.text_object("h1", "Point: Player 2", (WINDOW_WIDTH/2, WINDOW_HEIGHT/2))
                self.window.blit(self.p2_point, self.p2_point_rect)
                pygame.display.update()
                pygame.time.wait(3000)

            # Exit current match once someone hits 10 points
            if p1_score == 10 or p2_score == 10:
                self.running = False

        # Blit the paddles and the ball to screen
        self.paddles.draw(self.window)
        self.window.blit(self.ball.image, self.ball.rect)

        # drawing the center line
        pygame.draw.aaline(self.window, COLOURS["black"], (WINDOW_WIDTH/2, 0), (WINDOW_WIDTH/2, WINDOW_HEIGHT))
        
        #returning scores so that they can be passed into menu screen object later for game over screen
        return p1_score, p2_score
