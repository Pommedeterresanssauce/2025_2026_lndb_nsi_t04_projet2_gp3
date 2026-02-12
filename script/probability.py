import random
from combinations_test import combinations

# Structure pour stocker les résultats
# 0: Hauteur, 1: Paire, 2: Double Paire, 3: Brelan, 4: Suite, 
# 5: Couleur, 6: Full, 7: Carré, 8+: Quinte Flush
proba_table = {i: 0 for i in range(0, 10)}
proba_table["total"] = 0

def reset_proba():
    """Réinitialise les compteurs de probabilités."""
    for i in range(0, 10):
        proba_table[i] = 0
    proba_table["total"] = 0

def calculate_probability(board, deck_cards, iterations=1000):
    """
    Calcule les probabilités en utilisant la simulation de Monte Carlo 
    pour éviter les boucles infinies et les lags.
    
    Retourne un dictionnaire avec les probabilités pour chaque combinaison.
    """
    reset_proba()
    
    # On détermine combien de cartes il manque sur le board (max 5)
    cards_needed_on_board = 5 - len(board)
    
    for _ in range(iterations):
        # 1. On mélange une copie du deck pour simuler un tirage
        sim_deck = deck_cards.copy()
        random.shuffle(sim_deck)
        
        # 2. On pioche 2 cartes pour l'adversaire imaginaire
        opponent_hand = [sim_deck.pop(), sim_deck.pop()]
        
        # 3. On complète le board si nécessaire (Turn ou River manquants)
        sim_board = board.copy()
        for _ in range(cards_needed_on_board):
            sim_board.append(sim_deck.pop())
            
        # 4. On évalue la force de la main adverse possible
        combo = combinations(opponent_hand, sim_board)
        combo_rank = combo[0]  # Le premier élément du tuple est le rang de la combinaison
        
        proba_table[combo_rank] += 1
        proba_table["total"] += 1

    return proba_table

def get_inferior_proba(probabilities, my_combo):
    """
    Calcule la probabilité que l'adversaire ait une main moins forte que nous.
    my_combo est un tuple (rank, ...) où rank est le rang de la combinaison.
    """
    if probabilities["total"] == 0: 
        return 0
    
    my_rank = my_combo[0]  # Le rang de ma combinaison
    count = 0
    
    for i in range(0, 10):
        if i < my_rank:
            count += probabilities[i]
    
    return count / probabilities["total"]

def get_superior_proba(probabilities, my_combo):
    """
    Calcule la probabilité que l'adversaire ait une main plus forte que nous.
    my_combo est un tuple (rank, ...) où rank est le rang de la combinaison.
    """
    if probabilities["total"] == 0: 
        return 0
    
    my_rank = my_combo[0]  # Le rang de ma combinaison
    count = 0
    
    for i in range(0, 10):
        if i > my_rank:
            count += probabilities[i]
    
    return count / probabilities["total"]

def get_equal_proba(probabilities, my_combo):
    """
    Calcule la probabilité que l'adversaire ait une main égale à la nôtre.
    """
    if probabilities["total"] == 0: 
        return 0
    
    my_rank = my_combo[0]
    
    if my_rank in probabilities:
        return probabilities[my_rank] / probabilities["total"]
    
    return 0
            