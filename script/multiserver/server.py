

#192.168.56.1 , ip adress numero 1
#192.168.2.139 , ip adress numero 2


import socket
from _thread import *
import pickle
from threading import Lock
from script.multiserver.game_state import GameState

class PokerServer:
    def __init__(self):
        self.game_state = GameState()
        self.lock = Lock()  # Pour éviter les race conditions
        self.clients = []   # Liste des connexions actives
        
    def process_action(self, player_id, action):
        """Traite une action joueur et retourne le nouvel état"""
        with self.lock:  # Verrouiller pendant la modification
            if action['type'] == 'bet':
                amount = action['amount']
                self.game_state.pot += amount
                self.game_state.players[player_id]['chips'] -= amount
                self.game_state.max_bet = max(self.game_state.max_bet, amount)
                
            elif action['type'] == 'fold':
                self.game_state.players[player_id]['folded'] = True
                
            elif action['type'] == 'call':
                amount = self.game_state.max_bet
                self.game_state.pot += amount
                self.game_state.players[player_id]['chips'] -= amount
            
            # Passer au joueur suivant
            self.next_player()
            
            return self.game_state.to_dict()
    
    def next_player(self):
        """Passe au joueur suivant (logique métier)"""
        self.game_state.active_player_index += 1
        if self.game_state.active_player_index >= len(self.game_state.players):
            self.game_state.active_player_index = 0
            # Passer à la phase suivante si tour terminé
            if self.game_state.phase == 'player':
                self.game_state.phase = 'board_generation'
    
    def broadcast_state(self):
        """Envoie l'état à tous les clients"""
        state_data = self.game_state.to_dict()
        for conn in self.clients[:]:  # Copie pour éviter modification pendant itération
            try:
                conn.sendall(pickle.dumps(state_data))
            except:
                self.clients.remove(conn)
    
    def handle_client(self, conn, player_id):
        """Gère un client connecté"""
        conn.send(pickle.dumps(player_id))
        self.clients.append(conn)
        
        # Envoyer l'état initial
        conn.sendall(pickle.dumps(self.game_state.to_dict()))
        
        while True:
            try:
                data = pickle.loads(conn.recv(2048*8))
                if not data:
                    break
                
                # Traiter l'action du joueur
                new_state = self.process_action(player_id, data)
                
                # Broadcaster le nouvel état à tous
                self.broadcast_state()
                
            except Exception as e:
                print(f"Erreur client {player_id}: {e}")
                break
        
        print(f"Joueur {player_id} déconnecté")
        self.clients.remove(conn)
        conn.close()
    
    def start(self):
        """Démarre le serveur"""
        server = "192.168.1.17"
        port = 5555
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((server, port))
        s.listen(4)
        
        print(f"🎴 Serveur de poker démarré sur {server}:{port}")
        
        current_player = 0
        while True:
            conn, addr = s.accept()
            print(f"✅ Nouveau joueur connecté: {addr}")
            start_new_thread(self.handle_client, (conn, current_player))
            current_player += 1

if __name__ == "__main__":
    server = PokerServer()
    server.start()