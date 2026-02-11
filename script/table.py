import pygame
from player import *
from support import import_folder
import random
from bot_test import *
from combinations import *


class Table :
    def __init__(self) :
        self.player = Player()
        self.screen = pygame.display.get_surface()
        self.screen_width, self.screen_height = self.screen.get_size()
        self.mouse_clicked = False

        # --- PLAYERS --- 
        self.player1 = Player()
        self.player2 = BotTest()
        self.player3 = BotTest()
        self.players = [self.player1, self.player2, self.player3] 
        self.round_players = [self.player1, self.player2, self.player3]
        self.players_who_can_receive_chips = []
        self.active_player_indice = 0

        # --- PHASE ---
        self.active_turn = 'shuffle'
        self.shuffle_done = False 
        self.shuffle_animation_done = False
        self.time_since_end_shuffle_anim = 0
        self.distribution_done = False
        self.distribution_animation_done = False
        self.board_generation_done = False
        self.board_generation_anim_done = False
        self.player_turn_done = False
        self.chip_distribution_done = False
        self.chip_distribution_anim_done = False
        
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
        self.round_finished = False
        self.board_image_pos = {
            '1' : (700, 420),
            '2' : (885, 420),
            '3' : (1070, 420),
            '4' : (792.5, 657),
            '5' : (977.5, 657),
        }
        self.pot = 0
        self.max_bet = 0

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
        
        self.font = pygame.font.Font('graphics/ui/font.ttf', 55)

        # --- ANIMATIONS ---
        self.animations = {
            'shuffle' : import_folder('graphics/animations/shuffle', 4),
            'win' : import_folder('graphics/animations/win', 1.5),
            'lose' : import_folder('graphics/animations/lose', 1.5)
        }

        self.actual_animations = []
        self.actual_transition = None

        self.animations_infos = {
            # shuffle anim infos
            'shuffle' : {
                'pos' : (625, 102),
                'index' : 0,
                'speed' : 12
            },
            # win anim
            'win' : {
                'pos' : (1380, 350),
                'index' : 0,
                'speed' : 6
            },
            # lose anim
            'lose' : {
                'pos' : (1450, 450),
                'index' : 0,
                'speed' : 6
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
        self.board.append(self.deck_cards[self.deck_indice])
        self.deck_indice += 1
        self.board_generation_done = True
        
    
    def river(self) :
        self.board.append(self.deck_cards[self.deck_indice])
        self.deck_indice += 1
        self.board_generation_done = True
        
    
    def board_generation(self) :
        self.board_generation_done = True
        if len(self.board) == 0 :
            self.flop()
        elif len(self.board) == 3 :
            self.turn()
        else :
            self.river()


    def chip_distribution(self) :
        # from combinations import combinations

        # # Sécurité si personne n'est éligible
        # if not self.players_who_can_receive_chips:
        #     self.chip_distribution_done = True
        #     return

        # # 1. Trouver le meilleur score parmi les joueurs éligibles
        # best_score = -1
        # winners = []

        # for player in self.players_who_can_receive_chips:
        #     # On évalue la main du joueur avec les cartes sur la table
        #     score = combinations(player.hand, self.board)
            
        #     if score > best_score:
        #         best_score = score
        #         winners = [player]
        #     elif score == best_score:
        #         winners.append(player)

        # # 2. Distribuer le pot
        # if winners:
        #     gain_per_winner = self.pot // len(winners)
        #     for winner in winners:
        #         winner.chip_number += gain_per_winner
                
        #         # Gestion des animations selon le type du gagnant
        #         if winner.type == 'player':
        #             if 'win' not in self.actual_animations:
        #                 self.actual_animations.append('win')
        #         else: # C'est un bot
        #             if 'lose' not in self.actual_animations:
        #                 self.actual_animations.append('lose')

        # # 3. Nettoyage et élimination des joueurs sans jetons
        # self.pot = 0
        # self.chip_distribution_done = True
        
        # On utilise une copie [:] pour pouvoir supprimer des éléments en itérant
        for player in self.players[:]:
            if player.chip_number <= 0:
                self.players.remove(player)
        # self.actual_animations.append('lose')
        self.actual_animations.append('win')
        self.chip_distribution_done = True


    def turn_reset(self) :
        # reset des phase d'un tour de jeu
        self.active_turn = 'shuffle'
        self.shuffle_done = False 
        self.shuffle_animation_done = False
        self.time_since_end_shuffle_anim = 0
        self.distribution_done = False
        self.distribution_animation_done = False
        self.board_generation_done = False
        self.board_generation_anim_done = False
        self.player_turn_done = False
        self.chip_distribution_done = False
        self.chip_distribution_anim_done = False
            
        # reset des joueurs et de leur main
        self.round_players = []
        for player in self.players :
            self.round_players.append(player)
            player.hand = []
            
        # reset de la table de jeu (deck et board et jetons)
        self.pot = 0
        self.max_bet = 0
        self.board = []
        self.flop_done = False
        self.turn_done = False
        self.river_done = False
        self.round_finished = False
        self.deck_indice = 0
        
        # reset des anims du board
        self.actual_animations = []
        
        self.animations_infos = {
            # shuffle anim infos
            'shuffle' : {
                'pos' : (625, 102),
                'index' : 0,
                'speed' : 12
            },
            # win anim
            'win' : {
                'pos' : (1380, 350),
                'index' : 0,
                'speed' : 6
            },
            # lose anim
            'lose' : {
                'pos' : (1450, 450),
                'index' : 0,
                'speed' : 6
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
    

    def turn_action(self) :
        if self.active_turn == 'shuffle' and not self.shuffle_done :
            self.shuffle_deck()
            self.players_who_can_receive_chips = []
            
        if self.active_turn == 'distribution' and not self.distribution_done : 
            self.distribute_cards()
            
        if self.active_turn == 'board_generation' and not self.board_generation_done : 
            self.board_generation()
            
        possible_actions = ['Check', 'Bet', 'Fold'] if self.max_bet == 0 else ['Call', 'Raise', 'Fold']
        
        if self.active_turn == 'player' :
            self.round_players[self.active_player_indice].update(self.screen, possible_actions, self)
            
        if self.active_turn == 'chip_distribution' and not self.chip_distribution_done :
            self.chip_distribution()
            
            
    def shuffle_end(self, dt) :
        if self.time_since_end_shuffle_anim > 0.3 :
            self.active_turn = 'distribution'
            if 'distribution' not in self.actual_animations :
                self.actual_animations.append('distribution')
        else :
            self.time_since_end_shuffle_anim += dt
            
            
    def distribution_end(self) :
        self.active_turn = 'board_generation'
        if 'board_generation' not in self.actual_animations :
            self.actual_animations.append('board_generation')
            
            
    def board_generation_end(self) :
        self.active_turn = 'player'
        self.board_generation_done = False
        self.board_generation_anim_done = False
            
            
    def player_turn_end(self) :
        # Cas 1 : Un seul joueur restant ou round marqué comme fini
        if  len(self.round_players) <= 1 and len(self.players_who_can_receive_chips) == 1 : 
            self.active_turn = 'chip_distribution'
            self.chip_distribution_anim_done = True
            self.player_turn_done = False
        # Cas 2 : il n'y a pas eu de tour apres le river et il reste plus de 1 joueur en competition
        else :
            self.active_player_indice += 1 # Passer au joueur suivant
                
            # Si on a fait le tour de la table
            if self.active_player_indice >= len(self.round_players) :
                self.active_player_indice = 0
                    
                if not self.river_done :
                    # Si on n'est pas à la fin, on génère la phase suivante (Flop, Turn ou River)
                    self.active_turn = 'board_generation'
                    self.actual_animations.append('board_generation')
                    self.player_turn_done = False 
                else :
                    # si la river a déjà été faite : on arrête les tours de mise
                    self.active_turn = 'chip_distribution'
                    # self.chip_distribution_anim_done = True
                    self.player_turn_done = False
            else :
                # Si on n'est pas au bout de la table, on continue simplement le tour
                self.player_turn_done = False
                    
                # Pour les Bots
                if self.round_players[self.active_player_indice].type == 'bot': 
                    self.round_players[self.active_player_indice].beginning_turn_time = pygame.time.get_ticks()
    
            
    def update_turn_phase(self, dt) :
        # --- la premiere phase du tout est le melange --- 
        if self.active_turn == 'shuffle' and not self.shuffle_animation_done :
            if 'shuffle' not in self.actual_animations :
                self.animations_infos['shuffle']['index'] = 0
                self.actual_animations.append('shuffle')

        # --- quand le mélange est terminé depuis au moins 0.3 seconde ---
        if self.active_turn == 'shuffle' and self.shuffle_done and self.shuffle_animation_done :
            self.shuffle_end(dt)
            
        # --- quand la distribution est terminée --- 
        if self.active_turn == 'distribution' and self.distribution_done and self.distribution_animation_done :
            self.distribution_end()
        
        # --- quand la mise en place des cartes communes est terminée ---
        if self.active_turn == 'board_generation' and self.board_generation_done and self.board_generation_anim_done :
            self.board_generation_end()

        # --- quand le tour du joueur est terminé ---
        if self.active_turn == 'player' and self.player_turn_done : 
            self.player_turn_end()
            
        # --- quand le pot doit être distribué ---
        if self.active_turn == 'chip_distribution' and self.chip_distribution_done and self.chip_distribution_anim_done :
            self.turn_reset()
            
    
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
        if self.animations_infos['board_generation']['card4_pos'][1] < self.animations_infos['board_generation']['card4_final_pos'][1] :
            # update card4
            self.animations_infos['board_generation']['card4_pos'][0] -= dt * 92.5
            self.animations_infos['board_generation']['card4_pos'][1] += dt * 507
            # define the new position
            card4_pos = self.animations_infos['board_generation']['card4_pos']
        else :
            card4_pos = self.animations_infos['board_generation']['card4_final_pos']
            self.board_generation_anim_done = True
            self.turn_done = True
            self.actual_animations.remove('board_generation')
        self.screen.blit(self.back_image, card4_pos)
    
    
    def update_and_draw_river_animation(self, dt) :
        if self.animations_infos['board_generation']['card5_pos'][1] < self.animations_infos['board_generation']['card5_final_pos'][1] :
            # update card5
            self.animations_infos['board_generation']['card5_pos'][0] += dt * 92.5
            self.animations_infos['board_generation']['card5_pos'][1] += dt * 507
            # define the new position
            card5_pos = self.animations_infos['board_generation']['card5_pos']
        else :
            card5_pos = self.animations_infos['board_generation']['card5_final_pos']
            self.board_generation_anim_done = True
            self.river_done = True
            self.actual_animations.remove('board_generation')
        self.screen.blit(self.back_image, card5_pos)
    
    
    def update_and_draw_board_generation_animation(self, dt) :
        if not self.flop_done :
            self.update_and_draw_flop_animation(dt)
        elif not self.turn_done :
            self.update_and_draw_turn_animation(dt)
        elif not self.river_done :
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
        self.animations_infos[animation]['index'] += dt * self.animations_infos[animation]['speed']
        index = int(self.animations_infos[animation]['index'])

        if index >= len(self.animations[animation]) :
            self.actual_animations.remove(animation)
            if animation == 'shuffle' :
                self.shuffle_animation_done = True
            if animation == 'win' or animation == 'lose' :
                self.chip_distribution_anim_done = True
        else :
            pos = self.animations_infos[animation]['pos']
            self.screen.blit(self.animations[animation][index], pos)
    
        
    def update_and_draw_animations(self, dt) :
        for animation in self.actual_animations.copy() :
            if animation in ['shuffle', 'win', 'lose'] :
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
                if not self.turn_done and i == 4 :
                    break
                if not self.river_done and i == 5 :
                    break


    def draw_chip_infos(self) :
        # rects
        pygame.draw.rect(self.screen, (46, 82, 58), (635, 1, 638, 142))
        pygame.draw.rect(self.screen, (104, 157, 113), (640, 6, 628, 132))
        
        # infos
        pot_text = f'POT : {self.pot}'
        max_bet_text = f'MAX BET : {self.max_bet}'
        pot_text_surface = self.font.render(pot_text, True, (255, 255, 255))
        max_bet_text_surface = self.font.render(max_bet_text, True, (255, 255, 255))
        self.screen.blit(pot_text_surface, (797, 5))
        self.screen.blit(max_bet_text_surface, (647, 65))
        

    def update(self, dt) :
        self.update_turn_phase(dt)
        self.draw()
        self.draw_board()   
        self.turn_action()
        self.update_and_draw_animations(dt)
        self.draw_deck()
        if self.active_turn not in ['shuffle', 'distribution'] :
            self.draw_chip_infos()
            self.player1.draw(self.screen) 
            # self.players[self.active_player_indice].draw(self.screen) 

    
    