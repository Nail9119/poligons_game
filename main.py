import sys
import pygame
from game import Game
from global_vars import Global
from menu import MainMenu, GameOverMenu

if __name__ == "__main__":
    menu = MainMenu()
    result = menu.loop()
    while result != "Exit":
        if result == "Play":
            game = Game()
            result = game.loop()
        elif result == "Game over":
            game_over = GameOverMenu()
            result = game_over.loop()
        elif result == "Restart":
            game = Game()
            result = game.loop()
        elif result == "Menu":
            menu = MainMenu()
            result = menu.loop()
        Global().clear()
    pygame.quit()
    sys.exit()
