import pygame
import pygame, sys
from table import *
from settings import *
from menu import *
from multiserver.network import *

class Game :
    def __init__(self) :
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF, vsync=1)
        pygame.display.set_caption("Poker 2")
        self.clock = pygame.time.Clock()
        self.menu = Menu(self.screen)
        self.table = Table()
        
        self.network = Network(on_state_update=self.on_game_state_updated)
        self.connected = self.network.connect()

    def on_game_state_updated(self, state_data):
        """Appelé quand le serveur envoie un nouvel état"""
        # Mettre à jour la table locale avec les données du serveur
        self.table.pot = state_data['pot']
        self.table.max_bet = state_data['max_bet']
        self.table.board = state_data['board']
        self.table.active_player_indice = state_data['active_player_index']
        self.table.active_turn = state_data['phase']
        
        # Mettre à jour les joueurs
        for i, player_data in enumerate(state_data['players']):
            if i < len(self.table.players):
                self.table.players[i].chip_number = player_data['chips']
                self.table.players[i].hand = player_data.get('hand', [])
    
    def player_bet(self, amount):
        """Quand le joueur local mise"""
        self.network.send_action('bet', amount=amount)
    
    def player_fold(self):
        """Quand le joueur local se couche"""
        self.network.send_action('fold')

    def run(self) :
        while True :
            dt = self.clock.tick(0) / 1000.0  # secondes
            events = pygame.event.get()
            self.table.mouse_clicked = False
            for event in events :
                if event.type == pygame.QUIT :
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN :
                    if event.button == 1 :
                        self.table.mouse_clicked = True
                        

            if self.menu.is_open :
                self.menu.update()
            else :
                self.table.update(dt)
            # self.table.draw()
            pygame.display.update()

if __name__ == "__main__" :
    game = Game()
    game.run()
