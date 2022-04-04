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
        score = FONTS[font].render(f"{text}", True, COLOURS[color])
        score_rect = score.get_rect(center=position)
        return score, score_rect

    # Helper method to create button surface and rect that can be accessed by all child classes
    def button_object(self, size, color, position):
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
