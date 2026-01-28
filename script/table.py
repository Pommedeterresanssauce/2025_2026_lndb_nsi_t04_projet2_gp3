import pygame
from player import *
from support import import_folder


class Table:
    def __init__(self):
        self.player = Player()
        self.screen = pygame.display.get_surface()
        self.screen_width, self.screen_height = self.screen.get_size()

        # --- PHASE ---
        self.active_turn = 'shuffle'
        self.shuffle_done = False 
        self.distribution_done = False
        
        # --- DECK COMPOSITION ---
        self.deck_cards = [
            
        ]

        # --- IMAGES ---
        self.table_image = pygame.image.load(
            'graphics/table_de_jeu/table_verte.png'
        ).convert()
        self.table_image = pygame.transform.scale(
            self.table_image, (self.screen_width, self.screen_height)
        )

        self.white_rectangle_image = pygame.image.load(
            'graphics/table_de_jeu/rectangle_blanc.png'
        ).convert_alpha()
        self.white_rectangle_image = pygame.transform.scale(
            self.white_rectangle_image, (140, 192)
        )

        self.deck_image = pygame.image.load(
            'graphics/table_de_jeu/deck.png'
        ).convert_alpha()
        self.deck_image = pygame.transform.scale(
            self.deck_image, (140, 252)
        )

        # --- ANIMATIONS ---
        self.animations = {
            'shuffle': import_folder('graphics/animations/shuffle')
        }

        self.actual_animations = []

        self.animations_infos = {
            'shuffle': {
                'pos': (625, 102),
                'index': 0
            }
        }


    def turn_action(self) :
        if self.active_turn == 'distribution' : 
            pass
        


    def update_turn_phase(self):
        # lancer l'animation UNE SEULE FOIS
        if self.active_turn == 'shuffle' and not self.shuffle_done:
            if 'shuffle' not in self.actual_animations:
                self.animations_infos['shuffle']['index'] = 0
                self.actual_animations.append('shuffle')

        # quand le mélange est terminé
        if self.active_turn == 'shuffle' and self.shuffle_done :
            self.active_turn = 'distribution'
            
        # quand la distribution est terminée
        if self.active_turn == 'distribution' and self.distribution_done :
            self.active_turn = 'player1'
            
            
        
    def update_and_draw_animations(self, dt):
        for animation in self.actual_animations.copy():
            self.animations_infos[animation]['index'] += dt * 11
            index = int(self.animations_infos[animation]['index'])

            if index >= len(self.animations[animation]):
                self.actual_animations.remove(animation)
                if animation == 'shuffle':
                    self.shuffle_done = True
            else:
                pos = self.animations_infos[animation]['pos']
                self.screen.blit(self.animations[animation][index], pos)


    def draw(self):
        # table
        self.screen.blit(self.table_image, (0, 0))

        # rectangles blancs
        self.screen.blit(self.white_rectangle_image, (700, 420))
        self.screen.blit(self.white_rectangle_image, (1070, 420))
        self.screen.blit(self.white_rectangle_image, (885, 420))
        self.screen.blit(self.white_rectangle_image, (792.5, 657))
        self.screen.blit(self.white_rectangle_image, (977.5, 657))


            
    def draw_cards(self) :
        # deck visible seulement après le mélange
        if self.shuffle_done:
            self.screen.blit(self.deck_image, (885, 150))


    def update(self, dt):
        self.update_turn_phase()
        self.turn_action()
        self.draw()
        self.update_and_draw_animations(dt)
        self.draw_cards()
        self.player.draw()


    
    