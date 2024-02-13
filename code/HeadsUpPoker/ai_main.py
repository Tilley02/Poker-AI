from ai_base_strategy import base

'''
Orchestrates the overall AI behavior.
Combines the base play style and opponent modeling to make decisions during the game.
'''

def ai_action(bot, gamestate, hand, raise_state, little_blind_amount):
    action = base(bot, gamestate, hand, raise_state, little_blind_amount)
    return action