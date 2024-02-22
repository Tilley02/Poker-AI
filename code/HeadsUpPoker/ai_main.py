from ai_base_strategy import base

'''
Orchestrates the overall AI behavior.
Combines the base play style and opponent modeling to make decisions during the game.
'''

def ai(bot, gamestate, pocket, raise_state, ai_current_bet, known_community, player_action, ai_initial_chips):
    action = base(bot, gamestate, pocket, raise_state, ai_current_bet, known_community, ai_initial_chips)
    if action[0] == "fold" and player_action != None:
        if player_action[0] == "check":
            return bot.check()
    return action