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
    

def combinations(hand, table):

    cards = represent_cards(hand, table)

    values_count = [0]*13
    suits = {"p":[], "c":[], "t":[], "k":[]}

    for suit in cards:
        for i in range(13):
            if cards[suit][i] > 0:
                values_count[i] += cards[suit][i]
                suits[suit] += [i]*cards[suit][i]

    # liste triée des valeurs présentes
    values = []
    for i in range(13):
        values += [i]*values_count[i]

    values.sort(reverse=True)

    # -------- FOUR OF A KIND --------
    for i in range(12, -1, -1):
        if values_count[i] == 4:
            kicker = max([v for v in values if v != i])
            return (7, i, kicker)

    # -------- FULL HOUSE --------
    triple = None
    pair = None
    for i in range(12, -1, -1):
        if values_count[i] >= 3 and triple is None:
            triple = i
        elif values_count[i] >= 2 and pair is None:
            pair = i
    if triple is not None and pair is not None:
        return (6, triple, pair)

    # -------- FLUSH --------
    for suit in suits:
        if len(suits[suit]) >= 5:
            top5 = sorted(suits[suit], reverse=True)[:5]
            return (5, *top5)

    # -------- STRAIGHT --------
    unique_vals = sorted(set(values), reverse=True)
    for i in range(len(unique_vals)-4):
        if unique_vals[i] - unique_vals[i+4] == 4:
            return (4, unique_vals[i])

    # -------- THREE OF A KIND --------
    for i in range(12, -1, -1):
        if values_count[i] == 3:
            kickers = [v for v in values if v != i][:2]
            return (3, i, *kickers)

    # -------- TWO PAIR --------
    pairs = []
    for i in range(12, -1, -1):
        if values_count[i] == 2:
            pairs.append(i)
    if len(pairs) >= 2:
        kicker = max([v for v in values if v not in pairs[:2]])
        return (2, pairs[0], pairs[1], kicker)

    # -------- ONE PAIR --------
    for i in range(12, -1, -1):
        if values_count[i] == 2:
            kickers = [v for v in values if v != i][:3]
            return (1, i, *kickers)

    # -------- HIGH CARD --------
    return (0, *values[:5])
