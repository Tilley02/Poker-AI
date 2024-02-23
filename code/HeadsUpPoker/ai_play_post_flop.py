import random
from generate_raise import generate_raise
from determine_hand import determine_hand
from determine_community_strength_five_cards import determine_community_strength_five
from determine_community_strength_four_cards import determine_community_strength_four
from determine_community_strength_three_cards import determine_community_strength_three
from ai_actions import Bot
from shuffle import shuffle_deck
from chen_formula import chen_formula



def play_state_post(ai_bot, pocket, community, current_bet, raise_state, game_state, ai_initial_chips):

    hand_strength = determine_hand(pocket, community)
    max_bet = ai_bot.chips
    min_bet = 100
    pocket_ranks = [card['rank'] for card in pocket]
    pocket_ranks = sorted(pocket_ranks, key=lambda x: int(x), reverse=True)
    community_suits = [card['suit'] for card in community]
    chen_score = chen_formula(pocket)
    shape = 0.005 # Base 

    if game_state == 4: # Check to see if the strongest hand is within the community cards
        community_strength = determine_community_strength_five(community)

    elif game_state == 3:
        community_strength = determine_community_strength_four(community)

    elif game_state == 2:
        community_strength = determine_community_strength_three(community)
        
    # Player hasn't raised which means that they either checked, or AI is first to bet.
    if raise_state[0] == False:

        if hand_strength[0] == 4 or hand_strength[0] == 5:
            round(ai_bot.chips // 2, -2)
        if hand_strength[0] < 4:
            round(ai_bot.chips // 5, -2)

        if hand_strength[0] >= 9: # Royal Flush, Straight Flush, Four of a Kind
            min_bet = ai_bot.chips // 15

            if game_state == 2:
                x = random.randint(1, 16) 
                if x == 1: # 1 in 15 chance of going all in
                    return ai_bot.raise_bet(ai_bot.chips, ai_initial_chips, current_bet)
                else:
                    shape = 0.1
            elif game_state == 3:
                x = random.randint(1, 7)
                if x == 1: # 1 in 6 chance of going all in
                    return ai_bot.raise_bet(ai_bot.chips, ai_initial_chips, current_bet)
                else:
                    shape = 0.25
            else:
                x = random.randint(1, 21) #
                if x <= 19: # 95% chance of going all in
                    return ai_bot.raise_bet(ai_bot.chips, ai_initial_chips, current_bet)
                else:
                    shape = 0.99
                
            print(shape)
            raise_amount = generate_raise(min_bet, max_bet, shape)
            return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)     
        

        elif hand_strength[0] == 8: # Four Of A Kind
            if game_state == 4:
                if community_strength[0] == hand_strength[0]: # If both four of kind
                    #Best hand is located within community cards
                    if hand_strength > community_strength: #We have better kicker
                        if int(hand_strength[2]) >= 10: # We have a strong kicker 
                            if int(hand_strength[2]) >= 13:
                                return ai_bot.raise_bet(ai_bot.chips, ai_initial_chips, current_bet) #All in as likely cant lose
                            else:
                                raise_amount = generate_raise(ai_bot.chips // 15, max_bet, 0.7)
                        else: #Our kicker is more beatable
                            raise_amount = generate_raise(ai_bot.chips // 20, max_bet, 0.15)
                        return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)   
                    
                    else: #It can only be a split pot or player wins
                        if random.randint(1,5)  <= 3:
                            return ai_bot.check()
                        raise_amount = generate_raise(ai_bot.chips // 25, max_bet, 0.005) # Do small raise to hope player folds
                        return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  
                     
                else: #Four of kind is in our pocket
                    x = random.randint(1, 21) #
                    if x <= 19: # 95% chance of going all in
                        return ai_bot.raise_bet(ai_bot.chips, ai_initial_chips, current_bet)
                    else:
                        shape = 0.99 # Else do very high bet:
                        raise_amount = generate_raise(ai_bot.chips // 10, max_bet, shape)
                        return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet) 

            elif game_state == 2:
                x = random.randint(1, 21) #
                if x == 1: # 5% chance of going all in
                    return ai_bot.raise_bet(ai_bot.chips, ai_initial_chips, current_bet)
                else:
                    shape = 0.15

            elif game_state == 3: # Four Community cards
                if hand_strength[0] > community_strength[0]:
                    raise_amount = generate_raise(ai_bot.chips // 18, max_bet, 0.5)
                else:
                    if int(pocket_ranks[0]) >= 10: # We have a strong kicker 
                        if int(pocket_ranks[0]) >= 13:
                            raise_amount = generate_raise(ai_bot.chips // 17, max_bet, 0.5)
                        else:
                            raise_amount = generate_raise(ai_bot.chips // 20, max_bet, 0.38)
                    else: #Our kicker is more beatable
                        raise_amount = generate_raise(ai_bot.chips // 23, max_bet, 0.1)
                    return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)   

                    

        elif hand_strength[0] == 7: # Full House
            x = random.randint(1, 21)
            
            if game_state == 2:
                shape = 0.4

            elif game_state == 3:
                if x >= 19: 
                    return ai_bot.raise_bet(ai_bot.chips, ai_initial_chips, current_bet)
                else:
                    shape = 0.6

            elif game_state == 4:
                x = random.randint(1,21)
                if hand_strength[0] > community_strength[0]: #full house is not fully in community
                    if int(hand_strength[1]) >= 10:
                        if x >= 12:
                            return ai_bot.raise_bet(ai_bot.chips, ai_initial_chips, current_bet)
                        else:
                            shape = 0.8
                    else: # Weaker Three of a kind
                        shape = 0.5

                elif int(hand_strength[1]) > int(community_strength[1]): # Better Three of a kind
                    shape = 0.65
                elif int(hand_strength[1]) > int(community_strength[1]): # Better Pair
                    shape = 0.25

                else: # Full House is fully in community
                    if random.randint(1,5)  <= 3:
                        return ai_bot.check()
                    raise_amount = generate_raise(ai_bot.chips // 25, max_bet, 0.005) # Do small raise to hope player folds
                    return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  
                
            raise_amount = generate_raise(min_bet, max_bet, shape)
            return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  


        elif hand_strength[0] == 6: # Flush
            if game_state == 2:
                shape = 0.3
            elif game_state == 3:
                if len(set(community_suits)) == 1: # Four of same suit in community cards
                    shape = 0.15
                else: # 3 of same suit
                    shape = 0.475
            elif game_state == 4:
                if len(set(community_suits)) == 3: #Three of same suit in community cards
                    if random.randint(1,4) == 3:
                        return ai_bot.raise_bet(ai_bot.chips, ai_initial_chips, current_bet) # All in
                    else:
                        min_bet == ai_bot.chips // 12 
                        shape = 0.8

                elif len(set(community_suits)) == 2:
                    shape = 0.4

                elif len(set(community_suits)) == 1: # Flush in community cards
                    if hand_strength > community_strength: # Does Ai have a better flush than community cards flush
                        shape = 0.5
                    else: #Can only be split pot for AI
                        if random.randint(1,5)  <= 3:
                            return ai_bot.check()
                        else:
                            raise_amount = generate_raise(ai_bot.chips // 25, max_bet, 0.005) # Do small raise to hope player folds
                            return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)
                    
            raise_amount = generate_raise(min_bet, max_bet, shape)
            return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)   


        elif hand_strength[0] == 5: # Straight
            
            if game_state == 2:
                shape = 0.275

            elif game_state == 3:
                shape = 0.45

            elif game_state == 4:
                if hand_strength[0] > community_strength[0]:
                    shape = 0.7
                else: # Straight in community cards
                    if hand_strength > community_strength: # Hand uses something from AI pocket to be better straight
                        shape = 0.5
                    else:
                        if random.randint(1,5)  <= 3:
                            return ai_bot.check()
                        else:
                            raise_amount = generate_raise(ai_bot.chips // 25, max_bet, 0.005) # Do small raise to hope player folds
                            return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)
                    
            raise_amount = generate_raise(min_bet, max_bet, shape)
            return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  


        elif hand_strength[0] == 4: # Three Of A Kind

            if random.randint(1,81) <= game_state:
                if random.randint(1,21) <= chen_score:
                    return ai_bot.raise_bet(ai_bot.chips, ai_initial_chips, current_bet)


            if game_state == 2:
                if hand_strength > community_strength: # Three of a kind uses pocket
                    shape = 0.4
                else:
                    if random.randint(1,6) == 5:
                        shape = 0.3
                    else: 
                        return ai_bot.check()
                    
            elif game_state == 3:
                if hand_strength > community_strength: # Three of a kind uses pocket
                    shape = 0.45
                else: #Three of a kind is in community
                    if random.randint(1,5) == 4:
                        shape = 0.06
                    else: 
                        return ai_bot.check()
                    
            elif game_state == 4:
                if hand_strength > community_strength: # Three of a kind uses pocket
                    shape = 0.625
                else: #Three of a kind is in community
                    if pocket_ranks > community_strength[2]: # AI pocket has better kickers
                        if int(pocket_ranks[0]) >= 12: # AI has strong kickers
                            shape = 0.35
                        else: #AI kickers are more beatable
                            shape = 0.2

                    else: #AI pocket doesnt have better kickers
                        if int(pocket_ranks[0]) >= 12:
                            shape = 0.14
                        else:
                            if random.randint(1,5) == 4:
                                shape = 0.05
                            else:
                                return ai_bot.check()
                            
            raise_amount = generate_raise(min_bet, max_bet, shape)
            return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  


        elif hand_strength[0] == 3: # Two Pair
            if game_state == 2:
                shape = 0.39

            elif game_state == 3:
                if int(hand_strength[0]) > int(community_strength[0]) or hand_strength[1] > community_strength[1]: # Two pair uses pocket
                    shape = 0.18
                else: # Two pair is in community
                    if random.randint(1,3) == 1:
                        return ai_bot.check()
                    else:
                        shape = 0.28

            elif game_state == 4:
                if int(hand_strength[0]) > int(community_strength[0]) or hand_strength[1] > community_strength[1]: # Two pair uses pocket
                    shape = 0.26
                else:
                    if random.randint(1,3) == 1:
                        return ai_bot.check()
                    else:
                        shape = 0.16

            raise_amount = generate_raise(min_bet, max_bet, shape)
            return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  


        elif hand_strength[0] == 2: # Pair

            if random.randint(1,101) <= game_state:
                if random.randint(1,21) <= chen_score:
                    return ai_bot.raise_bet(ai_bot.chips, ai_initial_chips, current_bet)

            if game_state == 2:
                if int(hand_strength[0]) > int(community_strength[0]) or hand_strength[1] > community_strength[1]: # Pair uses pocket
                    shape = 0.2
                else: # Pair located in community cards
                    if chen_score >= 8:
                        if random.randint(1,4) <= 2:
                            shape = 0.14
                        else:
                            return ai_bot.check()
                    else:
                        if random.randint(1,5) <= 3:
                            return ai_bot.check()
                        else:
                            shape = 0.1

            elif game_state == 3:
                if int(hand_strength[0]) > int(community_strength[0]) or hand_strength[1] > community_strength[1]: # Pair uses pocket
                    if int(hand_strength[1]) >= 10: # If it is a pair of 10's or higher
                        shape = 0.22
                    else:
                        if chen_score >= 8:
                            shape = 0.15
                        else:
                            if random.randint(1,5) <= 3:
                                return ai_bot.check()
                            else:
                                shape = 0.11

                else: # Pair is in community cards
                    if chen_score >= 8:
                        if random.randint(1,4) == 1:
                            shape = 0.07
                        else:
                            return ai_bot.check()
                    else:
                        if random.randint(1,5) == 1:
                            shape = 0.04
                        else:
                            return ai_bot.check()
                            
            elif game_state == 4:
                if int(hand_strength[0]) > int(community_strength[0]) or hand_strength[1] > community_strength[1]: # Pair uses pocket
                    if int(hand_strength[1]) >= 10: # If it is a pair of 10's or higher
                        shape = 0.24
                    else:
                        if int(pocket_ranks[0]) >= 10:
                            shape = 0.17
                        else:
                            if random.randint(1,5) <= 3:
                                return ai_bot.check()
                            else:
                                shape = 0.13

                else: # Pair is in community cards
                    if hand_strength[2] > community_strength[2]: #Pocket kickers are stronger
                        if int(pocket_ranks[0]) > 10: #Strong kicker
                            if random.randint(1,6) <= 4:
                                shape = 0.28
                            else:
                                return ai_bot.check()
                        else: # More beatable kicker
                            if random.randint(1, 6) <= 4:
                                return ai_bot.check()
                            else:
                                shape = 0.14

                    else: # Community kickers are stronger:
                        if random.randint(1, 9) <= 7:
                            return ai_bot.check()
                        else:
                            shape = 0.09

            raise_amount = generate_raise(min_bet, max_bet, shape)
            return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  


        elif hand_strength[0] == 1: # High Card

            if random.randint(1,101) <= game_state:
                if random.randint(1, 21) <= chen_score:
                    return ai_bot.raise_bet(ai_bot.chips, ai_initial_chips, current_bet)

            if game_state == 2:
                if chen_score >= 12:
                    if random.randint(1,6) <= 4: # 80% chance of raising
                        shape = 0.22
                    else:
                        return ai_bot.check()
                elif chen_score >= 8:
                    if random.randint(1,11) <= 5: # 50% chance of raising
                        shape = 0.16
                    else:
                        return ai_bot.check()
                else:
                    if random.randint(1,11) <= 2: # 20% chance of raising
                        shape = 0.1
                    else:
                        return ai_bot.check()
                    
            elif game_state == 3:
                if chen_score >= 12:
                    if random.randint(1,6) <= 3: # 60% chance of raising
                        shape = 0.17
                    else:
                        return ai_bot.check()
                elif chen_score >= 8:
                    if random.randint(1,21) <= 5: # 25% chance of raising
                        shape = 0.11
                    else:
                        return ai_bot.check()
                else:
                    if random.randint(1,21) <= 3: # 15% chance of raising
                        shape = 0.08
                    else:
                        return ai_bot.check()
                    
            elif game_state == 4:
                if chen_score >= 12:
                    if random.randint(1,11) <= 5: # 50% chance of raising
                        shape = 0.15
                    else:
                        return ai_bot.check()
                elif chen_score >= 8:
                    if random.randint(1,11) <= 3: # 30% chance of raising
                        shape = 0.11
                    else:
                        return ai_bot.check()
                else:
                    if random.randint(1,11) == 1: # 10% chance of raising
                        shape = 0.07
                    else:
                        return ai_bot.check()

            raise_amount = generate_raise(min_bet, max_bet, shape)
            return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  
    




    else: # Player has Raised
        player_raise  = int(raise_state[1])
        chips = ai_bot.chips
        hand_rank = int(hand_strength[0])
        com_rank = int(community_strength[0])
        bonus = chen_score // 15
        if hand_rank == 4 or hand_rank == 5:
            round(chips // 2, -2)
        if hand_rank < 4:
            round(chips // 6, -2)


        if game_state == 2:
            if hand_rank >= 5: # AI has a very strong hand
                if player_raise > chips // 10:
                    shape = 0.19
                else:
                    shape = 0.15

                raise_amount = generate_raise(min_bet, max_bet, shape)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  


            elif hand_rank == 4: # Three Of A Kind
                if hand_rank > com_rank: # Three of a kind uses AI pocket
                    if player_raise > chips // 5:
                        shape = 0.175
                    else:
                        if random.randint(1,5) == 1:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            shape = 0.15
                
                else: #Three of a kind is in community
                    if random.randint(1,5) == 1:
                        shape = 0.15
                    else:
                        if random.randint(1,4) == 1:
                            shape = 0.1
                        else:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        
                raise_amount = generate_raise(min_bet, max_bet, shape)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  


            elif hand_rank == 3: # Two Pair
                if player_raise > chips // 5: #Large Raise
                    if random.randint(1,3) == 1:
                        return ai_bot.call(raise_state[1], ai_initial_chips)
                    else:
                        shape = 0.11
                    
                else: #Smaller Raise
                    if random.randint(1,5) == 1:
                        return ai_bot.call(raise_state[1], ai_initial_chips)
                    else:
                        shape = 0.09

                raise_amount = generate_raise(min_bet, max_bet, shape)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  


            elif hand_rank == 2: # Pair
                if hand_rank > com_rank: #pair uses pocket

                    if player_raise > chips // 5: # Large Raise
                        if chen_score <= 5 and current_bet <= chips // 25:
                            return ai_bot.fold()
                        else:
                            if current_bet > chips // 7:
                                if random.randint(1,5) == 1:
                                    shape = 0.05
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                            else:
                                if random.randint(1,9) == 1:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                                else:
                                    return ai_bot.fold()
                                
                    else: # Smaller Raise
                        if random.randint(1,25) <= chen_score:
                            shape = 0.05 + bonus
                        else:
                            if chen_score <= 3:
                                if current_bet <- chips // 30:
                                    if random.randint(1,5) == 1:
                                        return ai_bot.fold()
                                    else:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
                                else:
                                    if random.randint(1,3) == 1:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
                                    else:
                                        shape = 0.02
                            else:
                                if random.randint(1,4) == 1:
                                    shape = 0.08
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)



                else: # Pair is in community

                    if player_raise > chips // 5: # Large Raise

                        if chen_score >= 9: #Strong Pocket

                            if current_bet > chips // 7: #AI has large current bet:
                                if random.randint(1, 21) <= 5:
                                    shape = 0.01 + bonus
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                                
                            else: # AI has more foldable current bet
                                if random.randint(1,6) == 1:
                                    ai_bot.fold()
                                else:
                                    if random.randint(1,4) == 1:
                                        shape = 0.05 + bonus


                        else: #AI has more foldable pocket

                            if current_bet > chips // 7: #AI has large current bet:
                                if random.randint(1, 21) <= 1:
                                    return ai_bot.fold()
                                else:
                                    if random.randint(1,5) == 1:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
                                    else:
                                        shape = 0.05

                            else: # AI has more foldable current bet
                                if random.randint(1,5) != 1:
                                    ai_bot.fold()
                                else:
                                    if random.randint(1,9) == 1:
                                        shape = 0.03
                                    else:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
    

                    else: # Smaller Player Raise
                        if random.randint(1,25) <= chen_score:
                            shape = 0.07 + bonus
                        else:
                            if chen_score <= 7: # Weaker Pocket
                                if current_bet <= chips // 30:
                                    if random.randint(1,7) <= 2:
                                        return ai_bot.fold()
                                    else:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
                                else:
                                    if random.randint(1,3) == 1:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
                                    else:
                                        shape = 0.02

                            else: # Stronger Pocket
                                if random.randint(1,6) == 3:
                                    shape = 0.008 + bonus
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)

                raise_amount = generate_raise(min_bet, max_bet, shape)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  


            elif hand_rank == 1: # High Card

                if player_raise > chips // 10 and current_bet > chips // 5: # High Raise and High Current Bet
                    if chen_score >= 10: # Strong Pocket
                        if random.randint(1, 9) == 1:
                            shape = 0.04
                        else:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        
                    else: # Weaker Pocket
                        if random.randint(1, 16) == 1:
                            return ai_bot.fold()
                        else:
                            return ai_bot.call(raise_state[1], ai_initial_chips)

                elif player_raise > chips // 10 and current_bet <= chips // 10: # High Raise and Low Current Bet
                    if chen_score >= 10: # Strong Pocket
                        if random.randint(1,4) != 1:
                            if random.randint(1,3) == 1:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                            else:
                                shape = 0.01
                        else:
                            return ai_bot.fold()

                    else: # Weaker Pocket
                        if random.randint(1,9) == 1:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            return ai_bot.fold()

                elif player_raise < chips // 10 and current_bet > chips // 5: #Lower Raise and High Current Bet
                    if chen_score >= 8: # Strong Pocket
                        if random.randint(1, 3) == 1:
                            shape = 0.02
                        else:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                    else: # Weaker Pocket
                        if random.randint(1,5) == 1:
                            shape = 0.04
                        else:
                            return ai_bot.call(raise_state[1], ai_initial_chips)

                elif player_raise < chips // 10 and current_bet <= chips // 10: # Lower Raise and Low Current Bet
                    if chen_score >= 8: # Strong Pocket
                        if random.randint(1, 4) == 1:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            shape = 0.05

                    else: # Weaker Pocket
                        if random.randint(1,6) == 1:
                            return ai_bot.fold()
                        else:
                            if random.randint(1,4) == 1:
                                shape = 0.03
                            else:
                                return ai_bot.call(raise_state[1], ai_initial_chips)

                else:
                    if random.randint(1,5) == 1:
                        shape = 0.01
                    else:
                        if random.randint(1,11) != 1:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            if chen_score <= 5:
                                return ai_bot.fold()
                            else:
                                shape = 0.07
                    
                raise_amount = generate_raise(min_bet, max_bet, shape)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  
            




        elif game_state == 3: ### GAMESTATE IS 3 (4 Cards Shown) ### 

            if hand_rank >= 9: # Royal or Straight Flush
                if player_raise > chips // 10:
                    shape = 0.75
                else:
                    shape = 0.5    

                raise_amount = generate_raise(min_bet, max_bet, shape)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  
            
            if hand_rank == 8: #Four of a Kind:
                if pocket_ranks[0] > 10:
                    if random.randint(1, 5) == 1:
                        return ai_bot.call(raise_state[1], ai_initial_chips)
                    else:
                        shape = 0.15
                else:
                    if random.randint(1,9) == 1:
                        shape = 0.1
                    else:
                        ai_bot.call(raise_state[1], ai_initial_chips)
            
                raise_amount = generate_raise(min_bet, max_bet, shape)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  

            if 5 <= hand_rank <= 7:
                if random.randint(1,9) == 1:
                    return ai_bot.call(raise_state[1], ai_initial_chips)
                else:
                    if random.randint(1,3) == 1:
                        shape = 0.3
                    else:
                        shape = 0.09

                raise_amount = generate_raise(min_bet, max_bet, shape)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  

            
            if hand_rank == 4: # Three of a Kind
                if hand_rank > com_rank: # Three of a Kind uses ai pocket
                    if random.randint(1,5) == 1:
                        return ai_bot.call(raise_state[1], ai_initial_chips)
                    else:
                        shape = 0.12

                else: # Three of a kind in community cards
                    if pocket_ranks[0] >= 11:
                        if random.randint(1,3) == 1:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            shape = 0.1
                    else:
                        if player_raise > chips // 10: #Large Raise
                            if current_bet > chips // 3: # Large Current bet
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                            else: # Small Current Bet
                                if pocket_ranks[0] <= 7:
                                    return ai_bot.fold()
                                else:
                                    if random.randint(1,3) == 1:
                                        return ai_bot.fold()
                                    else:
                                        shape = 0.075

                        else: # Smaller Raise
                            if current_bet > chips // 3: #Large Current Bet
                                if random.randint(1,4) == 1:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                                else:
                                    shape = 0.08

                            else: # Small Current Bet
                                if random.randint(1,6) == 1:
                                    shape = 0.06
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)

                raise_amount = generate_raise(min_bet, max_bet, shape)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  
            

            if hand_rank == 3: # Two Pair
                if hand_rank > com_rank: # Two pair uses ai pocket
                    if random.randint(1,3) == 1:
                        return ai_bot.call(raise_state[1], ai_initial_chips)
                    else:
                        shape = 0.05

                else: #Two pair is in community
                    if player_raise > chips // 10 and current_bet > chips // 5: # High Raise and High Current Bet
                        if pocket_ranks[0] >= 11: #Strong pocket kicker
                            if random.randint(1,3):
                                shape = 0.05
                            else:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            if pocket_ranks[0] <= 3:
                                return ai_bot.fold()
                            else:
                                return ai_bot.call               , ai_initial_chips             

                    elif player_raise > chips // 10 and current_bet <= chips // 10: # High Raise and Low Current Bet
                        if pocket_ranks >= 12:
                            if random.randint(1,6) == 1:
                                shape = 0.05
                            else:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            return ai_bot.fold()


                    elif player_raise < chips // 10 and current_bet > chips // 5: #Lower Raise and High Current Bet
                        if pocket_ranks[0] >= 11:
                            if random.randint(1,6) == 1:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                            else:
                                shape = 0.12
                        else:
                            if random.randint(1,6) == 1:
                                shape = 0.08
                            else:
                                return ai_bot.call(raise_state[1], ai_initial_chips)

                    elif player_raise < chips // 10 and current_bet <= chips // 10: # Lower Raise and Low Current Bet
                        if pocket_ranks[0] > 11:
                            if random.randint(1, 6) == 1:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                            else:
                                shape = 0.1
                        else:
                            if random.randint(1,6) == 1:
                                shape = 0.07
                            else:
                                return ai_bot.call(raise_state[1], ai_initial_chips)

                raise_amount = generate_raise(min_bet, max_bet, shape)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  


            if hand_rank == 2: # Pair
                if hand_rank > com_rank: #pair uses pocket

                    if player_raise > chips // 5: # Large Raise
                        if chen_score <= 5 and current_bet <= chips // 25:
                            return ai_bot.fold()
                        else:
                            if current_bet > chips // 7:
                                if random.randint(1,5) == 1:
                                    shape = 0.08
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                            else:
                                if random.randint(1,9) == 1:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                                else:
                                    return ai_bot.fold()
                                
                    else: # Smaller Raise
                        if random.randint(1,25) <= chen_score:
                            shape = 0.08 + bonus
                        else:
                            if chen_score <= 3:
                                if current_bet <- chips // 30:
                                    if random.randint(1,5) == 1:
                                        return ai_bot.fold()
                                    else:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
                                else:
                                    if random.randint(1,3) == 1:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
                                    else:
                                        shape = 0.02
                            else:
                                if random.randint(1,4) == 1:
                                    shape = 0.07
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)

                else: # Pair is in community

                    if player_raise > chips // 5: # Large Raise

                        if chen_score >= 9: #Strong Pocket

                            if current_bet > chips // 7: #AI has large current bet:
                                if random.randint(1, 21) <= 5:
                                    shape = 0.04 + bonus
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                                
                            else: # AI has more foldable current bet
                                if random.randint(1,6) == 1:
                                    ai_bot.fold()
                                else:
                                    if random.randint(1,4) == 1:
                                        shape = 0.06 + bonus


                        else: #AI has more foldable pocket

                            if current_bet > chips // 7: #AI has large current bet:
                                if random.randint(1, 21) <= 1:
                                    return ai_bot.fold()
                                else:
                                    if random.randint(1,5) == 1:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
                                    else:
                                        shape = 0.05

                            else: # AI has more foldable current bet
                                if random.randint(1,5) != 1:
                                    ai_bot.fold()
                                else:
                                    if random.randint(1,9) == 1:
                                        shape = 0.03
                                    else:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
    

                    else: # Smaller Player Raise
                        if random.randint(1,25) <= chen_score:
                            shape = 0.05 + bonus
                        else:
                            if chen_score <= 7: # Weaker Pocket
                                if current_bet <= chips // 30:
                                    if random.randint(1,7) <= 2:
                                        return ai_bot.fold()
                                    else:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
                                else:
                                    if random.randint(1,3) == 1:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
                                    else:
                                        shape = 0.02

                            else: # Stronger Pocket
                                if random.randint(1,6) == 3:
                                    shape = 0.04 + bonus
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)

                raise_amount = generate_raise(min_bet, max_bet, shape+0.04)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  


            elif hand_rank == 1: # High Card

                if player_raise > chips // 10 and current_bet > chips // 5: # High Raise and High Current Bet
                    if chen_score >= 12: # Strong Pocket
                        if random.randint(1, 9) == 1:
                            shape = 0.06
                        else:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        
                    else: # Weaker Pocket
                        if random.randint(1, 16) == 1:
                            return ai_bot.fold()
                        else:
                            return ai_bot.call(raise_state[1], ai_initial_chips)


                elif player_raise > chips // 10 and current_bet <= chips // 10: # High Raise and Low Current Bet
                    if chen_score >= 12: # Strong Pocket
                        return ai_bot.call(raise_state[1], ai_initial_chips)
                    else:
                        return ai_bot.fold()


                elif player_raise < chips // 12 and current_bet > chips // 5: #Lower Raise and High Current Bet
                    if chen_score >= 10: # Strong Pocket
                        if random.randint(1, 4) == 1:
                            shape = 0.07
                        else:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                    else: # Weaker Pocket
                        if random.randint(1,5) == 1:
                            shape = 0.08
                        else:
                            return ai_bot.call(raise_state[1], ai_initial_chips)

                elif player_raise < chips // 12 and current_bet <= chips // 10: # Lower Raise and Low Current Bet
                    if chen_score >= 8: # Strong Pocket
                        if random.randint(1, 4) == 1:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            shape = 0.009

                    else: # Weaker Pocket
                        if random.randint(1,6) == 1:
                            return ai_bot.fold()
                        else:
                            if random.randint(1,4) == 1:
                                shape = 0.03
                            else:
                                return ai_bot.call(raise_state[1], ai_initial_chips)

                else:
                    if random.randint(1,2) == 1:
                        return ai_bot.fold()
                    else:
                        return ai_bot.call(raise_state[1], ai_initial_chips)

                raise_amount = generate_raise(min_bet, max_bet, shape+0.04)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  




        else: ### GAMESTATE IS 4 (All Cards Shown) ### 

            if hand_rank >= 9: # Royal or Straight Flush
                return ai_bot.raise_bet(chips) 

            if hand_rank == 6:
                if int(hand_rank) == 6:
                    if len(set(community_suits)) == 3: #Three of same suit in community cards
                        if random.randint(1,4) == 3:
                            return ai_bot.raise_bet(ai_bot.chips, ai_initial_chips, current_bet) # All in
                        else:
                            min_bet == ai_bot.chips // 12 
                            shape = 0.8

                    elif len(set(community_suits)) == 2:
                        if random.randint(1,5) == 1:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            shape = 0.4

                    elif len(set(community_suits)) == 1: # Flush in community cards
                        if hand_strength > community_strength: # Does Ai have a better flush than community cards flush
                            if random.randint(1,5) == 1:
                                shape = 0.5
                            else:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                        else: #Can only be split pot for AI
                            if random.randint(1,5)  <= 3:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                            else:
                                raise_amount = generate_raise(ai_bot.chips // 25, max_bet, 0.005) # Do small raise to hope player folds
                                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)
                        
                    raise_amount = generate_raise(min_bet, max_bet, shape)
                    return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)   
                

            if hand_rank == 8:
                if hand_rank > com_rank: # Strong hand uses AI Pocket

                    if random.randint(1,6) == 1:
                        return ai_bot.call(raise_state[1], ai_initial_chips)
                    else:
                        if random.randint(1,3) == 1:
                            shape = 0.4
                        else:
                            shape = 0.6

                else: # Four of a kind is in community
                    if hand_strength > community_strength: #AI kicker is used
                        if int(pocket_ranks[0]) >= 10: #Strong Kicker
                            if random.randint(1,6) == 1:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                            else:
                                shape = 0.35
                        else: #Weaker Kicker
                            if random.randint(1,4) == 1:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                            else:
                                shape = 0.15

                    else: #Fully community:
                        if hand_strength[2] >= 12: #Community kicker hard to beat
                            if random.rantint(1,3) == 1:
                                shape = 0.2
                            else:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                        elif hand_strength[2] <= 8: #Community Kicker is very beatable
                            if player_raise > chips // 10 and current_bet > chips // 5: # High Raise and High Current Bet
                                if random.randint(1,9) <= 7:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                                else:
                                    return ai_bot.fold()
                            elif player_raise > chips // 10 and current_bet <= chips // 10: # High Raise and Low Current Bet
                                if random.randint(1,6) == 1:
                                    return ai_bot.fold()
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                            elif player_raise < chips // 10 and current_bet > chips // 5: #Lower Raise and High Current Bet
                                if random.randint(1,5) == 1:
                                    shape = 0.12
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                            elif player_raise < chips // 10 and current_bet <= chips // 10: # Lower Raise and Low Current Bet
                                if random.randint(1,4) == 1:
                                    shape = 0.16
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)

                        else: # Community Kicker still beatable but better chance of Split Pot
                            if player_raise > chips // 10 and current_bet > chips // 5: # High Raise and High Current Bet
                                if random.randint(1,21) <= 19:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                                else:
                                    return ai_bot.fold()
                            elif player_raise > chips // 10 and current_bet <= chips // 10: # High Raise and Low Current Bet
                                if random.randint(1,4) == 1:
                                    return ai_bot.fold()
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                            elif player_raise < chips // 10 and current_bet > chips // 5: #Lower Raise and High Current Bet
                                if random.randint(1,3) == 1:
                                    shape = 0.4
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                            elif player_raise < chips // 10 and current_bet <= chips // 10: # Lower Raise and Low Current Bet
                                if random.randint(1,3) == 1:
                                    shape = 0.5
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)


            if hand_rank == 7 or hand_rank == 5: # Straight or Full House
                
                if hand_rank > com_rank: # Strong hand uses AI Pocket

                    if random.randint(1,6) == 1:
                        return ai_bot.call(raise_state[1], ai_initial_chips)
                    else:
                        if random.randint(1,3) == 1:
                            shape = 0.4
                        else:
                            shape = 0.2


                else: #Strong hand is fully in community
                    if player_raise > chips // 10 and current_bet > chips // 5: # High Raise and High Current Bet
                        if random.randint(1,5) == 1:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            shape = 0.15
                    elif player_raise > chips // 10 and current_bet <= chips // 10: # High Raise and Low Current Bet
                            if random.randint(1,9) == 1:
                                shape = 0.1
                            else:
                                return ai_bot.call(raise_state[1], ai_initial_chips)

                    elif player_raise < chips // 10 and current_bet > chips // 5: #Lower Raise and High Current Bet
                        if random.randint(1,11) == 1:
                            shape = 0.1
                        else:
                            shape = 0.3

                    elif player_raise < chips // 10 and current_bet <= chips // 10: # Lower Raise and Low Current Bet
                        shape = 0.2


                raise_amount = generate_raise(min_bet, max_bet, shape)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)

              

            

            if hand_rank == 4: # Three of a Kind
                if hand_rank > com_rank: # Three of a Kind uses ai pocket
                    if random.randint(1,5) == 1:
                        return ai_bot.call(raise_state[1], ai_initial_chips)
                    else:
                        shape = 0.1

                else: # Three of a kind in community cards
                    if int(pocket_ranks[0]) >= 11:
                        if random.randint(1,3) == 1:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            shape = 0.06
                    else:
                        if player_raise > chips // 10: #Large Raise
                            if current_bet > chips // 3: # Large Current bet
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                            else: # Small Current Bet
                                if int(pocket_ranks[0]) <= 7:
                                    return ai_bot.fold()
                                else:
                                    if random.randint(1,3) == 1:
                                        return ai_bot.fold()
                                    else:
                                        shape = 0.05

                        else: # Smaller Raise
                            if current_bet > chips // 3: #Large Current Bet
                                if random.randint(1,4) == 1:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                                else:
                                    shape = 0.05

                            else: # Small Current Bet
                                if random.randint(1,6) == 1:
                                    shape = 0.06
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)

                raise_amount = generate_raise(min_bet, max_bet, shape)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet + 0.04)  


            if hand_rank == 3: # Two Pair
                if hand_rank > com_rank: # Two pair uses ai pocket
                    if random.randint(1,3) == 1:
                        return ai_bot.call(raise_state[1], ai_initial_chips)
                    else:
                        shape = 0.05

                else: #Two pair is in community
                    if int(community_strength[2]) > int(pocket_ranks[0]): # Community kicker is strongest
                        if int(community_strength[2]) >= 11:
                            if random.randint(1,3) == 1:
                                shape = 0.05
                            else:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            if player_raise > chips // 10 and current_bet > chips // 5: # High Raise and High Current Bet
                                if random.randint(1,21) == 1:
                                    return ai_bot.fold()
                                else:
                                    return ai_bot.fold()
                      
                            elif player_raise > chips // 10 and current_bet <= chips // 10: # High Raise and Low Current Bet
                                if random.randint(1,11) == 1:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                                else:
                                    return ai_bot.fold()

                            elif player_raise < chips // 10 and current_bet > chips // 5: #Lower Raise and High Current Bet
                                if random.randint(1,5) == 1:
                                    shape = 0.067
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)

                            elif player_raise < chips // 10 and current_bet <= chips // 10: # Lower Raise and Low Current Bet
                                if random.randint(1,4) == 1:
                                    shape = 0.08
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)

                    if player_raise > chips // 10 and current_bet > chips // 5: # High Raise and High Current Bet
                        if pocket_ranks[0] >= 11: #Strong pocket kicker
                            if random.randint(1,3):
                                shape = 0.05
                            else:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            if pocket_ranks[0] <= 3:
                                return ai_bot.fold()
                            else:
                                return ai_bot.call(raise_state[1], ai_initial_chips)                           

                    elif player_raise > chips // 10 and current_bet <= chips // 10: # High Raise and Low Current Bet
                        if pocket_ranks >= 12:
                            if random.randint(1,6) == 1:
                                shape = 0.09
                            else:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            return ai_bot.fold()


                    elif player_raise < chips // 10 and current_bet > chips // 5: #Lower Raise and High Current Bet
                        if pocket_ranks[0] >= 11:
                            if random.randint(1,6) == 1:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                            else:
                                shape = 0.09
                        else:
                            if random.randint(1,6) == 1:
                                shape = 0.08
                            else:
                                return ai_bot.call(raise_state[1], ai_initial_chips)

                    elif player_raise < chips // 10 and current_bet <= chips // 10: # Lower Raise and Low Current Bet
                        if pocket_ranks[0] > 11:
                            if random.randint(1, 6) == 1:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                            else:
                                shape = 0.1
                        else:
                            if random.randint(1,6) == 1:
                                shape = 0.07
                            else:
                                return ai_bot.call(raise_state[1], ai_initial_chips)

                raise_amount = generate_raise(min_bet, max_bet, shape)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet) 
            

            if hand_rank == 2: # Pair
                if hand_rank > com_rank: #pair uses pocket

                    if player_raise > chips // 5: # Large Raise
                        if chen_score <= 5 and current_bet <= chips // 25:
                            return ai_bot.fold()
                        else:
                            if current_bet > chips // 7:
                                if random.randint(1,5) == 1:
                                    shape = 0.06
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                            else:
                                if random.randint(1,9) == 1:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                                else:
                                    return ai_bot.fold()
                                
                    else: # Smaller Raise
                        if random.randint(1,25) <= chen_score:
                            shape = 0.05 + bonus
                        else:
                            if chen_score <= 3:
                                if current_bet <- chips // 30:
                                    if random.randint(1,5) == 1:
                                        return ai_bot.fold()
                                    else:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
                                else:
                                    if random.randint(1,3) == 1:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
                                    else:
                                        shape = 0.02
                            else:
                                if random.randint(1,4) == 1:
                                    shape = 0.03
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)

                else: # Pair is in community

                    if player_raise > chips // 5: # Large Raise

                        if chen_score >= 9: #Strong Pocket

                            if current_bet > chips // 7: #AI has large current bet:
                                if random.randint(1, 21) <= 5:
                                    shape = 0.05 + bonus
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)
                                
                            else: # AI has more foldable current bet
                                if random.randint(1,6) == 1:
                                    ai_bot.fold()
                                else:
                                    if random.randint(1,4) == 1:
                                        shape = 0.05 + bonus


                        else: #AI has more foldable pocket

                            if current_bet > chips // 7: #AI has large current bet:
                                if random.randint(1, 21) <= 1:
                                    return ai_bot.fold()
                                else:
                                    if random.randint(1,5) == 1:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
                                    else:
                                        shape = 0.05

                            else: # AI has more foldable current bet
                                if random.randint(1,5) != 1:
                                    ai_bot.fold()
                                else:
                                    if random.randint(1,9) == 1:
                                        shape = 0.03
                                    else:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
    

                    else: # Smaller Player Raise
                        if random.randint(1,25) <= chen_score:
                            shape = 0.1 + bonus
                        else:
                            if chen_score <= 7: # Weaker Pocket
                                if current_bet <= chips // 30:
                                    if random.randint(1,7) <= 2:
                                        return ai_bot.fold()
                                    else:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
                                else:
                                    if random.randint(1,3) == 1:
                                        return ai_bot.call(raise_state[1], ai_initial_chips)
                                    else:
                                        shape = 0.02

                            else: # Stronger Pocket
                                if random.randint(1,6) == 3:
                                    shape = 0.02 + bonus
                                else:
                                    return ai_bot.call(raise_state[1], ai_initial_chips)

                raise_amount = generate_raise(min_bet, max_bet, shape+0.08)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  


            elif hand_rank == 1: # High Card

                if player_raise > chips // 10 and current_bet > chips // 5: # High Raise and High Current Bet
                    if chen_score >= 10: # Strong Pocket
                        if random.randint(1, 2) == 1:
                            return ai_bot.fold()
                        else:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        
                    else: # Weaker Pocket
                        return ai_bot.fold()


                elif player_raise > chips // 10 and current_bet <= chips // 15: # High Raise and Low Current Bet
                    if chen_score >= 10: # Strong Pocket
                        if random.randint(1,4) != 1:
                            if random.randint(1,5) == 1:
                                return ai_bot.call(raise_state[1], ai_initial_chips)
                            else:
                                return ai_bot.fold()
                        else:
                            return ai_bot.fold()

                    else: # Weaker Pocket
                        if random.randint(1,10) == 1:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            return ai_bot.fold()

                elif player_raise < chips // 10 and current_bet > chips // 5: #Lower Raise and High Current Bet
                    if chen_score >= 12: # Strong Pocket
                        if random.randint(1, 3) == 1:
                            shape = 0.06
                        else:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                    else: # Weaker Pocket
                        if random.randint(1,5) == 1:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            return ai_bot.fold()


                elif player_raise < chips // 10 and current_bet <= chips // 20: # Lower Raise and Low Current Bet
                    if chen_score >= 8: # Strong Pocket
                        if random.randint(1, 3) == 1:
                            return ai_bot.call(raise_state[1], ai_initial_chips)
                        else:
                            return ai_bot.fold()

                    else: # Weaker Pocket
                        if random.randint(1,5) != 1:
                            return ai_bot.fold()
                        else:
                            return ai_bot.call(raise_state[1], ai_initial_chips)

                else:
                    ai_bot.fold()

                raise_amount = generate_raise(min_bet, max_bet, shape+0.04)
                return ai_bot.raise_bet(raise_amount, ai_initial_chips, current_bet)  

