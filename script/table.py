import pygame
from player import *
from support import import_folder
import random


class Table :
    def __init__(self) :
        self.player = Player()
        self.screen = pygame.display.get_surface()
        self.screen_width, self.screen_height = self.screen.get_size()

        # --- PLAYERS --- 
        self.player1 = Player()
        self.player2 = Player()
        self.player3 = Player()
        self.players = [self.player1, self.player2, self.player3]

        # --- PHASE ---
        self.active_turn = 'shuffle'
        self.shuffle_done = False 
        self.shuffle_animation_done = False
        self.time_since_end_shuffle_anim = 0
        self.distribution_done = False
        self.distribution_animation_done = False
        self.board_generation_done = False
        self.board_generation_anim_done = False
        
        # --- DECK COMPOSITION ---
        self.deck_cards = []
        self.deck_indice = 0
        card_representation = {"p" : ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13'],
                               "c" : ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13'],
                               "t" : ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13'],
                               "k" : ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13']}
        for key, values in card_representation.items() :
            for value in values :
                self.deck_cards.append(str(value + key))
                
        self.card_images = {}
        for card in self.deck_cards :
            self.card_images[card] = pygame.transform.scale(pygame.image.load(f'graphics/cartes/{card}.png').convert(), (140, 192))
                
        # --- BOARD ---
        self.board = []
        self.flop_done = False
        self.turn_done = False
        self.river_done = False
        self.board_image_pos = {
            '1' : (700, 420),
            '2' : (885, 420),
            '3' : (1070, 420),
            '4' : (792.5, 657),
            '5' : (977.5, 657),
        }

        # --- IMAGES ---
        self.table_image = pygame.image.load('graphics/table_de_jeu/table_verte.png').convert()
        self.table_image = pygame.transform.scale(self.table_image, (self.screen_width, self.screen_height))

        self.white_rectangle_image = pygame.image.load('graphics/table_de_jeu/rectangle_blanc.png').convert_alpha()
        self.white_rectangle_image = pygame.transform.scale(self.white_rectangle_image, (140, 192))
        
        self.back_image = pygame.image.load('graphics/table_de_jeu/back.png').convert_alpha()
        self.back_image = pygame.transform.scale(self.back_image, (140, 192))
        
        self.selection_image = pygame.image.load('graphics/table_de_jeu/selection.png').convert_alpha()
        self.selection_image = pygame.transform.scale(self.selection_image, (140, 192))

        self.deck_image = pygame.image.load('graphics/table_de_jeu/deck.png').convert_alpha()
        self.deck_image = pygame.transform.scale(self.deck_image, (140, 252))

        # --- ANIMATIONS ---
        self.animations = {
            'shuffle' : import_folder('graphics/animations/shuffle')
        }

        self.actual_animations = []

        self.animations_infos = {
            # shuffle anim infos
            'shuffle' : {
                'pos' : (625, 102),
                'index' : 0
            },
            # distribution anim infos
            'distribution' : {
                'card1_pos' : [885, 150],
                'card2_pos' : [885, 150],
                'card1_final_pos' : (800, 890),
                'card2_final_pos' : (970, 890),
            },
            # generation of the board anim infos
            'board_generation' : {
                'card1_pos' : [885, 150],
                'card2_pos' : [885, 150],
                'card3_pos' : [885, 150],
                'card4_pos' : [885, 150],
                'card5_pos' : [885, 150],
                'card1_final_pos' : (700, 420),
                'card2_final_pos' : (885, 420),
                'card3_final_pos' : (1070, 420),
                'card4_final_pos' : (792.5, 657),
                'card5_final_pos' : (977.5, 657),
            },
        }


    def shuffle_deck(self) :
        random.shuffle(self.deck_cards)
        self.shuffle_done = True
        # print(self.deck_cards)


    def distribute_cards(self) :
        for player in self.players :
            player.hand = [self.deck_cards[self.deck_indice], self.deck_cards[self.deck_indice + 1]]
            player.card1_image = self.card_images[self.deck_cards[self.deck_indice]]
            player.card2_image = self.card_images[self.deck_cards[self.deck_indice + 1]]
            self.deck_indice += 2
        self.distribution_done = True
        
        
    def flop(self) :
        for i in range(3) :
            self.board.append(self.deck_cards[self.deck_indice])
            self.deck_indice += 1
        self.board_generation_done = True
        # print(self.board)
    
    
    def turn(self) :
        self.board_generation_done = True
    
    
    def river(self) :
        self.board_generation_done = True
        
    
    def board_generation(self) :
        self.board_generation_done = True
        if len(self.board) == 0 :
            self.flop()
        elif len(self.board) == 3 :
            self.turn()
        else :
            self.river()


    def turn_action(self) :
        if self.active_turn == 'shuffle' and not self.shuffle_done :
            self.shuffle_deck()
            
        if self.active_turn == 'distribution' and not self.distribution_done : 
            self.distribute_cards()
            
        if self.active_turn == 'board_generation' and not self.board_generation_done : 
            self.board_generation()
            
        if self.active_turn == 'player1' :
            self.player1.update(self.screen)
            
            
    def update_turn_phase(self, dt) :
        # la premiere phase du tout est le melange
        if self.active_turn == 'shuffle' and not self.shuffle_animation_done :
            if 'shuffle' not in self.actual_animations :
                self.animations_infos['shuffle']['index'] = 0
                self.actual_animations.append('shuffle')

        # quand le mélange est terminé depuis au moins 0.3 seconde
        if self.active_turn == 'shuffle' and self.shuffle_done and self.shuffle_animation_done :
            if self.time_since_end_shuffle_anim > 0.3 :
                self.active_turn = 'distribution'
                if 'distribution' not in self.actual_animations :
                    self.actual_animations.append('distribution')
            else :
                self.time_since_end_shuffle_anim += dt
            
        # quand la distribution est terminée    
        if self.active_turn == 'distribution' and self.distribution_done and self.distribution_animation_done :
            self.active_turn = 'board_generation'
            if 'board_generation' not in self.actual_animations :
                self.actual_animations.append('board_generation')
        
        # quand la mise en place des cartes communes est terminée
        if self.active_turn == 'board_generation' and self.board_generation_done and self.board_generation_anim_done :
            self.active_turn = 'player1'
            # print('okk')
            
    
    def update_and_draw_flop_animation(self, dt) :
        if self.animations_infos['board_generation']['card1_pos'][1] < self.animations_infos['board_generation']['card1_final_pos'][1] :
            # update card1
            self.animations_infos['board_generation']['card1_pos'][0] -= dt * 185
            self.animations_infos['board_generation']['card1_pos'][1] += dt * 270
            # update card2
            self.animations_infos['board_generation']['card2_pos'][1] += dt * 270
            # update_card3
            self.animations_infos['board_generation']['card3_pos'][0] += dt * 185
            self.animations_infos['board_generation']['card3_pos'][1] += dt * 270
            # define the new positions
            card1_pos = self.animations_infos['board_generation']['card1_pos']
            card2_pos = self.animations_infos['board_generation']['card2_pos']
            card3_pos = self.animations_infos['board_generation']['card3_pos']
        else :
            card1_pos = self.animations_infos['board_generation']['card1_final_pos']
            card2_pos = self.animations_infos['board_generation']['card2_final_pos']
            card3_pos = self.animations_infos['board_generation']['card3_final_pos']
            self.board_generation_anim_done = True
            self.flop_done = True
            self.actual_animations.remove('board_generation')
        
        self.screen.blit(self.back_image, card1_pos)
        self.screen.blit(self.back_image, card2_pos)
        self.screen.blit(self.back_image, card3_pos)
    
    
    def update_and_draw_turn_animation(self, dt) :
        pass
    
    
    def update_and_draw_river_animation(self, dt) :
        pass
    
    
    def update_and_draw_board_generation_animation(self, dt) :
        if not self.flop_done :
            self.update_and_draw_flop_animation(dt)
        elif self.flop_done :
            self.update_and_draw_turn_animation(dt)
        else :
            self.update_and_draw_river_animation(dt)
    
    
    def update_and_draw_distribution_animation(self, dt) :
        if self.animations_infos['distribution']['card1_pos'][1] < self.animations_infos['distribution']['card1_final_pos'][1] :
            # update card1
            self.animations_infos['distribution']['card1_pos'][0] -= dt * 68
            self.animations_infos['distribution']['card1_pos'][1] += dt * 592
            # update card2
            self.animations_infos['distribution']['card2_pos'][0] += dt * 68
            self.animations_infos['distribution']['card2_pos'][1] += dt * 592
            # define the new positions
            card1_pos = self.animations_infos['distribution']['card1_pos']
            card2_pos = self.animations_infos['distribution']['card2_pos']
        else :
            card1_pos = self.animations_infos['distribution']['card1_final_pos']
            card2_pos = self.animations_infos['distribution']['card2_final_pos']
            self.distribution_animation_done = True
            self.actual_animations.remove('distribution')
        
        self.screen.blit(self.back_image, card1_pos)
        self.screen.blit(self.back_image, card2_pos)
    
    
    def update_and_draw_frame_animation(self, animation, dt) :
        self.animations_infos[animation]['index'] += dt * 12
        index = int(self.animations_infos[animation]['index'])

        if index >= len(self.animations[animation]) :
            self.actual_animations.remove(animation)
            if animation == 'shuffle' :
                self.shuffle_animation_done = True
        else :
            pos = self.animations_infos[animation]['pos']
            self.screen.blit(self.animations[animation][index], pos)
    
        
    def update_and_draw_animations(self, dt) :
        for animation in self.actual_animations.copy() :
            if animation in ['shuffle'] :
                self.update_and_draw_frame_animation(animation, dt)
            elif animation == 'distribution' :
                self.update_and_draw_distribution_animation(dt)
            elif animation == 'board_generation' :
                self.update_and_draw_board_generation_animation(dt)
                

    def draw(self) :
        # table
        self.screen.blit(self.table_image, (0, 0))

        # rectangles blancs
        self.screen.blit(self.white_rectangle_image, (700, 420))
        self.screen.blit(self.white_rectangle_image, (1070, 420))
        self.screen.blit(self.white_rectangle_image, (885, 420))
        self.screen.blit(self.white_rectangle_image, (792.5, 657))
        self.screen.blit(self.white_rectangle_image, (977.5, 657))


    def draw_deck(self) :
        # deck visible seulement après le mélange
        if self.shuffle_animation_done :
            self.screen.blit(self.deck_image, (885, 150))
            
    
    def draw_board(self) :
        mouse_pos = pygame.mouse.get_pos()
        if self.flop_done :
            i = 1
            for card in self.board :
                pos = self.board_image_pos[str(i)]
                card_image = self.card_images[card]
                card_rect = card_image.get_rect(topleft = pos)
                self.screen.blit(card_image, pos)
                if card_rect.collidepoint(mouse_pos) :
                    self.screen.blit(self.selection_image, pos)
                    self.player.draw_card_info(card, self.screen)
                i += 1


    def update(self, dt):
        self.update_turn_phase(dt)
        self.draw()
        self.draw_board()   
        self.turn_action()
        self.update_and_draw_animations(dt)
        self.draw_deck()
        if self.active_turn not in ['shuffle', 'distribution'] :
            self.player1.draw(self.screen)

    
    