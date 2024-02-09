from ai_base_strategy import base

'''
Orchestrates the overall AI behavior.
Combines the base play style and opponent modeling to make decisions during the game.
'''

def AI(Player, game_state, hand):
    base(Player, game_state, hand)