'''
ai_bot = Bot()
deck = shuffle_deck()
com1 = deck[3:6]
com2 = deck[3:7]
com3 = deck[3:8]
pocket = deck[0:2]
n = 0

while(n < 10000):
    ai_bot = Bot()
    print(n, "\n")
    decision1 = play_state_post(ai_bot, pocket, com1, round(random.randint(200, 15000), -2), [False], 2)
    decision2 = play_state_post(ai_bot, pocket, com2, round(random.randint(200, 15000), -2), [False], 3)
    decision3 = play_state_post(ai_bot, pocket, com3, round(random.randint(200, 15000), -2), [False], 4)
    if decision1 == None or decision2 == None or decision3 == None:
        raise Exception("Code not functioning correctly")
    print("decision 1 is", decision1)
    print("decision 2 is", decision2)
    print("decision 3 is", decision3)


    print("\nPlayer Raised:")#
    ai_bot = Bot()
    decision1 = play_state_post(ai_bot, pocket, com1, random.randint(200, 15000), [True, round(random.randint(200, 50000), -2)], 2)
    decision2 = play_state_post(ai_bot, pocket, com2, random.randint(200, 15000), [True, round(random.randint(200, 50000), -2)], 3)
    decision3 = play_state_post(ai_bot, pocket, com3, random.randint(200, 15000), [True, round(random.randint(200, 50000), -2)], 4)
    if decision1 == None or decision2 == None or decision3 == None:
        raise Exception("Code not functioning correctly")
    print("decision 1 is", decision1)
    print("decision 2 is", decision2)
    print("decision 3 is", decision3)

    n += 1
'''