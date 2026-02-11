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

def calculate_probability(table, deck) :
    reset_proba()
    if len(table) == 3 :
        return proba_flop(table, deck)
    if len(table) == 4 :
        return proba_turn(table, deck)
    return proba_river(table, deck)

def proba_flop (table, deck) :
    
    table_copy = table.copy()
    table_copy.append(deck[0])
    table_copy.append(deck[1])
    hand = ["02p", "03p"]
    for card3 in deck :
        hand[0] = card3
        for card4 in deck :
            hand[1] = card4
            for card2 in deck :
                table_copy[3] = card2
                for card in deck :

                    table_copy[4] = card
                    combo = combinations(hand, table_copy)

                    if combo >= 1 :
                        proba_table[combo] += 1
                    proba_table["total"] += 1

    return proba_table

def proba_turn (table, deck) :

    table_copy = table.copy()
    table_copy.append(deck[0])
    hand = ["02p", "03p"]
    for card3 in deck :
        hand[0] = card3
        for card4 in deck :
            hand[1] = card4

            for card in deck :

                table[4] = card
                combo = combinations(hand, table_copy)

                if combo >= 1 :
                    proba_table[combo] += 1
                proba_table["total"] += 1

    return proba_table

def proba_river (table, deck) :

    hand = ["02p", "03p"]

    for card3 in deck :
        hand[0] = card3
        for card4 in deck :
            hand[1] = card4
            combo = combinations(hand, table)

            if combo >= 1 :
                proba_table[combo] += 1
            proba_table["total"] += 1
    return proba_table

def get_inferior_proba(probabilities, combo) :
    proba = 0
    for i in range(9) :
        if i + 1 < combo :
            proba += probabilities[i + 1]
    return proba / probabilities["total"]
            
def get_superior_proba(probabilities, combo) :
    proba = 0
    for i in range(9) :
        if i + 1 > combo :
            proba += probabilities[i + 1]
    return proba / probabilities["total"]
            

# print(calculate_probability(["02p", "03p"], ["10c", "02k", "02t"], ["02c", "05c", "07c", "09c", "10c", "11c", "12c", "13c"]))