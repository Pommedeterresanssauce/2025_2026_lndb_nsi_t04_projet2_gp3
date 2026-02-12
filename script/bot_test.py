from combinations_test import combinations
from math import *
from random import *
import random
from probability import *
from combinations_test import combinations
from math import *
from random import *
import random
from probability import *
import pygame

class BotTest :
    def __init__(self, image_path, draw_pos) :
        self.type = 'bot'
        self.hand = []
        self.chip_number = 2000
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert(), (200, 200))
        self.draw_pos = draw_pos
        self.turn_done = False
        self.futur_action = None
        self.futur_bet = 0
        self.beginning_turn_time = 0
        self.font = pygame.font.Font('graphics/ui/font.ttf', 40)
        

    def draw_image(self, screen) :
        screen.blit(self.image, self.draw_pos)
        text_surface = self.font.render(str(self.chip_number), True, (255, 255, 255))
        screen.blit(text_surface, (self.draw_pos[0] + 30, self.draw_pos[1] + 210))
        

    def draw_action_name(self, screen) :
        if self.futur_action :
            text_surface = self.font.render(self.futur_action, True, (255, 255, 255))
            screen.blit(text_surface, (self.draw_pos[0] + 35, self.draw_pos[1] + 275))


    def all_in(self, table) :
        table.pot += self.chip_number
        self.chip_number = 0
        table.player_turn_done = True
        # Trouver l'indice du joueur actuel avant de le retirer
        current_index = table.round_players.index(self)
        table.round_players.remove(self)
        # Ajuster l'indice du joueur actif si nécessaire
        if current_index < table.active_player_indice :
            table.active_player_indice -= 1        
        

    def action_check(self, table) :
        table.player_turn_done = True


    def action_call(self, table) :
        if self not in table.players_who_can_receive_chips :
            table.players_who_can_receive_chips.append(self)
        if self.chip_number >= table.max_bet :
            table.player_turn_done = True
            table.pot += table.max_bet
            self.chip_number -= table.max_bet
            if self.chip_number == 0 :
                # Trouver l'indice du joueur actuel avant de le retirer
                current_index = table.round_players.index(self)
                table.round_players.remove(self)
                # Ajuster l'indice du joueur actif si nécessaire
                if current_index < table.active_player_indice :
                    table.active_player_indice -= 1
        else :
            self.all_in(table)


    def action_bet(self, table, bet_value) :
        if self not in table.players_who_can_receive_chips :
            table.players_who_can_receive_chips.append(self)
        if self.chip_number >= bet_value :
            table.max_bet = bet_value
            table.pot += bet_value
            self.chip_number -= bet_value
            table.player_turn_done = True
            if self.chip_number == 0 :
                # Trouver l'indice du joueur actuel avant de le retirer
                current_index = table.round_players.index(self)
                table.round_players.remove(self)
                # Ajuster l'indice du joueur actif si nécessaire
                if current_index < table.active_player_indice :
                    table.active_player_indice -= 1
        else :
            self.all_in(table)


    def action_raise(self, table, bet_value) :
        if self not in table.players_who_can_receive_chips :
            table.players_who_can_receive_chips.append(self)
        if self.chip_number >= bet_value :
            table.pot += bet_value
            self.chip_number -= bet_value
            table.max_bet = bet_value
            table.player_turn_done = True
            if self.chip_number == 0 :
                # Trouver l'indice du joueur actuel avant de le retirer
                current_index = table.round_players.index(self)
                table.round_players.remove(self)
                # Ajuster l'indice du joueur actif si nécessaire
                if current_index < table.active_player_indice :
                    table.active_player_indice -= 1
        else :
            self.all_in(table)


    def action_fold(self, table) :
        if self in table.players_who_can_receive_chips :
            table.players_who_can_receive_chips.remove(self)
        table.player_turn_done = True
        table.round_players.remove(self)
        table.active_player_indice -= 1
    
    
    def decide_action(self, possible_actions, table) :
        # Facteur de bluff aléatoire (1-10) - plus le chiffre est élevé, plus le bot bluffe
        bluff_factor = randint(1, 10)
        
        # Calculer la combinaison actuelle du bot
        my_combo = combinations(self.hand, table.board)
        
        # Calculer les probabilités
        probabilities = calculate_probability(table.board, table.deck_cards, iterations=500)
        
        # Probabilité que l'adversaire ait une main moins forte
        inferior_proba = get_inferior_proba(probabilities, my_combo)
        
        # Probabilité que l'adversaire ait une main plus forte
        superior_proba = get_superior_proba(probabilities, my_combo)
        
        # Win probability (on gagne si l'adversaire a moins bien)
        win_proba = inferior_proba
        
        # Ratio de la mise par rapport au stack (pour éviter les gros risques)
        bet_ratio = table.max_bet / self.chip_number if self.chip_number > 0 else 1
        
        # --- STRATÉGIE EN FONCTION DE LA WIN PROBABILITY ---
        
        # Excellente main (80%+ de chances de gagner)
        if win_proba >= 0.8 :
            if 'Bet' in possible_actions :
                # Mise très agressive
                if self.chip_number > 500 :
                    self.futur_bet = randint(300, min(self.chip_number, 1000))
                elif self.chip_number > 100 :
                    self.futur_bet = randint(100, self.chip_number)
                else :
                    self.futur_bet = self.chip_number
                self.futur_action = 'Bet'
                
            elif 'Raise' in possible_actions :
                # Relance très agressive
                min_raise = table.max_bet + 100
                if self.chip_number > min_raise :
                    self.futur_bet = randint(min_raise, min(self.chip_number, table.max_bet * 3))
                else :
                    self.futur_bet = self.chip_number
                self.futur_action = 'Raise'
                
            elif 'Call' in possible_actions :
                # On suit toujours avec une excellente main
                self.futur_action = 'Call'
                
            else :  # Check disponible
                self.futur_action = 'Check'
        
        # Très bonne main (60%-80% de chances de gagner)
        elif win_proba >= 0.6 :
            if 'Bet' in possible_actions :
                # Mise agressive
                if self.chip_number > 500 :
                    self.futur_bet = randint(200, min(self.chip_number, 700))
                elif self.chip_number > 100 :
                    self.futur_bet = randint(100, self.chip_number)
                else :
                    self.futur_bet = self.chip_number
                self.futur_action = 'Bet'
                
            elif 'Raise' in possible_actions :
                # Relance agressive (70% du temps)
                if bluff_factor > 3 :
                    min_raise = table.max_bet + 50
                    if self.chip_number > min_raise :
                        self.futur_bet = randint(min_raise, min(self.chip_number, table.max_bet * 2))
                        self.futur_action = 'Raise'
                    else :
                        self.futur_action = 'Call' if 'Call' in possible_actions else 'Check'
                else :
                    self.futur_action = 'Call' if 'Call' in possible_actions else 'Check'
                    
            elif 'Call' in possible_actions :
                # On suit presque toujours
                self.futur_action = 'Call'
                
            else :  # Check disponible
                self.futur_action = 'Check'
        
        # Bonne main (40%-60% de chances de gagner)
        elif win_proba >= 0.4 :
            if 'Bet' in possible_actions :
                # Mise modérée avec bluff fréquent (60% du temps)
                if bluff_factor > 4 :
                    if self.chip_number > 300 :
                        self.futur_bet = randint(150, 400)
                    else :
                        self.futur_bet = min(100, self.chip_number)
                    self.futur_action = 'Bet'
                else :
                    self.futur_action = 'Check'
                    
            elif 'Raise' in possible_actions :
                # Call ou parfois raise
                if bluff_factor > 7 :  # 30% de relance
                    min_raise = table.max_bet + 50
                    if self.chip_number > min_raise * 2 :
                        self.futur_bet = min_raise
                        self.futur_action = 'Raise'
                    else :
                        self.futur_action = 'Call' if 'Call' in possible_actions else 'Check'
                else :
                    self.futur_action = 'Call' if 'Call' in possible_actions else 'Check'
                    
            elif 'Call' in possible_actions :
                # On suit si la mise n'est pas trop grosse (< 50% du stack)
                if bet_ratio < 0.5 :
                    self.futur_action = 'Call'
                else :
                    # Fold seulement si la mise est énorme
                    self.futur_action = 'Fold'
                    
            else :  # Check disponible
                self.futur_action = 'Check'
        
        # Main moyenne (25%-40% de chances de gagner)
        elif win_proba >= 0.25 :
            if 'Bet' in possible_actions :
                # Bluff fréquent (50% du temps)
                if bluff_factor > 5 :
                    self.futur_bet = min(200, self.chip_number // 3)
                    self.futur_action = 'Bet'
                else :
                    self.futur_action = 'Check'
                    
            elif 'Raise' in possible_actions :
                # Call presque toujours, fold rarement
                if 'Call' in possible_actions :
                    if bet_ratio < 0.6 :  # Augmenté de 0.4 à 0.6
                        self.futur_action = 'Call'
                    else :
                        # Bluff agressif même avec main moyenne (40%)
                        if bluff_factor > 6 :
                            self.futur_action = 'Call'
                        else :
                            self.futur_action = 'Fold'
                else :
                    self.futur_action = 'Check'
                    
            elif 'Call' in possible_actions :
                # On suit presque toujours (< 50% du stack)
                if bet_ratio < 0.5 :  # Augmenté de 0.3 à 0.5
                    self.futur_action = 'Call'
                else :
                    # Bluff agressif (40%)
                    if bluff_factor > 6 :
                        self.futur_action = 'Call'
                    else :
                        self.futur_action = 'Fold'
                    
            else :  # Check disponible
                self.futur_action = 'Check'
        
        # Main faible (10%-25% de chances de gagner)
        elif win_proba >= 0.1 :
            if 'Bet' in possible_actions :
                # Bluff assez fréquent (40% du temps)
                if bluff_factor > 6 :
                    self.futur_bet = min(150, self.chip_number // 4)
                    self.futur_action = 'Bet'
                else :
                    self.futur_action = 'Check'
                    
            elif 'Raise' in possible_actions :
                # Call si mise raisonnable
                if 'Call' in possible_actions :
                    if bet_ratio < 0.4 :  # Augmenté de 0.2 à 0.4
                        self.futur_action = 'Call'
                    else :
                        # Bluff même avec main faible (30%)
                        if bluff_factor > 7 :
                            self.futur_action = 'Call'
                        else :
                            self.futur_action = 'Fold'
                else :
                    self.futur_action = 'Check'
                    
            elif 'Call' in possible_actions :
                # On suit si la mise est < 30% du stack
                if bet_ratio < 0.3 :  # Augmenté de 0.15 à 0.3
                    self.futur_action = 'Call'
                else :
                    # Bluff (30%)
                    if bluff_factor > 7 :
                        self.futur_action = 'Call'
                    else :
                        self.futur_action = 'Fold'
                    
            else :  # Check disponible
                self.futur_action = 'Check'
        
        # Main très faible (<10% de chances de gagner)
        else :
            if 'Bet' in possible_actions :
                # Bluff assez fréquent (30% du temps)
                if bluff_factor > 7 :
                    self.futur_bet = min(100, self.chip_number // 5)
                    self.futur_action = 'Bet'
                else :
                    self.futur_action = 'Check'
                    
            elif 'Raise' in possible_actions :
                # Call si mise faible ou bluff
                if 'Call' in possible_actions :
                    if bet_ratio < 0.25 :  # Augmenté de 0.1 à 0.25
                        self.futur_action = 'Call'
                    else :
                        # Bluff audacieux (25%)
                        if bluff_factor > 7.5 :
                            self.futur_action = 'Call'
                        else :
                            self.futur_action = 'Fold'
                else :
                    self.futur_action = 'Check'
                    
            elif 'Call' in possible_actions :
                # Call si mise < 20% du stack
                if bet_ratio < 0.2 :  # Augmenté de 0.1 à 0.2
                    self.futur_action = 'Call'
                else :
                    # Bluff même avec main nulle (20%)
                    if bluff_factor > 8 :
                        self.futur_action = 'Call'
                    else :
                        self.futur_action = 'Fold'
                    
            else :  # Check disponible
                self.futur_action = 'Check'
    
    
    def update(self, screen, possible_actions, table) :
        current_time = pygame.time.get_ticks()
        
        # Décider de l'action si ce n'est pas encore fait
        if self.futur_action is None :
            self.decide_action(possible_actions, table)
        
        # Exécuter l'action après 1 seconde
        if current_time - self.beginning_turn_time >= 1000 :
            if self.futur_action == 'Bet' : 
                self.action_bet(table, self.futur_bet)
            elif self.futur_action == 'Check' :
                self.action_check(table)
            elif self.futur_action == 'Call' :
                self.action_call(table)
            elif self.futur_action == 'Fold' :
                self.action_fold(table)
            elif self.futur_action == 'Raise' :
                self.action_raise(table, self.futur_bet)
            
            # Réinitialiser pour le prochain tour
            self.futur_action = None
            self.futur_bet = 0
        else :
            # Afficher l'action prévue pendant le délai
            self.draw_action_name(screen)