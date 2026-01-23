import socket
from _thread import *
import sys

#192.168.56.1 , ip adress numero 1
#192.168.2.139 , ip adress numero 2

server = "192.168.56.1"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try :
    s.bind((server, port))
except socket.error as  e:
    str(e)
    
s.listen(4)
print ("waiting for a connection, server started")

def threaded_connection(conn) :
    reply = ""
    while True :
        try :
            data = conn.rcv(2048)
            reply = data.decode("uth-8")
            if not data :
                
                print ("Disconnected")
                break
            else :
                print ("Received : ", reply)
                print ("Sending : ", reply)
            conn.sendall(str.encode(reply))
        except :
            break
                
while True :
    conn, addr = s.accept()
    pritn("Connected to :", addr)
    
    start_new_thread (threaded_client, (conn,))