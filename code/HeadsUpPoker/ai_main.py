from ai_base_strategy import base

'''
Orchestrates the overall AI behavior.
Combines the base play style and opponent modeling to make decisions during the game.
'''

def ai(bot, gamestate, pocket, raise_state, ai_current_bet, known_community, player_action):
    action = base(bot, gamestate, pocket, raise_state, ai_current_bet, known_community)
    if action[0] == "fold" and player_action[0] == "check":
        return bot.check()
    return action