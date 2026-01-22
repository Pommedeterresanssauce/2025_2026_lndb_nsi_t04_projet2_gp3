import pygame
import pygame, sys
from table import *
from settings import *

class Simulation :
    def __init__(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Poker 2")
        self.clock = pygame.time.Clock()
        
        self.table = Table()

    def run(self) :
        while True :
            self.clock.tick(60)
            events = pygame.event.get()
            for event in events :
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()

            self.table.update()
            pygame.display.update()

if __name__ == "__main__" :
    sim = Simulation()
    sim.run()
