import socket
from _thread import *
import sys
import pickle
import table as Table 

#192.168.56.1 , ip adress numero 1
#192.168.2.139 , ip adress numero 2


def threaded_client(conn, player_id, poker_game):
    conn.send(pickle.dumps(player_id))
    while True:
        try:
            data = pickle.loads(conn.recv(2048*8))
            if not data:
                print("Disconnected")
                break
            conn.sendall(pickle.dumps(poker_game))
        except:
            break

    print("Lost connection")
    conn.close()

def main():
    server = "192.168.1.17"
    port = 5555
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((server, port))
    s.listen(4)

    # On crée l'unique instance de la table ici
    poker_game = Table()
    current_player = 0

    while True:
        conn, addr = s.accept()
        # On passe poker_game directement dans les arguments du thread
        start_new_thread(threaded_client, (conn, current_player, poker_game))
        current_player += 1

main()