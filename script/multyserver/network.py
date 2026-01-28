import socket

class Network :
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serveur = "192.168.56.1"
        self.port = 5555
        self.addr = (self.serveur, self.port)
        self.id = self.connect()
        print (self.id)
        
    def connect (self) :
        try :
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except :
            pass
    
    def send (self, data) :
        try :
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
            
n = Network()
print (n.send("hello"))
print (n.send("working"))