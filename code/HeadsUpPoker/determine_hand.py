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

    if hand.isRoyalFlush()[0]:
        return hand.isRoyalFlush()[1:]
    
    elif hand.isStraightFlush()[0]:
        return hand.isStraightFlush()[1:]
    
    elif hand.isFourOfAKind()[0]:
        return hand.isFourOfAKind()[1:]
    
    elif hand.isFullHouse()[0]:
        return hand.isFullHouse()[1:]
    
    elif hand.isFlush()[0]:
        flush_result = hand.isFlush()
        flush_result.insert(1, 6)
        return [flush_result[1], flush_result[2]]
    
    elif hand.isStraight(hand.ranks)[0]:
        return hand.isStraight(hand.ranks)[1:]
    
    elif hand.isThreeOfAKind()[0]:
        return hand.isThreeOfAKind()[1:]
    
    elif hand.isTwoPair()[0]:
        return hand.isTwoPair()[1:]
    
    elif hand.isPair()[0]:
        return hand.isPair()[1:]
    
    else:
        return hand.highest_card()
    

