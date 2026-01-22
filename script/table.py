import pygame
from player import *
from support import import_folder

class Table :
    def __init__(self) :
        self.player = Player()
        self.screen = pygame.display.get_surface()
        self.screen_width, self.screen_height = self.screen.get_size()
        
        # action in progress
        self.active_turn = 'shuffle'
        
        # images
        self.table_image = pygame.image.load('graphics/table_de_jeu/table_verte.png')
        self.table_image = pygame.transform.scale(self.table_image, (self.screen_width, self.screen_height))
        self.white_rectangle_image = pygame.image.load('graphics/table_de_jeu/rectangle_blanc.png')
        self.white_rectangle_image = pygame.transform.scale(self.white_rectangle_image, (140, 192))
        self.deck_image = pygame.image.load('graphics/table_de_jeu/deck.png')
        self.deck_image = pygame.transform.scale(self.deck_image, (140, 252))
        
        # animations
        self.animations = {
            'shuffle' : [],
        }
        for animation in self.animations.keys() :
            full_path = 'graphics/table_de_jeu/' + animation
            self.animations[animation] = import_folder(full_path)
    
    
    def update_turn(self) :
        pass
    
    
    def draw(self) :
        # affchage de la table
        self.screen.blit(self.table_image, (0, 0))
        # affichage des rectangle blanc
        self.screen.blit(self.white_rectangle_image, (700, 420))
        self.screen.blit(self.white_rectangle_image, (1070, 420))
        self.screen.blit(self.white_rectangle_image, (885, 420))
        self.screen.blit(self.white_rectangle_image, (792.5, 657))
        self.screen.blit(self.white_rectangle_image, (977.5, 657))
        # affichage du deck
        self.screen.blit(self.deck_image, (885, 150))
    
    
    def update(self) :
        self.update_turn()
        self.draw()
        self.player.draw()
    
    