import math

'''
----------------------------------{ Pre-Flop }----------------------------------
Chen formula goes up to 20, (Pair of Aces Suited).
If the chen score for the AI's starting hand is 16, there will be a 16/20 chance of the AI raising.
if not, the computer will check. 

Additionally if the AI's chen score is 0 or less on the first 5 turns, the AI will fold.
--------------------------------------------------------------------------------
'''


def chen_formula(hand):
    suits = [card['suit'] for card in hand]
    ranks = [int(card['rank']) for card in hand]
    suit_count = len(set(suits))
    max_rank, min_rank = max(ranks), min(ranks)
    is_pair = max_rank == min_rank
    card_gap = abs(max_rank - min_rank)
    score = 0


    '''
    Score your highest card only. Do not add any points for your lower card.

    A = 10 points.
    K = 8 points.
    Q = 7 points.
    J = 6 points.
    10 to 2 = 1/2 of card value. (e.g. a 6 would be worth 3 points)
    '''

    if max_rank == 14:  # Ace
        score += 10
    elif max_rank >= 13:  # King
        score += 8
    elif max_rank >= 12:  # Queen
        score += 7
    elif max_rank >= 11:  # Jack
        score += 6
    else:
        score = max_rank // 2

# Multiply pairs by 2 of one card’s value. However, minimum score for a pair is 5.
    if is_pair:
        if score > 2:
            score *= 2
        else:
            score = 5

# Add 2 points if cards are suited.
    if suit_count == 1:
        score += 2

# Subtract points if their is a gap between the two cards.
    if not is_pair:
        if card_gap == 1:
            score -= 1
        elif card_gap == 2:
            score -= 2
        elif card_gap == 3:
            score -= 4
        else:
            score -= 5

# Add 1 point if there is a 0 or 1 card gap and both cards are lower than a Q. (e.g. JT, 75, 32 etc, this bonus point does not apply to pocket pairs)
    if card_gap == 1 and max_rank < 12:
        score += 1

# Round half point scores up. (e.g. 7.5 rounds up to 8)
    return math.ceil(score)