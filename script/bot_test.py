from combinations import*
from math import*
import random
from probability import*
import pygame

class BotTest :
    def __init__ (self, image_path, draw_pos) :
        self.type = 'bot'
        self.hand = []
        self.chip_number = 100000
        self.image = pygame.transform.scale(pygame.image.load(image_path).convert(), (200, 200))
        self.draw_pos = draw_pos
        self.turn_done = False
        self.futur_action = None
        self.beginning_turn_time = 0
        self.font = pygame.font.Font('graphics/ui/font.ttf', 40)
        

    def draw_image(self, screen) :
        screen.blit(self.image, self.draw_pos)


    def draw_action_name(self, screen) :
        text_surface = self.font.render(self.futur_action, True, (255, 255, 255))
        screen.blit(text_surface, (self.draw_pos[0] + 30, self.draw_pos[1] + 210))


    def all_in(self, table) :
        table.pot += self.chip_number
        self.chip_number = 0
        table.player_turn_done = True
        table.round_players.remove(self)        
        

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
                table.round_players.remove(self)
        else :
            self.all_in(table)


    def action_bet(self, table, bet_value) :
        if self not in table.players_who_can_receive_chips :
            table.players_who_can_receive_chips.append(self)
        if self.chip_number > table.max_bet :
            table.max_bet = bet_value
            table.pot += bet_value
            table.player_turn_done = True
        else :
            self.all_in()
        if self.chip_number == 0 :
                table.round_players.remove(self)


    def action_raise(self, table, bet_value) :
        if self not in table.players_who_can_receive_chips :
            table.players_who_can_receive_chips.append(self)
        table.max_bet = bet_value
        table.pot += bet_value
        table.player_turn_done = True
        if self.chip_number == 0 :
                table.round_players.remove(self)


    def action_fold(self, table) :
        if self in table.players_who_can_receive_chips :
            table.players_who_can_receive_chips.remove(self)
        table.player_turn_done = True
        table.round_players.remove(self)
        table.active_player_indice -= 1
    
    
    def update(self, screen, possible_actions, table) :
        current_time = pygame.time.get_ticks()
        if self.futur_action == None :
            number = random.randint(1, 100)
            if 'bet' in possible_actions :
                if number <= 90 :
                    self.futur_action = 'bet'
                else :
                    self.futur_action = 'check'
            else :
                if number <= 5 :
                    self.futur_action = 'fold'
                elif 5 < number <= 60 :
                    self.futur_action = 'call'
                else :
                    self.futur_action = 'raise'
                    
        if current_time - self.beginning_turn_time >= 1000 :
            if self.futur_action == 'bet' : 
                self.action_bet(table, 1)
            if self.futur_action == 'check' :
                self.action_check(table)
            if self.futur_action == 'call' :
                self.action_call(table)
            if self.futur_action == 'fold' :
                self.action_fold(table)
            if self.futur_action == 'raise' :
                self.action_raise(table, table.max_bet + 1)
            self.futur_action = None
            
        else :
            self.draw_action_name(screen)
            
            
                    