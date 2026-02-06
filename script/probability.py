from math import*
from combinations import*

proba_table = {1 : 0,
               2 : 0,
               3 : 0,
               4 : 0,
               5 : 0,
               6 : 0,
               7 : 0,
               8 : 0,
               9 : 0,
               "total" : 0}

def reset_proba() :
    proba_table[0] = 0
    proba_table[1] = 0
    proba_table[2] = 0
    proba_table[3] = 0
    proba_table[4] = 0
    proba_table[5] = 0
    proba_table[6] = 0
    proba_table[7] = 0
    proba_table[8] = 0
    proba_table["total"] = 0

def calculate_probability(hand, table, deck) :
    reset_proba()
    if len(table) == 0 :
        return proba_preflop(hand, table, deck)
    if len(table) == 3 :
        return proba_flop(hand, table, deck)
    if len(table) == 4 :
        return proba_turn(hand, table, deck)
    return proba_river(hand, table, deck)

def proba_preflop (hand, table, deck) :
    pass

def proba_flop (hand, table, deck) :
    
    table.append(deck[0])
    table.append(deck[1])
    while len(deck) > 1 :
        table[3] = deck.pop(0)
        for card in deck :

            table[4] = card
            combo = combinations(hand, table)

            if combo >= 1 :
                proba_table[combo] += 1
            proba_table["total"] += 1

    return proba_table

def proba_turn (hand, table, deck) :
    
    table.append(deck[0])
    table.append(deck[1])
    while len(deck) > 1 :
        table[3] = deck.pop(0)
        for card in deck :

            table[4] = card
            combo = combinations(hand, table)

            if combo >= 1 :
                proba_table[combo] += 1
            proba_table["total"] += 1

    return proba_table

def proba_river (hand, table, deck) :

    table.append(deck[0])

    for card in deck :

        table[4] = card
        combo = combinations(hand, table)

        if combo >= 1 :
            proba_table[combo] += 1
        proba_table["total"] += 1

    return proba_table