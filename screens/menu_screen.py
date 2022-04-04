# Author: Lucas Angelozzi
# Date: 03/28/22
# Purpose: Menu screen object

# Imports
import pygame
from .base_screen import Screen
from constants import COLOURS, FONTS, WINDOW_HEIGHT, WINDOW_WIDTH

class MenuScreen(Screen):
    '''Class for a Menu Screen object'''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Importing background image and sizing it to window
        bg = pygame.image.load("imgs/welcomebg.jpg")
        self.bg = pygame.transform.scale(bg, (WINDOW_WIDTH, WINDOW_HEIGHT))
        
        # Setting arguments from kwargs to variables
        self.version = kwargs["version"]
        self.left_button_color = kwargs["lbc"]
        self.left_button_word = kwargs["lbw"]
        self.right_button_color = kwargs["rbc"]
        self.right_button_word = kwargs["rbw"]
        
        # Title and scores for the gameover screen
        if self.version == "gameover":
            # Getting the scores from kwargs that was returned from game_screen
            self.left_score = kwargs["left_score"]
            self.right_score = kwargs["right_score"]
            
            # Creating title text surface and its rectangle
            self.title, self.title_rect = self.text_object("h1", "Game Over", (WINDOW_WIDTH/2, WINDOW_HEIGHT/8))

            # Create and blit left score
            left_score, left_score_rect = self.text_object("h1", self.left_score, (WINDOW_WIDTH/8, WINDOW_HEIGHT/8))
            self.bg.blit(left_score, left_score_rect)

            # Create and blit right score
            right_score, right_score_rect = self.text_object("h1", self.right_score, (WINDOW_WIDTH/1.15, WINDOW_HEIGHT/8))
            self.bg.blit(right_score, right_score_rect)

        # Title for the normal menu screen
        if self.version == "welcome" or self.version == "finish":
            # Creating title text surface and its rectangle
            self.title, self.title_rect = self.text_object("h1", "Penguin Pong", (WINDOW_WIDTH/2, WINDOW_HEIGHT/8))
            
        # Creating surface, rectangles and text for left button
        self.left_button, self.left_button_rect = self.button_object((WINDOW_WIDTH/6, WINDOW_HEIGHT/8), self.left_button_color, (WINDOW_WIDTH/3, WINDOW_HEIGHT/2))
        self.left_button_words, self.left_button_words_rect = self.text_object("h2", self.left_button_word, (self.left_button.get_width()/2, self.left_button.get_height()/2))
       
        # Creating surface, rectangles and text for right button
        self.right_button, self.right_button_rect = self.button_object((WINDOW_WIDTH/6, WINDOW_HEIGHT/8), self.right_button_color, (WINDOW_WIDTH/1.5, WINDOW_HEIGHT/2))
        self.right_button_words, self.right_button_words_rect = self.text_object("h2", self.right_button_word, (self.right_button.get_width()/2, self.right_button.get_height()/2))
        
        # Inizialiting game mode and replay as none
        self.game_mode = None
        self.replay = None

    # A helper function to reduce some repetetive code
    def change_button_colour(self, button, color):
        """Change the colour of a button

        Args:
            button (pygame.Surface): the button surface you would like to change the colour of
            color (rgb): a colour from constants.COLOURS or an rgb value
        """
        
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
        """Processes any pygame events that occur during gameplay such as mouse presses

        Args:
            event (pygame.event): a pygame event that occurs
        """
        
        # Different functions for buttons based on what version of the menu screen
        if self.version == "welcome":
            # Checking if the mouse is clicked inside the button and setting game mode based off which button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN and self.left_button_rect.collidepoint(event.pos):
                self.game_mode = "practice"
            elif event.type == pygame.MOUSEBUTTONDOWN and self.right_button_rect.collidepoint(event.pos):
                self.game_mode = "ranked"
        
        elif self.version == "finish" or self.version == "gameover":
            # Checking button clicks and setting replay variable accordingly
            if event.type == pygame.MOUSEBUTTONDOWN and self.left_button_rect.collidepoint(event.pos):
                self.replay = False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.right_button_rect.collidepoint(event.pos):
                self.replay = True
                

    def process_loop(self):
        """The loop for any menu screens that are being shown 

        Returns:
            bool or str: will either return the game mode if the player is going to start a match
                            or it will return a boolean about whether to replay the game.
        """
        
        # Change right button colour on hover
        if self.right_button_rect.collidepoint(pygame.mouse.get_pos()):
            self.change_button_colour("right", COLOURS["white"])
        elif not self.right_button_rect.collidepoint(pygame.mouse.get_pos()):
            self.change_button_colour("right", self.right_button_color)

        # Change left button colour on hover
        if self.left_button_rect.collidepoint(pygame.mouse.get_pos()):
            self.change_button_colour("left", COLOURS["white"])
        elif not self.left_button_rect.collidepoint(pygame.mouse.get_pos()):
            self.change_button_colour("left", self.left_button_color)

        # Blit the background image
        self.window.blit(self.bg, (0,0))
        
        # Set the title to the center top of screen
        self.window.blit(self.title, self.title_rect)
        
        # Blitting button in the window and text in the button
        self.window.blit(self.left_button, self.left_button_rect)
        self.left_button.blit(self.left_button_words, self.left_button_words_rect)

        # Blitting button in the window and text in the button
        self.window.blit(self.right_button, self.right_button_rect)
        self.right_button.blit(self.right_button_words, self.right_button_words_rect)

        # returning game mode if its not none
        if self.game_mode:
            self.running = False
            return self.game_mode
        
        # returning if the player chose to replay or not
        if self.replay != None:
            self.running = False
            return self.replay