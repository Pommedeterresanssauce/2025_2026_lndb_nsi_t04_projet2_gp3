from combinations import*
from math import*
from random import*
from probability import*
import pygame

class Bot :
    def __init__ (self) :
        self.type = 'bot'
        self.hand = []
        self.chip_number = 2000
        self.turn_done = False
        self.beginning_turn_time = 0
        
    
    def action_check(self, table) :
        table.player_turn_done = True
        print('check')


    def action_call(self, table) :
        table.player_turn_done = True
        print('call')


    def action_bet(self, table, bet) :
        table.player_turn_done = True
        print('bet')


    def action_raise(self, table, bet) :
        table.player_turn_done = True
        print('raise')


    def action_fold(self, table) :
        table.player_turn_done = True
        table.players.remove(self)
        table.active_player_indice -= 1
        print('fold')
    
    
    def update(self, screen, possible_actions, table) :
        current_time = pygame.time.get_ticks()
        if current_time - self.beginning_turn_time >= 1000 :
            # table.board
            bluff_indice = randint(1, 10)
            combo = combinations(self.hand, table.board)
            probabilities = calculate_probability(self.hand, table.board, table.deck_cards)
            inferior_proba = get_inferior_proba(probabilities, combo)
            superior_proba = get_superior_proba(probabilities, combo)
            difference = 1 - inferior_proba - superior_proba

            # Victoire (quasi) garantie du bot, pas de bluff, que de la mise 
            if superior_proba + difference <= 0.15 :
                if 'bet' in possible_actions :
                    if self.chip_number > 500 :
                        bet = randint(200, self.chip_number - 200)
                    elif self.chip_number > 200 :
                        bet = 100
                    else :
                        bet = self.chip_number
                    return self.action_bet(table, bet)
                
                else :
                    return self.action_raise(table, self.chip_number)
                
            # Bot en position de force, bluff possible mais faible
            elif superior_proba + difference <= 0.3 :
                if bluff_indice > 8 :
                    return self.action_call(table)
                
                elif 'bet' in possible_actions :
                    if self.chip_number > 500 :
                        bet = randint(200, self.chip_number - 200)
                    elif self.chip_number > 200 :
                        bet = 100
                    else :
                        bet = self.chip_number
                    return self.action_bet(table, bet)
                
                else :
                    if randint(1,2) == 1 :
                        return self.action_raise(table, self.chip_number)
                    else :
                        if self.chip_number > 500 :
                            return self.action_raise
                        


            elif superior_proba + difference	<= 0.5 :
                pass

            elif superior_proba + difference <= 0.7 :
                pass
            
            # The bot is lowkey cooked
            else :
                if 'raise' in possible_actions :
                    return self.action_fold(table)
                return self.action_check(table)