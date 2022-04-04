# Author: Lucas Angelozzi
# Date: 03/28/22
# Purpose: Parent screen class that all other screens inherit from

# Imports
import pygame, sys
from constants import FONTS, COLOURS

class Screen:
    """
    Use the Screen class as a parent class for your own screens
    """

    def __init__(self, window, fps=60, bgcolor=None, **kwargs):
        """Constructor must receive the window"""
        self.window = window
        self.running = True
        self.fps = 60
        self.bgcolor = bgcolor
        if not self.bgcolor:
            self.bgcolor = (0, 0, 0)


    # Helper method to create text surface and rect that can be accessed by all child classes (aka the other screens)
    def text_object(self, font, text, position, color="black"):
        """Create a pygame text surface and rectangle

        Args:
            font (str): either h1 or h2
            text (str): the string that will be displayed on the text surface
            position (tuple): (x, y) coordinates
            color (str, optional): a colour from constants.COLOURS. Defaults to "black".

        Returns:
            tuple: the text surface object and a rectangle for the surface
        """
        
        words = FONTS[font].render(f"{text}", True, COLOURS[color])
        words_rect = words.get_rect(center=position)
        return words, words_rect


    # Helper method to create button surface and rect that can be accessed by all child classes
    def button_object(self, size, color, position):
        """Create a pygame surface that acts as a button as well as a rectangle for it

        Args:
            size (tuple): (x, y)
            color (str): a colour from constants.COLOURS
            position (tuple): (x, y) coordinates

        Returns:
            tuple: the button surface and a rectangle for the button
        """
        
        button = pygame.Surface(size)
        button.fill(COLOURS[color])
        button_rect = button.get_rect(center=position)

        return button, button_rect
        

    def loop(self):
        """Main screen loop: deals with Pygame events"""

        clock = pygame.time.Clock()

        while self.running:
            clock.tick(self.fps)

            # Fill the screen
            self.window.fill(self.bgcolor)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.running = False
                    result = False
                else:
                    # Override this method to customize your screens!
                    self.process_event(event)

            # Override this method to customize what happens in your screens!
            result = self.process_loop()

            # Update display
            pygame.display.update()

        return result


    def process_event(self, event):
        """This method should be overriden by your child classes"""
        print("YOU SHOULD IMPLEMENT 'process_event' IN YOUR SCREEN SUBCLASS!")


    def process_loop(self):
        """This method should be overriden by your child classes"""
        raise NotImplementedError("YOU MUST IMPLEMENT 'process_loop' IN YOUR SUBCLASS!")
