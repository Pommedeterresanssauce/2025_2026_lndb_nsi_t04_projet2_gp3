def represent_cards(hand, table) :

    card_representation = { 'p' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            'c' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            't' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            'k' : [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]}
    for card in hand :
        card_representation[card[2]][int(card[:2]) - 1] += 1

    for card in table :
        card_representation[card[2]][int(card[:2]) - 1] += 1

    return card_representation
    

def combinations(hand, table) :

    cards = represent_cards(hand, table)

    if is_royal_flush(cards) :
        return 9

    if is_straight_flush(cards) :
        return 8

    if is_four_of_k(cards) :
        return 7

    if is_full_house(cards) :
        return 6

    if is_flush(cards) :
        return 5

    if is_straight(cards) :
        return 4

    if is_three_of_k(cards) :
        return 3

    if is_two_pair(cards) :
        return 2

    if is_pair(cards) :
        return 1
    
    return high_card(cards)

def is_pair(cards) :
    for i in range(13) :
        if cards["p"][i] + cards["c"][i] + cards["t"][i] + cards["k"][i] == 2:
            return True
    
    return False

def is_two_pair(cards) :
    number_of_pairs = 0
    for i in range(13) :
        if cards["p"][i] + cards["c"][i] + cards["t"][i] + cards["k"][i] == 2:
            number_of_pairs += 1
            if number_of_pairs == 2:
                return True
    
    return False

def is_three_of_k(cards) :
    for i in range(13) :
        if cards["p"][i] + cards["c"][i] + cards["t"][i] + cards["k"][i] == 3:
            return True
    
    return False

def is_straight(cards) :
    in_a_row = 0
    for i in range(13) :
        count = 0
        for j in cards :
            count += cards[j][i]
        if count > 0 :
            in_a_row += 1
            if in_a_row == 5 :
                return True
        else :
            in_a_row = 0
        
    if in_a_row == 4 and cards["p"][0] + cards["c"][0] + cards["t"][0] + cards["k"][0] > 0 :
        return True
        
    return False

def is_flush(cards) :
    for i in cards :
        count = 0

        for j in cards[i] :
            count += j
        if count > 4 :
            return True

    
    return False

def is_full_house(cards) :
    if is_pair(cards) and is_three_of_k(cards) :
        return True
    
    return False

def is_four_of_k(cards) :
    for i in range(13) :
        if cards["p"][i] + cards["c"][i] + cards["t"][i] + cards["k"][i] == 4:
            return True
    
    return False

def is_straight_flush(cards) :
    in_a_row = 0
    for j in cards :
        for i in cards[j] :
            if i > 0 :
                in_a_row += 1
                if in_a_row == 5 :
                    return True
            else :
                in_a_row = 0
        
    return False

def is_royal_flush(cards) :
    
    for i in cards :
        if cards[i][10] + cards[i][11] + cards[i][12] + cards[i][13] + cards[i][0] == 5 :
            return True
        
    return False

def high_card(cards) :
    for i in range(13) :
        if cards["p"][13 - i] + cards["c"][13 - i] + cards["t"][13 - i] + cards["k"][13 - i] > 0:
            return (i * 0.0099999)
        
# COMBO SPECIAUX        
        
def is_67(cards) :
    if cards["p"][5] + cards["c"][5] + cards["t"][5] + cards["k"][5] > 0 :
        if cards["p"][6] + cards["c"][6] + cards["t"][6] + cards["k"][6] > 0 :
            return True
    
    return False

def is_curve(cards) :
    in_a_row = 0
    for i in range(13) :
        count = 0
        for j in cards :
            count += cards[j][i]
        if count > 0 :
            in_a_row += 1
            if in_a_row == 4 :
                return True
        else :
            in_a_row = 0
        
    if in_a_row == 3 and cards["p"][0] + cards["c"][0] + cards["t"][0] + cards["k"][0] > 0 :
        return True
        
    return False

def is_double_triple(cards) :
    if cards["p"][1] + cards["c"][1] + cards["t"][1] + cards["k"][1] == 2 :
        if cards["p"][2] + cards["c"][2] + cards["t"][2] + cards["k"][2] == 3 :
            return True
    
    return False

def is_jackpot(cards) :
    if cards["p"][6] + cards["c"][6] + cards["t"][6] + cards["k"][6] == 3 :
        return True
    
    return False