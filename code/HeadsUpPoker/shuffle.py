import random

def shuffle_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13']

    deck = [{'suit': suit, 'rank': rank} for suit in suits for rank in ranks]
    random.shuffle(deck)

    return deck
