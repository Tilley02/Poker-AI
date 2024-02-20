from determine_hand_strength import Hand

def determine_community_strength_three(community):

# Changing values of aces to 14
    for card in community:
        if card['rank'] == '1':
            card['rank'] = '14'

    suits = [card['suit'] for card in community] #list of all suits in the full hand

    ranks = [card['rank'] for card in community] # list of all ranks in full hand

    hand = Hand(community, ranks, suits)

    is_three_of_a_kind = hand.isThreeOfAKind()
    is_pair = hand.isPair()

    if is_three_of_a_kind[0]:
        return is_three_of_a_kind[1:]
    
    elif is_pair[0]:
        return is_pair[1:]
    
    else:
        return ['1']

