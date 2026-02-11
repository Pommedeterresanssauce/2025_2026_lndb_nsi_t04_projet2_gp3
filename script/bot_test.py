from combinations import*
from math import*
import random
from probability import*
import pygame

class BotTest :
    def __init__ (self) :
        self.type = 'bot'
        self.hand = []
        self.chip_number = 100000
        self.turn_done = False
        self.beginning_turn_time = 0
        
    
    def action_check(self, table) :
        table.player_turn_done = True
        print('check')


    def action_call(self, table) :
        table.player_turn_done = True
        print('call')


    def action_bet(self, table) :
        table.player_turn_done = True
        print('bet')


    def action_raise(self, table) :
        table.player_turn_done = True
        print('raise')


    def action_fold(self, table) :
        table.player_turn_done = True
        table.round_players.remove(self)
        table.active_player_indice -= 1
        print('fold')
    
    
    def update(self, screen, possible_actions, table) :
        current_time = pygame.time.get_ticks()
        if current_time - self.beginning_turn_time >= 1000 :
            number = random.randint(1, 100)
            if 'bet' in possible_actions :
                if number <= 40 :
                    self.action_bet(table)
                else :
                    self.action_check(table)
            else :
                if number <= 10 :
                    self.action_fold(table)
                elif 10 < number <= 80 :
                    self.action_call(table)
                else :
                    self.action_raise(table)