'''
----------------------------------{ Pre-Flop }----------------------------------
Chen formula goes up to 20, (Pair of Aces Suited).
If the chen score for the AI's starting hand is 16, there will be a 16/20 chance of the AI raising.
if not, the computer will check or do a small raise. 

Note for possible changes: Deal with raises less than 1/8 of ai's chips, 1/4 etc...

Possible issues: not much variation between way AI bets when player does small raise to medium raise.
--------------------------------------------------------------------------------
'''
import random
import numpy as np
from chen_formula import chen_formula

def play_state_1(ai_bot, hand, big_blind_amount, raise_state):

    chen_score = chen_formula(hand)

    # Player hasn't raised which means that they either checked, or AI is first to bet.
    if raise_state[0] == False:

        x = random.randint(10, 21)
        if big_blind_amount < 5000:
            shape_a, shape_b, shape_c = 0.25, 0.15, 0.02
        else:
            shape_a, shape_b, shape_c = 0.35, 0.25, 0.05 # AI will do higher bets as the blinds increase...

        if x <= chen_score: # random value was less than chen score. (Only chen score's 10 or better will do larger raises)

            min_bet = big_blind_amount * 2
            max_bet = ai_bot.chips
            raise_risk_decider = random.randint(1, 21)

            if raise_risk_decider <= chen_score:

                # Generate a random number
                rand_exp_better_pocket = np.random.exponential(scale=shape_a)
                # Scale the random number to fit within the desired range
                scaled_value_better_pocket = min_bet * 2 + (max_bet - min_bet * 2) * (1 - np.exp(-rand_exp_better_pocket))
                # Ensure that the scaled value is within the desired range
                raise_amount = min(max_bet, max(min_bet * 2, int(scaled_value_better_pocket)))
                # Ensure there is a difference of 100 between each choice
                raise_amount = round(raise_amount / 100) * 100
                return ai_bot.raise_bet(raise_amount)
        
            else:

                # Adjusting for lower risk
                new_max_bet = max_bet // 2
                rand_exp_lower_pocket = np.random.exponential(scale=shape_b)
                scaled_value_lower_pocket = min_bet + (new_max_bet - min_bet) * (1 - np.exp(-rand_exp_lower_pocket))
                # Ensure that the scaled value is within the desired range
                raise_amount = min(new_max_bet, max(min_bet, int(scaled_value_lower_pocket)))
                # Ensure there is a difference of 100 between each choice
                raise_amount = round(raise_amount / 100) * 100
                return ai_bot.raise_bet(raise_amount)
        
        else: # random value was greater than chen score

            x = random.randint(1, 4)

            if x != 1: 
                return ai_bot.check() 
        
            else: #There is a 1 in 3 chance the ai will do a small raise to make it harder to predict.

                min_bet = big_blind_amount
                max_bet = ai_bot.chips // 2
                # Adjusting for lower risk
                rand_exp = np.random.exponential(scale=shape_c)
                scaled_value = min_bet + (max_bet - min_bet) * (1 - np.exp(-rand_exp))
                # Ensure that the scaled value is within the desired range
                raise_amount = min(max_bet, max(min_bet, int(scaled_value)))
                # Ensure there is a difference of 100 between each choice
                raise_amount = round(raise_amount / 100) * 100
                return ai_bot.raise_bet(raise_amount)
            


    else: # Player has raised the bet.

        if chen_score >= 10: # AI has Strong Hand

            x = random.randint(1, 51) 
            if x <= chen_score: # Will raise 20% of the time with a chen score of 10 and 40% of the time with chen score of 20
                shape = 0.006 * chen_score
                min_bet = raise_state[1]
                max_bet = ai_bot.chips
                # Adjusting for lower risk
                rand_exp = np.random.exponential(scale=shape)
                scaled_value = min_bet + (max_bet - min_bet) * (1 - np.exp(-rand_exp))
                # Ensure that the scaled value is within the desired range
                raise_amount = min(max_bet, max(min_bet, int(scaled_value)))
                # Ensure there is a difference of 100 between each choice
                raise_amount = round(raise_amount / 100) * 100
                return ai_bot.raise_bet(raise_amount)

            else:
                return ai_bot.call(raise_state[1]) # Else just call
            


        else: # Chen score is less than 10.

            if chen_score > 5:
            
                if raise_state[1] > ai_bot.chips // 2 and big_blind_amount < ai_bot.chips // 16: # Raise by player is greater than half of ai's chips and small big blind
                    x = random.randint(5, 16)
                    if x <= chen_score -3: # AI will play 20% of time with 9 and 10% of time with 8, otherwise deemed not worth the risk
                        return ai_bot.call(raise_state[1])
                    else:
                        return ai_bot.fold() # Always fold with chen score of 7 or 6

                elif raise_state[1] > ai_bot.chips // 2 and big_blind_amount >= ai_bot.chips // 16: # Raise by player is greater than half of ai's chips and large big blind
                    x = random.randint(1, 11)
                    if x <= chen_score: 
                        return ai_bot.call(raise_state[1])
                    else:
                        return ai_bot.fold()  # 40% chance of folding a 6... 10% of folding 9.
                

                elif raise_state[1] <= ai_bot.chips // 2 and big_blind_amount < ai_bot.chips // 16: # Raise by player is less than half of ai's chips. and small big blind
                    x = random.randint(1, 21)
                    if x <= chen_score + 12: # Will always call/reraise with a chen score of 8 or 9

                        if random.randint(1, 4) == 1: # 33.3% chance of re-raising.
                            shape = 0.03
                            min_bet = raise_state[1]
                            max_bet = ai_bot.chips // 2
                            # Adjusting for smaller bets more often
                            rand_exp = np.random.exponential(scale=shape)
                            scaled_value = min_bet + (max_bet - min_bet) * (1 - np.exp(-rand_exp))
                            # Ensure that the scaled value is within the desired range
                            raise_amount = min(max_bet, max(min_bet, int(scaled_value)))
                            # Ensure there is a difference of 100 between each choice
                            raise_amount = round(raise_amount / 100) * 100
                            return ai_bot.raise_bet(raise_amount)
                        else:
                            return ai_bot.call(raise_state[1]) # Call 75% of the time
                        
                    else:
                        return ai_bot.fold() # fold 10% with a 6 and 5% with a 7.
                

                elif raise_state[1] <= ai_bot.chips // 2 and big_blind_amount >= ai_bot.chips // 16: # Raise by player is less than half of ai's chips and large big blind
                    x = random.randint(1, 11)
                    if x <= chen_score + 3: #Play with a 7, 8, 9 chen score and 90% of the time with a 6.

                        if random.randint(1, 4) == 1: # 33% chance of re-raising.
                            shape = 0.09
                            min_bet = raise_state[1]
                            max_bet = ai_bot.chips // 2
                            # Adjusting for smaller bets more often
                            rand_exp = np.random.exponential(scale=shape)
                            scaled_value = min_bet + (max_bet - min_bet) * (1 - np.exp(-rand_exp))
                            # Ensure that the scaled value is within the desired range
                            raise_amount = min(max_bet, max(min_bet, int(scaled_value)))
                            # Ensure there is a difference of 100 between each choice
                            raise_amount = round(raise_amount / 100) * 100
                            return ai_bot.raise_bet(raise_amount)
                        else:
                            return ai_bot.call(raise_state[1]) # Call 67% of the time
                        
                    else:
                        return ai_bot.fold() # Fold 10% of the time if chen is 6
                    
                else: 
                    return "ERROR when computing state 'Chen Score less than 10, greater than 5'"    
                


            else: # Chen Score is less than or equal to 5 (WEAK POCKET)
                if chen_score < 0:
                    chen_score = 1


                if raise_state[1] > ai_bot.chips // 2 and big_blind_amount < ai_bot.chips // 16: # Raise by player is greater than half of ai's chips and small big blind
                    #WEAK HAND, BIG RAISE, small min bet
                    return ai_bot.fold() # Always fold weak hand with small min bet


                elif raise_state[1] > ai_bot.chips // 2 and big_blind_amount >= ai_bot.chips // 16: # Raise by player is greater than half of ai's chips and large big blind
                    #WEAK HAND, BIG RAISE, Large min bet
                    if big_blind_amount > ai_bot.chips // 8: # Very Large min bet

                        x = random.randint(2, 10) # 50% chance of playing with 5 score, 12.5% chance of playing with 2 score 
                        if x <= chen_score + 2:
                            return ai_bot.call(raise_state[1])
                        else:
                            return ai_bot.fold() # Always fold a 1 or lower chen score. 

                    else: # Slighly more ability to fold these hands
                        x = random.randint(3,15) # 8.33% of playing with 3 score, 16.67% chance of playing with 4 score, 25% with 5 score 
                        if x <= chen_score:
                            return ai_bot.call(raise_state[1])
                        else:
                            return ai_bot.fold() # Always fold a 2 or lower chen score. 
                

                elif raise_state[1] <= ai_bot.chips // 2 and big_blind_amount < ai_bot.chips // 16: # Raise by player is less than half of ai's chips. and small big blind
                    #WEAK HAND, small RAISE, small min bet # Almost never fold
                    x = random.randint(1, 21)
                    if x <= chen_score + 15: # Will always call with 5 and 80% of the time with 1.

                        if random.randint(1, 11) == 1: # 10% chance of re-raising.
                            shape = 0.01 # Skew more towards very small raises
                            min_bet = raise_state[1]
                            max_bet = ai_bot.chips // 2
                            rand_exp = np.random.exponential(scale=shape)
                            scaled_value = min_bet + (max_bet - min_bet) * (1 - np.exp(-rand_exp))
                            # Ensure that the scaled value is within the desired range
                            raise_amount = min(max_bet, max(min_bet, int(scaled_value)))
                            # Ensure there is a difference of 100 between each choice
                            raise_amount = round(raise_amount / 100) * 100
                            return ai_bot.raise_bet(raise_amount)
                        else:
                            return ai_bot.call(raise_state[1]) # Call 90% of the time
                        
                    else:
                        return ai_bot.fold() # fold 20% with a 1 score etc..
                

                elif raise_state[1] <= ai_bot.chips // 2 and big_blind_amount >= ai_bot.chips // 16: # Raise by player is less than half of ai's chips and large big blind
                    #WEAK HAND, Small RAISE, Large min bet
                    x = random.randint(1, 11)
                    if x <= chen_score + 7: #Play 80% of the time with 1 and alwyas with 3, 4 and 5

                        if random.randint(1, 6) == 1: # 20% chance of re-raising.
                            shape = 0.09
                            min_bet = raise_state[1]
                            max_bet = ai_bot.chips // 2
                            # Adjusting for smaller bets more often
                            rand_exp = np.random.exponential(scale=shape)
                            scaled_value = min_bet + (max_bet - min_bet) * (1 - np.exp(-rand_exp))
                            # Ensure that the scaled value is within the desired range
                            raise_amount = min(max_bet, max(min_bet, int(scaled_value)))
                            # Ensure there is a difference of 100 between each choice
                            raise_amount = round(raise_amount / 100) * 100
                            return ai_bot.raise_bet(raise_amount)
                        else:
                            return ai_bot.call(raise_state[1]) # Call 80% of the time
                        
                    else:
                        return ai_bot.fold() # Fold 20% of time score is 1 etc..
                    

                else: 
                    return "ERROR when computing state 'Chen Score less than 5'"                
                
