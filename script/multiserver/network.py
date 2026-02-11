import socket
import pickle
from threading import Thread

class Network:
    def __init__(self, on_state_update):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.2.139"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.player_id = None
        self.on_state_update = on_state_update  
        self.running = True
        
    def connect(self):
        try:
            self.client.connect(self.addr)
            self.player_id = pickle.loads(self.client.recv(2048*8))
            print(f"Connecté en tant que joueur {self.player_id}")
            
            Thread(target=self.receive_loop, daemon=True).start()
            return True
        except Exception as e:
            print(f"Erreur connexion: {e}")
            return False
    
    def receive_loop(self):
        while self.running:
            try:
                state_data = pickle.loads(self.client.recv(2048*8))
                self.on_state_update(state_data)
            except Exception as e:
                print(f"Erreur réception: {e}")
                break
    
    def send_action(self, action_type, **kwargs):
        action = {'type': action_type, **kwargs}
        try:
            self.client.send(pickle.dumps(action))
        except Exception as e:
            print(f"Erreur envoi: {e}")
    
    def disconnect(self):
        self.running = False
        self.client.close()