from determine_hand_strength import Hand

def determine_community_strength_four(community):

# Changing values of aces to 14
    for card in community:
        if card['rank'] == '1':
            card['rank'] = '14'

    suits = [card['suit'] for card in community] #list of all suits in the full hand

    ranks = [card['rank'] for card in community] # list of all ranks in full hand

    hand = Hand(community, ranks, suits)

    is_four_of_a_kind = hand.isFourOfAKind()
    is_three_of_a_kind = hand.isThreeOfAKind()
    is_two_pair = hand.isTwoPair()
    is_pair = hand.isPair()


    if is_four_of_a_kind[0]:
        return is_four_of_a_kind[1:3]
    
    elif is_three_of_a_kind[0]:
        return is_three_of_a_kind[1:]
    
    elif is_two_pair[0]:
        return is_two_pair[1:3]
    
    elif is_pair[0]:
        return is_pair[1:]
    
    else:
        return ['1']

