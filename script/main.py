import pygame
import pygame, sys
from table import *
from settings import *
from menu import *

class Game :
    def __init__(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF, vsync=1)
        pygame.display.set_caption("Poker 2")
        self.clock = pygame.time.Clock()
        
        self.menu = Menu(self.screen)
        self.table = Table()

    def run(self) :
        while True :
            dt = self.clock.tick(0) / 1000.0  # secondes
            events = pygame.event.get()
            for event in events :
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()

            if self.menu.is_open :
                self.menu.update()
            else :
                self.table.update(dt)
            pygame.display.update()

if __name__ == "__main__" :
    game = Game()
    game.run()
