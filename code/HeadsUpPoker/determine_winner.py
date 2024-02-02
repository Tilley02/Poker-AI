from determine_hand import determine_hand
from poker_hand_ranks import poker_hand_ranks

'''
isRoyalFlush returns [hand rank]
isStraightFlush returns [hand rank, Straight high]
isFourOfAKind returns [hand rank, Four of a kind value]
isFullHouse returns [hand rank, Three of a kind value]
isflush returns [hand rank, cards values descending]
isStraight returns [hand rank, Straight high]
isThreeOfAKind returns [hand rank, Three of a kind value]
isTwoPair returns [hand rank, [two pairs], kicker]
isPair returns [hand rank, pair, [kickers descending]]
highest_card returns [hand rank, highest card, [kickers descending]]

'''

#hand[0] is hand rank
def determine_winner(player, ai, community):

    player_hand = determine_hand(player, community)
    ai_hand = determine_hand(ai, community)

    player_hand_type, ai_hand_type = player_hand[0], ai_hand[0]
    print("Player has '" + poker_hand_ranks[player_hand[0]] + "'")
    print("AI has '" + poker_hand_ranks[ai_hand[0]] + "'")

    if (player_hand[0] > ai_hand[0]):
        return "Player Wins"
    
    if (player_hand[0] < ai_hand[0]):
        return "AI Wins"
    
    #Else Player and AI have same hand strength, e.g. both have a single pair.
    

    #Royal Flush
    if player_hand[0] == 10 and ai_hand[0] == 10: 
        return "Split Pot" #Case if community cards are the Royal Flush

    #Straight Flush
    elif player_hand[0] == 9 and ai_hand[0] == 9:

        if int(player_hand[1]) > int(ai_hand[1]):
            return "Player Wins"
        elif int(player_hand[1]) < int(ai_hand[1]):
            return "AI Wins"
        else:
            return "Split Pot"
    
    #Four of a kind
    elif player_hand[0] == 8 and ai_hand[0] ==  8:
            
        if int(player_hand[1]) > int(ai_hand[1]):
            return "Player Wins"
        elif int(player_hand[1]) < int(ai_hand[1]):
            return "AI Wins"
        
        else: #The four of a kind is from community cards, compare kickers
            if int(player_hand[2]) > int(ai_hand[2]):
                return "Player Wins"
            elif int(player_hand[2]) < int(ai_hand[2]):
                return "AI Wins"
            else:
                return "Split Pot"
    
    #Full House
    elif player_hand[0] == 7 and ai_hand[0] == 7:
            
        #Compare Three of a Kind
        if int(player_hand[1]) > int(ai_hand[1]):
            return "Player Wins"
        elif int(player_hand[1]) < int(ai_hand[1]):
            return "AI Wins"
        
        else: #Compare Pairs
            if int(player_hand[2]) > int(ai_hand[2]):
                return "Player Wins"
            elif int(player_hand[2]) < int(ai_hand[2]):
                return "AI Wins"
            else:
                return "Split Pot"
    
    #Flush
    elif player_hand[0] == 6 and ai_hand[0] == 6:

        p_flush = player_hand[1]
        ai_flush = ai_hand[1]

        if p_flush > ai_flush:
            return "Player win"
        elif p_flush < ai_flush:
            return "AI Wins"
        else:
            return "Split Pot"

    #Straight
    elif player_hand[0] == 5 and ai_hand[0] == 5:
            
        if int(player_hand[1]) > int(ai_hand[1]):
            return "Player Wins"
        elif int(player_hand[1]) < int(ai_hand[1]):
            return "AI Wins"
        else:
            return "Split Pot"
    
    #Three of a kind
    elif player_hand[0] == 4 and ai_hand[0] == 4:
            
        if int(player_hand[1]) > int(ai_hand[1]):
            return "Player Wins"
        elif int(player_hand[1]) < int(ai_hand[1]):
            return "AI Wins"
        
        else: #Three of a kind in community, compare kickers.
            if player_hand[2] > ai_hand[2]:
                return "Player Wins"
            elif player_hand[2] < ai_hand[2]:
                return "AI Wins"
            else:
                return "Split Pot"

    
    #Two Pair
    elif player_hand[0] == 3 and ai_hand[0] == 3:

        player_pairs = [int(value) for value in player_hand[1]]
        ai_pairs = [int(value) for value in ai_hand[1]]
        #Compare Pair Values
        if player_pairs > ai_pairs:
            return "Player Wins"
        elif player_pairs < ai_pairs:
            return "AI Wins"     
        
        else: #Same two Pairs so compare the kicker
            if int(player_hand[2]) > int(ai_hand[2]):
                return "Player Wins"
            elif int(player_hand[2]) < int(ai_hand[2]):
                return "AI Wins" 
            
            else:
                return "Split Pot"

    #One Pair
    elif player_hand[0] == 2 and ai_hand[0] == 2:

        player_kickers = [int(value) for value in player_hand[2]]
        ai_kickers = [int(value) for value in ai_hand[2]]

        #Compare who has higher pair.
        if int(player_hand[1]) > int(ai_hand[1]):
            return "Player Wins"
        elif int(player_hand[1]) < int(ai_hand[1]):
            return "AI Wins"
        
        else: #Same Pair so compare highest cards.
            if player_kickers > ai_kickers:
                return "Player Wins"
            elif player_kickers < ai_kickers:
                return "AI Wins"
            
            else: #Same Cards Ranks and Pair
                return "Split Pot"
    
    #Highest Card
    elif player_hand[0] == 1 and ai_hand[0] == 1:

        player_kickers = [int(value) for value in player_hand[2]]
        ai_kickers = [int(value) for value in ai_hand[2]] 
        
        #Compare who has highest card
        if int(player_hand[1]) > int(ai_hand[1]):
            return "Player Wins"
        elif int(player_hand[1]) < int(ai_hand[1]):
            return "AI Wins"
        
        else: #Same highest card so compare next highest...
            if player_kickers > ai_kickers:
                return "Player Wins"
            elif player_kickers < ai_kickers:
                return "AI Wins"
            
            else: #Same card values
                return "Split Pot"
            
    