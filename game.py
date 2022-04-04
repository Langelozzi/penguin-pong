import pygame
from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from screens.game_screen import GameScreen
from screens.menu_screen import MenuScreen


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    replay = True

    while replay == True:
        # Create welcome page object
        welcome = MenuScreen(
            window, 
            version="welcome", 
            lbc="green",
            lbw="Practice", 
            rbc="orange",
            rbw="Ranked"
        )
        
        # Start the welcome page loop and get mode as return value
        mode = welcome.loop() 

        # Start game in practice mode or ranked mode
        if mode == "practice":
            # Create game screen object as practice mode and start the loop
            game = GameScreen(window, "practice")
            game.loop()

            # Create and Render Menu Screen as End Game screen
            end_game = MenuScreen(
                window, 
                version="finish",
                lbc="red",
                lbw="Quit", 
                rbc="blue",
                rbw="Replay"
            )
            # Return value is true if user selected to replay
            replay = end_game.loop()

        elif mode == "ranked":
            # Create game screen object as ranked mode and start the loop
            game = GameScreen(window, "ranked")
            p1_score, p2_score = game.loop() # Getting scores as return values so they can be passed into the game_over screen
            
            # Render Menu Screen as a Game Over screen and start loop
            game_over = MenuScreen(
                window,
                version="gameover",
                lbc="red",
                lbw="Quit", 
                rbc="blue",
                rbw="Replay",
                left_score=p1_score,
                right_score=p2_score
            )
            replay = game_over.loop()


if __name__ == "__main__":
    main()
