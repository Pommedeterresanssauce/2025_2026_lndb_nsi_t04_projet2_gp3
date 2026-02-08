import socket
import pickle

class Network :
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur = "192.168.1.17"
        self.port = 5555
        self.addr = (self.serveur, self.port)
        self.player_id = self.connect()
        
    def connect(self):
        try:
            self.client.connect(self.addr)
            return pickle.loads(self.client.recv(2048*8))
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048*8))
        except socket.error as e:
            print(e)