import pygame
from constants import WINDOW_HEIGHT, WINDOW_WIDTH
from screens.game_screen import GameScreen
from screens.menu_screen import MenuScreen


def main():
    pygame.init()
    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    replay = True

    while replay == True:
        # Render the welcome page and set the mode based on users decision
        welcome = MenuScreen(
            window, 
            version="welcome", 
            lbc="green",
            lbw="Practice", 
            rbc="orange",
            rbw="Ranked"
        )
        mode = welcome.loop() #this is what starts the actual game

        # Start game in practice mode or ranked mode
        if mode == "practice":
            print("Practice mode")
            game = GameScreen(window, "practice")
            game.loop()

            # Render Menu Screen as End Game screen
            end_game = MenuScreen(
                window, 
                version="finish",
                lbc="red",
                lbw="Quit", 
                rbc="blue",
                rbw="Replay"
            )
            
            replay = end_game.loop()

        elif mode == "ranked":
            print("Playing ranked")
            game = GameScreen(window, "ranked")
            p1_score, p2_score = game.loop()
            
            # Render Menu Screen as a Game Over screen
            game_over = MenuScreen(
                window,
                version="gameover",
                lbc="red",
                lbw="Quit", 
                rbc="blue",
                rbw="Replay"
            )
            
            replay = game_over.loop()


if __name__ == "__main__":
    main()
