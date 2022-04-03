# Author: Lucas Angelozzi
# Date: 03/28/22
# Purpose: Menu screen object

# Imports
from enum import Flag
import pygame
from .base_screen import Screen
from constants import COLOURS, FONTS, WINDOW_HEIGHT, WINDOW_WIDTH

class MenuScreen(Screen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Importing background image and sizing it to window
        bg = pygame.image.load("imgs/welcomebg.jpg")
        self.bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Setting arguments to variables
        self.version = kwargs["version"]
        self.left_button_color = kwargs["lbc"]
        self.left_button_word = kwargs["lbw"]
        self.right_button_color = kwargs["rbc"]
        self.right_button_word = kwargs["rbw"]
        
        # Title and scores for the gameover screen
        if self.version == "gameover":
            self.left_score = kwargs["left_score"]
            self.right_score = kwargs["right_score"]
            
            # Creating title surface and its rectangle
            self.title = FONTS["h1"].render(f"Game Over", True, COLOURS["black"])
            self.title_rect = self.title.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/8))

            # Display left score
            left_score = FONTS["h1"].render(f"{self.left_score}", True, COLOURS["black"])
            left_score_rect = left_score.get_rect(center=(WINDOW_WIDTH/8, WINDOW_HEIGHT/8))
            self.bg.blit(left_score, left_score_rect)

            # Display right score
            right_score = FONTS["h1"].render(f"{self.right_score}", True, COLOURS["black"])
            right_score_rect = right_score.get_rect(center=(WINDOW_WIDTH/1.15, WINDOW_HEIGHT/8))
            self.bg.blit(right_score, right_score_rect)

        # Title for the normal menu screen
        if self.version == "welcome" or self.version == "finish":
            # Creating title surface and its rectangle
            self.title = FONTS["h1"].render(f"Penguin Pong", True, COLOURS["black"])
            self.title_rect = self.title.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/8))
            
        # Creating surfaces for practice button and text
        self.left_button = pygame.Surface((WINDOW_WIDTH/6, WINDOW_HEIGHT/8))
        self.left_button.fill(COLOURS[self.left_button_color])
        self.left_button_rect = self.left_button.get_rect(center=(WINDOW_WIDTH/3, WINDOW_HEIGHT/2))
        self.left_button_words = FONTS["h2"].render(self.left_button_word, False, COLOURS["black"])
        self.left_button_words_rect = self.left_button_words.get_rect(center=(self.left_button.get_width()/2, self.left_button.get_height()/2))

        # Creating surfaces for ranked button and text
        self.right_button = pygame.Surface((WINDOW_WIDTH/6, WINDOW_HEIGHT/8))
        self.right_button.fill(COLOURS[self.right_button_color])
        self.right_button_rect = self.right_button.get_rect(center=(WINDOW_WIDTH/1.5, WINDOW_HEIGHT/2))
        self.right_button_words = FONTS["h2"].render(self.right_button_word, False, COLOURS["black"])
        self.right_button_words_rect = self.right_button_words.get_rect(center=(self.right_button.get_width()/2, self.right_button.get_height()/2))

        # Inizialiting game mode as none
        self.game_mode = None
        self.replay = None

    # Helper functions
    def change_button_colour(self, button, color):
        if button == "right":
            self.right_button.fill(color)
            self.right_button_words = FONTS["h2"].render(self.right_button_word, False, COLOURS["black"])
            self.window.blit(self.right_button, self.right_button_rect)
            self.right_button.blit(self.right_button_words, self.right_button_words_rect)
        elif button == "left":
            self.left_button.fill(color)
            self.practice_words = FONTS["h2"].render(self.left_button_word, False, COLOURS["black"])
            self.window.blit(self.left_button, self.left_button_rect)
            self.left_button.blit(self.left_button_words, self.left_button_words_rect)
        

    def process_event(self, event):
        # Checking if the mouse is clicked inside the button and setting game mode based off which button is clicked
        if self.right_button_rect.collidepoint(pygame.mouse.get_pos()):
            self.change_button_colour("right", COLOURS["white"])
        elif not self.right_button_rect.collidepoint(pygame.mouse.get_pos()):
            self.change_button_colour("right", self.right_button_color)

        #change practice button colour on hover
        if self.left_button_rect.collidepoint(pygame.mouse.get_pos()):
            self.change_button_colour("left", COLOURS["white"])
        elif not self.left_button_rect.collidepoint(pygame.mouse.get_pos()):
            self.change_button_colour("left", self.left_button_color)
        
        # Different functions for buttons based on what version of the menu screen
        if self.version == "welcome":
            # Checking if the mouse is clicked inside the button and setting game mode based off which button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN and self.left_button_rect.collidepoint(event.pos):
                self.game_mode = "practice"
            elif event.type == pygame.MOUSEBUTTONDOWN and self.right_button_rect.collidepoint(event.pos):
                self.game_mode = "ranked"
        
        elif self.version == "finish" or self.version == "gameover":
            if event.type == pygame.MOUSEBUTTONDOWN and self.left_button_rect.collidepoint(event.pos):
                self.replay = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.right_button_rect.collidepoint(event.pos):
                self.replay = True
                

    def process_loop(self):
        # blit the background image
        self.window.blit(self.bg, (0,0))
        
        # set the title to the center top of screen
        self.window.blit(self.title, self.title_rect)
        
        # blitting button in the window and text in the button
        self.window.blit(self.left_button, self.left_button_rect)
        self.left_button.blit(self.left_button_words, self.left_button_words_rect)

        # blitting button in the window and text in the button
        self.window.blit(self.right_button, self.right_button_rect)
        self.right_button.blit(self.right_button_words, self.right_button_words_rect)

        # returning game mode if its not none
        if self.game_mode:
            self.running = False
            return self.game_mode
        
        if self.replay != None:
            self.running = False
            return self.replay