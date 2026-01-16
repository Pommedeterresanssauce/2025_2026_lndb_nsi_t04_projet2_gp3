import pygame
import pygame, sys

class Simulation :
    def __init__(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((1500, 850))
        pygame.display.set_caption("Poker 2")
        self.clock = pygame.time.Clock()

    def run(self) :
        while True :
            self.clock.tick(60)
            events = pygame.event.get()
            for event in events :
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

if __name__ == "__main__" :
    sim = Simulation()
    sim.run()
