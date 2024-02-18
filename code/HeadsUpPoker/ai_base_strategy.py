from determine_hand_strength import Hand
from ai_actions import Bot
from ai_play_state_1 import play_state_1

from shuffle import shuffle_deck

def base(bot, gamestate, hand, raise_state, ai_current_bet):
    states = {
        1: play_state_1,
        2: play_state_2,
        3: play_state_3,
        4: play_state_4,
        5: play_state_5
    }

    play = states.get(gamestate)
    return play(bot, hand, ai_current_bet, raise_state)

        


'''
----------------------------------{ Pre-Flop }----------------------------------
Chen formula goes up to 20, (Pair of Aces Suited).
If the chen score for the AI's starting hand is 16, there will be a 16/20 chance of the AI raising.
if not, the computer will check or do a small raise. 

AI does not fold pre-flop
--------------------------------------------------------------------------------
'''

            
def play_state_2(hand):
    print(2)
    pass

def play_state_3(hand):
    pass

def play_state_4(hand):
    pass

def play_state_5(hand):
    pass


'''
ai_bot = Bot()
deck = shuffle_deck()
print(deck[0:2])


print("\nPlayer did small raise:")
action = base(ai_bot, 1, deck[0:2], [True, 1000], 500)
print(action, "Min bet was 500")
action = base(ai_bot, 1, deck[0:2], [True, 1000], 1000)
print(action, "Min bet was 1,000")
action = base(ai_bot, 1, deck[0:2], [True, 1000], 3000)
print(action, "Min bet was 3,000")
action = base(ai_bot, 1, deck[0:2], [True, 1000], 10000)
print(action, "Min bet was 10,000")
action = base(ai_bot, 1, deck[0:2], [True, 1000], 20000)
print(action, "Min bet was 20,000")
print("\n----------------------------------------------------------\n")


ai_bot = Bot()
print("\nPlayer did medium raise:")
action = base(ai_bot, 1, deck[0:2], [True, 10000], 500)
print(action, "Min bet was 500")
action = base(ai_bot, 1, deck[0:2], [True, 10000], 1000)
print(action, "Min bet was 1,000")
action = base(ai_bot, 1, deck[0:2], [True, 10000], 3000)
print(action, "Min bet was 3,000")
action = base(ai_bot, 1, deck[0:2], [True, 10000], 10000)
print(action, "Min bet was 10,000")
action = base(ai_bot, 1, deck[0:2], [True, 10000], 20000)
print(action, "Min bet was 20,000")
print("\n----------------------------------------------------------\n")


ai_bot = Bot()
print("\nPlayer did large raise:")
action = base(ai_bot, 1, deck[0:2], [True, 30000], 500)
print(action, "Min bet was 500")
action = base(ai_bot, 1, deck[0:2], [True, 30000], 1000)
print(action, "Min bet was 1,000")
action = base(ai_bot, 1, deck[0:2], [True, 30000], 3000)
print(action, "Min bet was 3,000")
action = base(ai_bot, 1, deck[0:2], [True, 30000], 10000)
print(action, "Min bet was 10,000")
action = base(ai_bot, 1, deck[0:2], [True, 30000], 20000)
print(action, "Min bet was 20,000")
print("\n----------------------------------------------------------\n")


ai_bot = Bot()
print("\nPlayer didn't raise:")
#Player did not raise
action = base(ai_bot, 1, deck[0:2], [False], 500)
print(action, "Min bet was 500")
action = base(ai_bot, 1, deck[0:2], [False], 1000)
print(action, "Min bet was 1,000")
action = base(ai_bot, 1, deck[0:2], [False], 3000)
print(action, "Min bet was 3,000")
action = base(ai_bot, 1, deck[0:2], [False], 10000)
print(action, "Min bet was 10,000")
action = base(ai_bot, 1, deck[0:2], [False], 20000)
print(action, "Min bet was 20,000")
print("\n----------------------------------------------------------\n")
'''