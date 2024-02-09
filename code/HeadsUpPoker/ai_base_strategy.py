'''
Defines the default play style for the AI when it doesn't have enough information about opponents.

Chen Formula is used:

Short-handed strategy.
Early position.

    Raise = 8 points or more.
    Call = 7 points or less.

Mid position.

    Raise = 7 points or more.
    call = 6 points or less.

Late position.

    Raise = 6 points or more.
    call = 5 points or less.

"Raise" = Raise if there have been no raises or calls before you.
"call" = call regardless if there has been a raise before you or not. Just fold.


'''
from determine_hand_strength import Hand
from chen_formula import chen_formula
from create_player import Player

def base(Bot, gamestate, hand):
    states = {
        1: play_state_1,
        2: play_state_2,
        3: play_state_3,
        4: play_state_4,
        5: play_state_5
    }

    play = states.get(Bot, gamestate)
    play(hand)
        

def play_state_1(Bot, hand):
    pocket_score = chen_formula(hand)
    if pocket_score >= 8:
        
        if pocket_score > 14:
            Bot.raise_bet()


def play_state_2(hand):
    print(2)
    pass

def play_state_3(hand):
    pass

def play_state_4(hand):
    pass

def play_state_5(hand):
    pass

#deckp = [{'suit': 'Diamonds', 'rank': '14'}, {'suit': 'Hearts', 'rank': '14'}]
#deckp = [{'suit': 'Diamonds', 'rank': '14'}, {'suit': 'Diamonds', 'rank': '13'}]
#base(1, deckp)
