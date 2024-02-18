from determine_hand_strength import Hand

'''
We'll check from strongest to weakest hand rankings, to ensure we return the strongest possible.

E.g. If a player has a Royal-Flush/Straight-Flush, check for this first to ensure we don't incorrectly return that they just have a flush or a straight.
'''

def determine_hand(pocket, community):

    full_hand = pocket + community

# Changing values of aces to 14
    for card in full_hand:
        if card['rank'] == '1':
            card['rank'] = '14'

    suits = [card['suit'] for card in full_hand] #list of all suits in the full hand

    ranks = [card['rank'] for card in full_hand] # list of all ranks in full hand

    hand = Hand(full_hand, ranks, suits)

    is_royal_flush = hand.isRoyalFlush()
    is_straight_flush = hand.isStraightFlush()
    is_four_of_a_kind = hand.isFourOfAKind()
    is_full_house = hand.isFullHouse()
    is_flush = hand.isFlush()
    is_straight = hand.isStraight(hand.ranks)
    is_three_of_a_kind = hand.isThreeOfAKind()
    is_two_pair = hand.isTwoPair()
    is_pair = hand.isPair()[0]
    is_high_card = hand.highest_card()

    if is_royal_flush[0]:
        return is_royal_flush[1:]
    
    elif is_straight_flush[0]:
        return is_straight_flush[1:]
    
    elif is_four_of_a_kind[0]:
        return is_four_of_a_kind[1:]
    
    elif is_full_house[0]:
        return is_full_house[1:]
    
    elif is_flush[0]:
        flush_result = is_flush
        flush_result.insert(1, 6)
        return [flush_result[1], flush_result[2]]
    
    elif is_straight[0]:
        return is_straight[1:]
    
    elif is_three_of_a_kind[0]:
        return is_three_of_a_kind[1:]
    
    elif is_two_pair[0]:
        return is_two_pair[1:]
    
    elif is_pair[0]:
        return is_pair[1:]
    
    else:
        return is_high_card
    

