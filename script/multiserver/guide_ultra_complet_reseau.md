# 🎴 GUIDE ULTRA-COMPLET : Réseau Multijoueur pour Poker

## 📚 TABLE DES MATIÈRES

1. [Concepts Fondamentaux](#1-concepts-fondamentaux)
2. [Architecture Globale](#2-architecture-globale)
3. [Anatomie du Code : Chaque Fonction Expliquée](#3-anatomie-du-code)
4. [Timeline d'une Partie Complète](#4-timeline-dune-partie)
5. [Flux de Données Détaillé](#5-flux-de-données)
6. [Gestion des Erreurs](#6-gestion-des-erreurs)
7. [Exercices Pratiques](#7-exercices-pratiques)

---

## 1. CONCEPTS FONDAMENTAUX

### 1.1 Socket : Qu'est-ce que c'est ?

Un **socket** = une prise électrique pour connecter deux ordinateurs.

```python
import socket

# Créer un socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#                    ↑              ↑
#                 IPv4          TCP (fiable)
```

**Vocabulaire :**
- `AF_INET` : famille d'adresses Internet (IPv4)
- `SOCK_STREAM` : type de communication en flux continu (TCP)
- TCP vs UDP : TCP garantit que les données arrivent dans l'ordre (important pour un jeu !)

**Analogie :** 
- Socket = téléphone
- `bind()` = choisir ton numéro de téléphone
- `listen()` = attendre qu'on t'appelle
- `connect()` = appeler quelqu'un
- `send()`/`recv()` = parler/écouter

### 1.2 Pickle : Sérialisation d'Objets

**Problème :** Tu ne peux pas envoyer un dictionnaire Python directement sur le réseau.
**Solution :** Pickle transforme des objets Python en bytes (et vice-versa).

```python
import pickle

# Objet Python → bytes
data = {'pot': 100, 'max_bet': 20}
bytes_data = pickle.dumps(data)  # dumps = "dump string" (en bytes)
# bytes_data = b'\x80\x04\x95...'  ← Données binaires

# bytes → Objet Python
received_data = pickle.loads(bytes_data)  # loads = "load string"
# received_data = {'pot': 100, 'max_bet': 20}  ← Dictionnaire normal
```

**⚠️ Attention :** Pickle ne peut pas sérialiser certains objets Pygame (surfaces, images).

### 1.3 Threading : Exécution Parallèle

Un **thread** = un fil d'exécution parallèle dans ton programme.

```python
from threading import Thread

def fonction_longue():
    for i in range(1000):
        print(i)

# Sans thread : bloque tout le programme
fonction_longue()  # ❌ Pygame se fige !

# Avec thread : s'exécute en arrière-plan
thread = Thread(target=fonction_longue)
thread.start()  # ✅ Pygame continue de tourner
```

**Pourquoi c'est essentiel pour le réseau ?**
- `conn.recv()` est **bloquant** : il attend jusqu'à recevoir des données
- Si tu l'appelles dans le thread principal → Pygame se fige
- Solution : mettre `recv()` dans un thread séparé

### 1.4 Lock (Verrou) : Éviter les Conflits

**Problème :** Deux threads modifient `pot` en même temps.

```python
# Thread 1                    # Thread 2
pot = 100                     pot = 100
pot += 50  # pot = 150        pot += 30  # pot = 130 ❌ (devrait être 180 !)
```

**Solution :** Utiliser un verrou (`Lock`).

```python
from threading import Lock

lock = Lock()

# Thread 1
with lock:  # Acquiert le verrou
    pot += 50
# Relâche automatiquement le verrou

# Thread 2 doit ATTENDRE que Thread 1 finisse
with lock:
    pot += 30
# Maintenant pot = 180 ✅
```

---

## 2. ARCHITECTURE GLOBALE

### 2.1 Schéma d'Ensemble

```
┌─────────────────────────────────────────────────────────────────┐
│                        SERVEUR (1 machine)                       │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  PokerServer                                               │ │
│  │  ├─ game_state (GameState)                                │ │
│  │  │  ├─ players = [...]                                    │ │
│  │  │  ├─ board = []                                         │ │
│  │  │  ├─ pot = 0                                            │ │
│  │  │  └─ active_player_index = 0                           │ │
│  │  ├─ lock (Lock) ← pour synchroniser                       │ │
│  │  ├─ clients = [conn1, conn2, conn3]                       │ │
│  │  └─ handle_client() ← 1 thread par joueur                │ │
│  └────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                          ↑          ↑          ↑
                          │          │          │
                  ┌───────┘          │          └───────┐
                  │                  │                  │
          ┌───────▼──────┐   ┌──────▼──────┐   ┌──────▼──────┐
          │  CLIENT 1    │   │  CLIENT 2   │   │  CLIENT 3   │
          │ ┌──────────┐ │   │ ┌─────────┐ │   │ ┌─────────┐ │
          │ │ Network  │ │   │ │ Network │ │   │ │ Network │ │
          │ │ player_id│ │   │ │player_id│ │   │ │player_id│ │
          │ │    = 0   │ │   │ │   = 1   │ │   │ │   = 2   │ │
          │ └──────────┘ │   │ └─────────┘ │   │ └─────────┘ │
          │ ┌──────────┐ │   │ ┌─────────┐ │   │ ┌─────────┐ │
          │ │ Table    │ │   │ │ Table   │ │   │ │ Table   │ │
          │ │ (local)  │ │   │ │ (local) │ │   │ │ (local) │ │
          │ └──────────┘ │   │ └─────────┘ │   │ └─────────┘ │
          └──────────────┘   └─────────────┘   └─────────────┘
```

### 2.2 Qui Fait Quoi ?

| Composant | Rôle | Exemples |
|-----------|------|----------|
| **GameState** | Stocke l'état du jeu | `pot`, `board`, `players` |
| **PokerServer** | Gère la logique métier | Valider mises, distribuer cartes |
| **Network** | Communique avec serveur | Envoyer actions, recevoir état |
| **Table** | Affiche le jeu | Dessiner cartes, animations |

**Règle d'or :** Le serveur est le **maître**, les clients sont des **miroirs**.

---

## 3. ANATOMIE DU CODE : Chaque Fonction Expliquée

### 3.1 GameState (game_state.py)

#### `__init__(self)`

```python
def __init__(self):
    self.players = []  # Liste de dictionnaires
    self.board = []    # ['02p', '13k', ...]
    self.pot = 0
    self.max_bet = 0
    self.active_player_index = 0
    self.phase = 'shuffle'
    self.deck = []
```

**Quand appelée ?** Au démarrage du serveur.

**Données stockées :**
- `players` : exemple `[{'chips': 2000, 'folded': False, 'hand': ['02p', '13k']}, ...]`
- `board` : cartes communes visibles
- `pot` : somme totale des mises
- `phase` : 'shuffle' → 'distribution' → 'player' → 'board_generation'

#### `to_dict(self)`

```python
def to_dict(self):
    return {
        'players': self.players,
        'board': self.board,
        'pot': self.pot,
        'max_bet': self.max_bet,
        'active_player_index': self.active_player_index,
        'phase': self.phase
    }
```

**Quand appelée ?** Avant d'envoyer l'état aux clients.

**Pourquoi ?** Pickle peut sérialiser un dictionnaire facilement.

**Exemple :**
```python
state = GameState()
state.pot = 150
data_to_send = state.to_dict()  # {'pot': 150, ...}
bytes_to_send = pickle.dumps(data_to_send)
conn.send(bytes_to_send)  # Envoyé sur le réseau
```

#### `from_dict(data)` (méthode statique)

```python
@staticmethod
def from_dict(data):
    state = GameState()
    state.players = data['players']
    state.board = data['board']
    # ... (assigner tous les champs)
    return state
```

**Quand appelée ?** Quand le client reçoit un état du serveur (optionnel, on peut utiliser directement le dict).

**`@staticmethod` expliqué :**
- Méthode qui n'a pas besoin de `self`
- S'appelle avec `GameState.from_dict(data)` au lieu de `instance.from_dict(data)`

---

### 3.2 PokerServer (server_improved.py)

#### `__init__(self)`

```python
def __init__(self):
    self.game_state = GameState()
    self.lock = Lock()  # Verrou pour éviter conflits
    self.clients = []   # Liste des connexions socket
```

**Quand appelée ?** Une seule fois au démarrage du serveur.

**Attributs :**
- `game_state` : instance unique partagée
- `lock` : permet qu'un seul thread modifie `game_state` à la fois
- `clients` : pour broadcaster les mises à jour

#### `process_action(player_id, action)`

```python
def process_action(self, player_id, action):
    with self.lock:  # Acquérir le verrou
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
        
        self.next_player()
        
        return self.game_state.to_dict()
```

**Quand appelée ?** Quand un client envoie une action (bet, fold, call).

**Paramètres :**
- `player_id` : 0, 1, 2 (quel joueur agit)
- `action` : `{'type': 'bet', 'amount': 50}`

**Déroulement :**
1. Acquiert le verrou (`with self.lock`)
2. Vérifie le type d'action
3. Modifie `game_state` en conséquence
4. Passe au joueur suivant
5. Retourne l'état mis à jour

**Exemple concret :**
```python
# Joueur 1 mise 50
action = {'type': 'bet', 'amount': 50}
new_state = server.process_action(player_id=1, action=action)
# new_state = {'pot': 50, 'players': [{'chips': 2000}, {'chips': 1950}], ...}
```

#### `next_player(self)`

```python
def next_player(self):
    self.game_state.active_player_index += 1
    if self.game_state.active_player_index >= len(self.game_state.players):
        self.game_state.active_player_index = 0
        if self.game_state.phase == 'player':
            self.game_state.phase = 'board_generation'
```

**Quand appelée ?** Après chaque action validée.

**Logique :**
- Incrémente l'index du joueur actif
- Si on dépasse le dernier joueur → retour au premier
- Si tous les joueurs ont joué ce tour → passe à la phase suivante

#### `broadcast_state(self)`

```python
def broadcast_state(self):
    state_data = self.game_state.to_dict()
    for conn in self.clients[:]:  # [:] = copie de la liste
        try:
            conn.sendall(pickle.dumps(state_data))
        except:
            self.clients.remove(conn)  # Enlever clients déconnectés
```

**Quand appelée ?** Après chaque modification de `game_state`.

**Pourquoi `self.clients[:]` ?**
- Crée une **copie** de la liste
- Permet de supprimer des clients pendant l'itération sans erreur

**Déroulement :**
1. Convertit `game_state` en dictionnaire
2. Pour chaque client connecté :
   - Sérialise avec pickle
   - Envoie via `sendall()`
   - Si erreur → déconnexion, on l'enlève

#### `handle_client(conn, player_id)`

```python
def handle_client(self, conn, player_id):
    # 1. Envoyer l'ID du joueur
    conn.send(pickle.dumps(player_id))
    self.clients.append(conn)
    
    # 2. Envoyer l'état initial
    conn.sendall(pickle.dumps(self.game_state.to_dict()))
    
    # 3. Boucle d'écoute
    while True:
        try:
            data = pickle.loads(conn.recv(2048*8))
            if not data:
                break
            
            # Traiter l'action
            new_state = self.process_action(player_id, data)
            
            # Broadcaster à tous
            self.broadcast_state()
            
        except Exception as e:
            print(f"Erreur client {player_id}: {e}")
            break
    
    # 4. Nettoyage à la déconnexion
    self.clients.remove(conn)
    conn.close()
```

**Quand appelée ?** Dès qu'un client se connecte (dans un thread séparé).

**Phases :**
1. **Handshake** : envoyer l'ID au client
2. **État initial** : synchroniser le nouveau joueur
3. **Boucle infinie** : écouter les actions du joueur
4. **Déconnexion** : nettoyer les ressources

**Pourquoi `conn.recv(2048*8)` ?**
- `2048*8 = 16384 bytes` : taille max du buffer
- Si les données dépassent, elles seront coupées (augmente si nécessaire)

#### `start(self)`

```python
def start(self):
    server = "192.168.1.17"
    port = 5555
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((server, port))  # Attacher le socket à cette adresse
    s.listen(4)  # Accepter jusqu'à 4 connexions en attente
    
    print(f"🎴 Serveur de poker démarré sur {server}:{port}")
    
    current_player = 0
    while True:
        conn, addr = s.accept()  # Bloque jusqu'à ce qu'un client se connecte
        print(f"✅ Nouveau joueur connecté: {addr}")
        start_new_thread(self.handle_client, (conn, current_player))
        current_player += 1
```

**Quand appelée ?** Point d'entrée du serveur.

**Déroulement :**
1. Créer un socket TCP
2. `bind()` : lier à l'IP et au port
3. `listen()` : démarrer l'écoute
4. Boucle infinie :
   - `accept()` bloque jusqu'à connexion
   - Créer un thread pour gérer le client
   - Incrémenter l'ID du joueur

**Pourquoi `start_new_thread` ?**
- Chaque client a son propre thread
- Permet de gérer plusieurs clients simultanément

---

### 3.3 Network (network_improved.py)

#### `__init__(self, on_state_update)`

```python
def __init__(self, on_state_update):
    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.server = "192.168.1.17"
    self.port = 5555
    self.addr = (self.server, self.port)
    self.player_id = None
    self.on_state_update = on_state_update  # Callback
    self.running = True
```

**Paramètres :**
- `on_state_update` : fonction à appeler quand l'état change

**Exemple d'utilisation :**
```python
def ma_fonction_callback(state_data):
    print(f"Pot mis à jour: {state_data['pot']}")

network = Network(on_state_update=ma_fonction_callback)
```

#### `connect(self)`

```python
def connect(self):
    try:
        self.client.connect(self.addr)  # Se connecter au serveur
        self.player_id = pickle.loads(self.client.recv(2048*8))  # Recevoir l'ID
        print(f"✅ Connecté en tant que joueur {self.player_id}")
        
        # Démarrer thread d'écoute
        Thread(target=self.receive_loop, daemon=True).start()
        return True
    except Exception as e:
        print(f"❌ Erreur connexion: {e}")
        return False
```

**Quand appelée ?** Au démarrage du client.

**Déroulement :**
1. Se connecter au serveur
2. Recevoir son `player_id`
3. Lancer le thread d'écoute

**`daemon=True` expliqué :**
- Thread "démon" : se ferme automatiquement quand le programme principal se termine
- Sans `daemon=True` : le programme reste ouvert même après fermeture de Pygame

#### `receive_loop(self)`

```python
def receive_loop(self):
    while self.running:
        try:
            state_data = pickle.loads(self.client.recv(2048*8))
            # Appeler le callback avec le nouvel état
            self.on_state_update(state_data)
        except Exception as e:
            print(f"❌ Erreur réception: {e}")
            break
```

**Quand appelée ?** En continu dans un thread séparé.

**Fonctionnement :**
1. `recv()` bloque jusqu'à recevoir des données
2. Désérialiser avec pickle
3. Appeler le callback pour mettre à jour l'interface

**Exemple de flux :**
```
[Thread d'écoute]                [Thread principal Pygame]
recv() ← attend...               draw()
                                 update()
                                 draw()
recv() ← reçoit état             update()
on_state_update(state)    →      Table.pot = state['pot']
recv() ← attend...               draw() ← affiche nouveau pot
```

#### `send_action(action_type, **kwargs)`

```python
def send_action(self, action_type, **kwargs):
    action = {'type': action_type, **kwargs}
    try:
        self.client.send(pickle.dumps(action))
    except Exception as e:
        print(f"❌ Erreur envoi: {e}")
```

**Paramètres :**
- `action_type` : 'bet', 'fold', 'call', 'raise'
- `**kwargs` : arguments supplémentaires (comme `amount=50`)

**Exemple :**
```python
network.send_action('bet', amount=50)
# Équivalent à envoyer {'type': 'bet', 'amount': 50}
```

**`**kwargs` expliqué :**
```python
def ma_fonction(**kwargs):
    print(kwargs)  # {'a': 1, 'b': 2}

ma_fonction(a=1, b=2)
```

#### `disconnect(self)`

```python
def disconnect(self):
    self.running = False  # Arrêter la boucle d'écoute
    self.client.close()
```

**Quand appelée ?** Quand le joueur quitte.

---

## 4. TIMELINE D'UNE PARTIE COMPLÈTE

### 4.1 Phase 1 : Démarrage du Serveur

```
┌──────────────────────────────────────────┐
│ Terminal : python server_improved.py     │
└──────────────────────────────────────────┘
           ↓
    PokerServer.__init__()
           ↓
    game_state = GameState()
    game_state.phase = 'shuffle'
    game_state.players = []
           ↓
    start()
           ↓
    socket.bind(("192.168.1.17", 5555))
    socket.listen(4)
           ↓
    print("🎴 Serveur démarré")
           ↓
    while True: accept() ← ATTEND des connexions
```

**État du serveur :**
```python
{
    'players': [],
    'board': [],
    'pot': 0,
    'max_bet': 0,
    'active_player_index': 0,
    'phase': 'shuffle'
}
```

### 4.2 Phase 2 : Connexion du Joueur 1

```
┌──────────────────────────────────────────┐
│ Client 1 : python main.py                │
└──────────────────────────────────────────┘
           ↓
    network = Network(on_state_update=callback)
    network.connect()
           ↓
    client.connect(("192.168.1.17", 5555))
           ↓
           
    ┌─────────────────────────────────────┐
    │ SERVEUR                             │
    ├─────────────────────────────────────┤
    │ s.accept() → conn, addr             │
    │ start_new_thread(handle_client,     │
    │                  (conn, 0))         │
    └─────────────────────────────────────┘
           ↓
    handle_client(conn, player_id=0)
           ↓
    conn.send(pickle.dumps(0))  ← Envoyer ID
           ↓
           
    ┌─────────────────────────────────────┐
    │ CLIENT 1                            │
    ├─────────────────────────────────────┤
    │ player_id = pickle.loads(recv())    │
    │ player_id = 0 ✅                    │
    │ Thread(receive_loop).start()        │
    └─────────────────────────────────────┘
           ↓
    handle_client() → clients.append(conn)
                   → sendall(game_state)
           ↓
           
    ┌─────────────────────────────────────┐
    │ CLIENT 1 - receive_loop()           │
    ├─────────────────────────────────────┤
    │ state = pickle.loads(recv())        │
    │ on_state_update(state)              │
    │   ↓                                 │
    │ Table.pot = state['pot']            │
    │ Table.board = state['board']        │
    └─────────────────────────────────────┘
```

**État mis à jour (serveur ajoute joueur 1) :**
```python
{
    'players': [
        {'chips': 2000, 'folded': False, 'hand': []}
    ],
    'board': [],
    'pot': 0,
    'max_bet': 0,
    'active_player_index': 0,
    'phase': 'shuffle'
}
```

### 4.3 Phase 3 : Connexion des Joueurs 2 & 3

**Même processus pour chaque joueur :**

```
CLIENT 2 connecté → player_id = 1
CLIENT 3 connecté → player_id = 2
```

**État final après 3 connexions :**
```python
{
    'players': [
        {'chips': 2000, 'folded': False, 'hand': []},  # Joueur 0
        {'chips': 2000, 'folded': False, 'hand': []},  # Joueur 1
        {'chips': 2000, 'folded': False, 'hand': []}   # Joueur 2
    ],
    'board': [],
    'pot': 0,
    'max_bet': 0,
    'active_player_index': 0,
    'phase': 'shuffle'
}
```

### 4.4 Phase 4 : Mélange & Distribution

**⚠️ À implémenter dans `process_action()` :**

```python
# Quand phase = 'shuffle'
elif action['type'] == 'start_game':
    random.shuffle(self.game_state.deck)
    
    # Distribuer 2 cartes à chaque joueur
    for i, player in enumerate(self.game_state.players):
        player['hand'] = [
            self.game_state.deck.pop(),
            self.game_state.deck.pop()
        ]
    
    self.game_state.phase = 'player'
```

**Timeline :**
```
SERVEUR : shuffle deck
       ↓
   distribute cards
       ↓
   game_state.phase = 'player'
       ↓
   broadcast_state()
       ↓
CLIENTS : receive_loop()
       ↓
   on_state_update(state)
       ↓
   Afficher les cartes
```

### 4.5 Phase 5 : Tour de Jeu (Joueur 0)

```
┌─────────────────────────────────────────────────────────────┐
│ CLIENT 0 - Interface                                        │
├─────────────────────────────────────────────────────────────┤
│ Joueur clique sur "BET 50"                                  │
│    ↓                                                        │
│ network.send_action('bet', amount=50)                       │
│    ↓                                                        │
│ client.send(pickle.dumps({'type': 'bet', 'amount': 50}))   │
└─────────────────────────────────────────────────────────────┘
           ↓ (envoi réseau)
┌─────────────────────────────────────────────────────────────┐
│ SERVEUR - handle_client() thread 0                         │
├─────────────────────────────────────────────────────────────┤
│ data = pickle.loads(conn.recv())                            │
│ data = {'type': 'bet', 'amount': 50}                        │
│    ↓                                                        │
│ process_action(player_id=0, action=data)                    │
│    ↓                                                        │
│ with lock:  ← VERROU                                       │
│    pot += 50                                                │
│    players[0]['chips'] -= 50                                │
│    max_bet = 50                                             │
│    next_player()                                            │
│       ↓                                                     │
│    active_player_index = 1                                  │
│    ↓                                                        │
│ broadcast_state()                                           │
│    ↓                                                        │
│ for conn in [conn0, conn1, conn2]:                          │
│    conn.sendall(pickle.dumps(new_state))                    │
└─────────────────────────────────────────────────────────────┘
           ↓ (envoi à tous les clients)
┌──────────────┬──────────────┬──────────────┐
│  CLIENT 0    │  CLIENT 1    │  CLIENT 2    │
├──────────────┼──────────────┼──────────────┤
│ receive_loop │ receive_loop │ receive_loop │
│      ↓       │      ↓       │      ↓       │
│ state = recv │ state = recv │ state = recv │
│      ↓       │      ↓       │      ↓       │
│ callback()   │ callback()   │ callback()   │
│      ↓       │      ↓       │      ↓       │
│ pot = 50     │ pot = 50     │ pot = 50     │
│ actif = 1    │ actif = 1 ✅ │ actif = 1    │
└──────────────┴──────────────┴──────────────┘
```

**État après l'action :**
```python
{
    'players': [
        {'chips': 1950, 'folded': False},  # -50
        {'chips': 2000, 'folded': False},
        {'chips': 2000, 'folded': False}
    ],
    'pot': 50,  # ✅
    'max_bet': 50,
    'active_player_index': 1,  # ✅ Tour du joueur 1
    'phase': 'player'
}
```

### 4.6 Phase 6 : Tour de Jeu (Joueur 1)

**Joueur 1 fait CALL :**

```
CLIENT 1 : send_action('call')
    ↓
SERVEUR : process_action(player_id=1, {'type': 'call'})
    ↓
    with lock:
        pot += max_bet  (50)
        players[1]['chips'] -= 50
        next_player()
    ↓
    broadcast_state()
    ↓
TOUS LES CLIENTS : pot = 100, actif = 2
```

### 4.7 Phase 7 : Fin du Tour

**Tous les joueurs ont joué → Passer au Flop**

```python
# Dans next_player()
if active_player_index >= len(players):
    active_player_index = 0
    
    if phase == 'player':
        # Générer le flop
        board = [deck.pop(), deck.pop(), deck.pop()]
        phase = 'board_generation'
```

**État après flop :**
```python
{
    'players': [...],
    'board': ['02p', '13k', '07c'],  # ✅ Flop visible
    'pot': 150,
    'max_bet': 0,  # Reset pour le nouveau tour
    'active_player_index': 0,
    'phase': 'player'  # Nouveau tour de mises
}
```

---

## 5. FLUX DE DONNÉES DÉTAILLÉ

### 5.1 Action du Joueur → Broadcast

```
┌─────────────┐
│ CLIENT 0    │
│ Clique BET  │
└──────┬──────┘
       │ send({'type': 'bet', 'amount': 50})
       ↓
┌──────────────────────────────────────┐
│ SERVEUR - Thread 0                   │
│ ┌──────────────────────────────────┐ │
│ │ recv() débloqué                  │ │
│ │  ↓                               │ │
│ │ process_action()                 │ │
│ │  ↓                               │ │
│ │ with lock:  ← CRITIQUE           │ │
│ │    game_state.pot += 50          │ │
│ │    game_state.players[0] -= 50   │ │
│ │  ↓                               │ │
│ │ return new_state                 │ │
│ └──────────────────────────────────┘ │
│ ┌──────────────────────────────────┐ │
│ │ broadcast_state()                │ │
│ │  ↓                               │ │
│ │ for conn in clients:             │ │
│ │    sendall(new_state)            │ │
│ └──────────────────────────────────┘ │
└──────────────────────────────────────┘
       │           │           │
       ↓           ↓           ↓
┌──────────┐ ┌──────────┐ ┌──────────┐
│ CLIENT 0 │ │ CLIENT 1 │ │ CLIENT 2 │
│ recv()   │ │ recv()   │ │ recv()   │
│  ↓       │ │  ↓       │ │  ↓       │
│ update() │ │ update() │ │ update() │
└──────────┘ └──────────┘ └──────────┘
```

### 5.2 Gestion de Collision (Lock)

**Scénario SANS lock (❌ MAUVAIS) :**

```
TEMPS    THREAD 0 (Joueur 0)         THREAD 1 (Joueur 1)
------   ---------------------        ---------------------
t=0      recv({'type': 'bet'})        
t=1      pot = 100                    
t=2      pot += 50  (pot = 150)       recv({'type': 'bet'})
t=3                                   pot = 100 ❌ (lit ancienne valeur)
t=4                                   pot += 30  (pot = 130) ❌
t=5      sendall(pot=150)             
t=6                                   sendall(pot=130) ❌
         
RÉSULTAT : pot = 130 au lieu de 180 !
```

**Avec lock (✅ BON) :**

```
TEMPS    THREAD 0 (Joueur 0)         THREAD 1 (Joueur 1)
------   ---------------------        ---------------------
t=0      recv({'type': 'bet'})        
t=1      with lock:  ← ACQUIERT       
t=2         pot += 50                 recv({'type': 'bet'})
t=3      ← RELÂCHE LOCK               with lock:  ← ATTEND...
t=4                                   ← ACQUIERT
t=5      sendall(pot=150)             pot += 30
t=6                                   ← RELÂCHE
t=7                                   sendall(pot=180) ✅
         
RÉSULTAT : pot = 180 ✅
```

---

## 6. GESTION DES ERREURS

### 6.1 Client Déconnecté Brutalement

**Problème :** Joueur ferme le jeu sans prévenir.

```python
# Dans handle_client()
while True:
    try:
        data = pickle.loads(conn.recv(2048*8))
        if not data:  # Connexion fermée proprement
            break
    except Exception as e:
        print(f"❌ Client {player_id} déconnecté : {e}")
        break

# Nettoyage
self.clients.remove(conn)
self.game_state.players[player_id]['connected'] = False
self.broadcast_state()  # Informer les autres
```

### 6.2 Données Corrompues

```python
# Dans receive_loop()
try:
    state_data = pickle.loads(self.client.recv(2048*8))
except pickle.UnpicklingError:
    print("❌ Données corrompues reçues")
    continue  # Ignorer et attendre le prochain paquet
```

### 6.3 Timeout de Connexion

```python
# Dans Network.connect()
self.client.settimeout(5)  # 5 secondes max
try:
    self.client.connect(self.addr)
except socket.timeout:
    print("❌ Serveur ne répond pas")
    return False
```

### 6.4 Validation des Actions

```python
# Dans process_action()
def process_action(self, player_id, action):
    with self.lock:
        # Vérifier que c'est le bon joueur
        if player_id != self.game_state.active_player_index:
            print(f"❌ Joueur {player_id} joue hors tour !")
            return self.game_state.to_dict()  # Renvoyer état inchangé
        
        # Vérifier que le joueur a assez de chips
        if action['type'] == 'bet':
            if action['amount'] > self.game_state.players[player_id]['chips']:
                print(f"❌ Joueur {player_id} n'a pas assez de chips")
                return self.game_state.to_dict()
        
        # Action valide → continuer
        # ...
```

---

## 7. EXERCICES PRATIQUES

### Exercice 1 : Ajouter l'Action RAISE

**Objectif :** Permettre aux joueurs de relancer.

```python
# Dans process_action()
elif action['type'] == 'raise':
    amount = action['amount']
    
    # Vérifications
    if amount <= self.game_state.max_bet:
        print("❌ Relance doit être > max_bet")
        return self.game_state.to_dict()
    
    # Appliquer
    self.game_state.pot += amount
    self.game_state.players[player_id]['chips'] -= amount
    self.game_state.max_bet = amount
    self.next_player()
```

**Côté client :**
```python
# Dans player.py
def action_raise(self, table):
    self.placing_a_bet = True
    # (utiliser le slider existant)
```

### Exercice 2 : Détecter la Fin de Partie

**Objectif :** Identifier le gagnant quand la river est passée.

```python
# Dans process_action()
def check_winner(self):
    if len(self.game_state.board) == 5:  # River complète
        best_combo = -1
        winner_id = -1
        
        for i, player in enumerate(self.game_state.players):
            if not player['folded']:
                combo = combinations(player['hand'], self.game_state.board)
                if combo > best_combo:
                    best_combo = combo
                    winner_id = i
        
        # Attribuer le pot
        self.game_state.players[winner_id]['chips'] += self.game_state.pot
        self.game_state.pot = 0
        self.game_state.phase = 'game_over'
```

### Exercice 3 : Ajouter un Chat

**Objectif :** Permettre aux joueurs de discuter.

```python
# Ajouter dans GameState
self.chat_messages = []

# Nouvelle action
elif action['type'] == 'chat':
    message = f"Joueur {player_id}: {action['message']}"
    self.game_state.chat_messages.append(message)
    # Pas besoin de next_player() pour le chat
```

**Côté client :**
```python
# Dans Network
def send_chat(self, message):
    self.send_action('chat', message=message)

# Dans on_state_update
def on_game_state_updated(self, state_data):
    # ...
    for msg in state_data['chat_messages']:
        print(msg)
```

---

## 📝 CHECKLIST FINALE

### Avant de Tester

- [ ] Le serveur est lancé AVANT les clients
- [ ] L'IP dans `network.py` correspond au serveur
- [ ] Le port 5555 n'est pas bloqué par le firewall
- [ ] `pickle` et `socket` sont bien importés
- [ ] Les threads sont marqués `daemon=True`

### Debug

```python
# Ajouter des logs partout
import logging
logging.basicConfig(level=logging.DEBUG)

# Dans server
logging.debug(f"Action reçue: {action}")
logging.debug(f"État après action: {self.game_state.to_dict()}")

# Dans client
logging.debug(f"Envoi action: {action}")
logging.debug(f"Réception état: {state_data}")
```

### Test en Local

```bash
# Terminal 1
python server_improved.py

# Terminal 2
python main.py  # Client 1

# Terminal 3
python main.py  # Client 2
```

---

## 🎓 CONCEPTS CLÉS À RETENIR

1. **Serveur = Source de vérité** : toute logique métier est sur le serveur
2. **Clients = Miroirs** : ils affichent et envoient des actions
3. **Lock = Protection** : évite les conflits entre threads
4. **Pickle = Sérialisation** : convertit objets ↔ bytes
5. **Threads = Parallélisme** : écoute réseau sans bloquer Pygame

---

Bon courage ! 🚀
