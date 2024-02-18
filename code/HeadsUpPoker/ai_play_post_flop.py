import random
from generate_raise import generate_raise
from determine_hand import determine_hand
from determine_community_strength_five_cards import determine_community_strength_five
from ai_actions import Bot
from shuffle import shuffle_deck


def play_state_post(ai_bot, pocket, community, ai_current_bet, raise_state, game_state):

    hand_strength = determine_hand(pocket, community)
    max_bet = ai_bot.chips

    if game_state == 4: # Check to see if the strongest hand is within the community cards
        community_strength = determine_community_strength(community)
        
    # Player hasn't raised which means that they either checked, or AI is first to bet.
    if raise_state[0] == False:

        if hand_strength[0] >= 9: # Royal Flush, Straight Flush, Four of a Kind
            min_bet = ai_bot.chips // 15

            if game_state == 2:
                x = random.randint(1, 16) 
                if x == 1: # 1 in 15 chance of going all in
                    return ai_bot.raise_bet(ai_bot.chips)
                else:
                    shape = 0.1
            elif game_state == 3:
                x = random.randint(1, 7)
                if x == 1: # 1 in 6 chance of going all in
                    return ai_bot.raise_bet(ai_bot.chips)
                else:
                    shape = 0.25
            else:
                x = random.randint(1, 21) #
                if x <= 19: # 95% chance of going all in
                    return ai_bot.raise_bet(ai_bot.chips)
                else:
                    shape = 0.99
                
            print(shape)
            raise_amount = generate_raise(min_bet, max_bet, shape)
            return ai_bot.raise_bet(raise_amount)     
        
        elif hand_strength[0] == 8: # Four Of A Kind
            if game_state == 4:
                if community_strength[0] == hand_strength[0]: # If both four of kind
                    #Best hand is located within community cards
                    if hand_strength > community_strength: #We have better kicker
                        if int(hand_strength[2]) >= 10: # We have a strong kicker 
                            if int(hand_strength[2]) >= 13:
                                return ai_bot.raise_bet(ai_bot.chips) #All in as likely cant lose
                            raise_amount = generate_raise(ai_bot.chips // 15, max_bet, 0.7)
                        else: #Our kicker is more beatable
                            raise_amount = generate_raise(ai_bot.chips // 20, max_bet, 0.15)
                        return ai_bot.raise_bet(raise_amount)   
                    
                    else: #It can only be a split pot or player wins
                        if random.randint(1,5)  <= 3:
                            return ai_bot.check()
                        raise_amount = generate_raise(ai_bot.chips // 25, max_bet, 0.005) # Do small raise to hope player folds
                        return ai_bot.raise_bet(raise_amount)  
                     
                else: #Four of kind is in our pocket
                    x = random.randint(1, 21) #
                    if x <= 19: # 95% chance of going all in
                        return ai_bot.raise_bet(ai_bot.chips)
                    else:
                        shape = 0.99 # Else do very high bet:
                        raise_amount = generate_raise(ai_bot.chips // 10, max_bet, shape)
                        return ai_bot.raise_bet(raise_amount) 


            elif game_state == 2:
                x = random.randint(1, 21) #
                if x == 1: # 5% chance of going all in
                    return ai_bot.raise_bet(ai_bot.chips)
                else:
                    shape = 0.15

                pass

            elif game_state == 3: # Four Community cards
                pass

                    

        elif hand_strength[0] == 7: # Full House
            pass

        elif hand_strength[0] == 6: # Flush
            pass

        elif hand_strength[0] == 5: # Straight
            pass

        elif hand_strength[0] == 4: # Three Of A Kind
            pass

        elif hand_strength[0] == 3: # Two Pair
            pass

        elif hand_strength[0] == 2: # Pair
            pass

        elif hand_strength[0] == 1: # High Card
            pass



ai_bot = Bot()
deck = shuffle_deck()
com = [
    {'suit': 'Hearts', 'rank': '5'},  # Jack of Hearts
    {'suit': 'Hearts', 'rank': '5'},  # Ace of Hearts
    {'suit': 'Diamonds', 'rank': '5'},  
    {'suit': 'Clubs', 'rank': '5'}   
]

pocket = [
    {'suit': 'Hearts', 'rank': '4'},  # King of Hearts
    {'suit': 'Hearts', 'rank': '2'}
    ] # Queen of Hearts


decision = play_state_post(ai_bot, pocket, com, 200, [False], 3)
print("decision is", decision)