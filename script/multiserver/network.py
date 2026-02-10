# network_improved.py
import socket
import pickle
from threading import Thread

class Network:
    def __init__(self, on_state_update):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.17"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player_id = None
        self.on_state_update = on_state_update  # Callback quand état change
        self.running = True
        
    def connect(self):
        """Se connecte au serveur"""
        try:
            self.client.connect(self.addr)
            self.player_id = pickle.loads(self.client.recv(2048*8))
            print(f"Connecté en tant que joueur {self.player_id}")
            
            # Démarrer thread d'écoute
            Thread(target=self.receive_loop, daemon=True).start()
            return True
        except Exception as e:
            print(f"Erreur connexion: {e}")
            return False
    
    def receive_loop(self):
        """Thread qui écoute en continu les mises à jour du serveur"""
        while self.running:
            try:
                state_data = pickle.loads(self.client.recv(2048*8))
                # Appeler le callback avec le nouvel état
                self.on_state_update(state_data)
            except Exception as e:
                print(f"Erreur réception: {e}")
                break
    
    def send_action(self, action_type, **kwargs):
        """Envoie une action au serveur"""
        action = {'type': action_type, **kwargs}
        try:
            self.client.send(pickle.dumps(action))
        except Exception as e:
            print(f"Erreur envoi: {e}")
    
    def disconnect(self):
        """Déconnexion propre"""
        self.running = False
        self.client.close()