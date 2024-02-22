from determine_hand_strength import Hand
from ai_actions import Bot
from ai_play_state_1 import play_state_1
from ai_play_post_flop import play_state_post

def base(bot, game_state, pocket, raise_state, ai_current_bet, known_community, ai_initial_chips):
    if game_state == 1:
        return play_state_1(bot, pocket, ai_current_bet, raise_state, ai_initial_chips)
    elif game_state == 2:
        return play_state_post(bot, pocket, known_community, ai_current_bet, raise_state, game_state, ai_initial_chips)
    elif game_state == 3:
        return play_state_post(bot, pocket, known_community, ai_current_bet, raise_state, game_state, ai_initial_chips)
    elif game_state == 4:
        return play_state_post(bot, pocket, known_community, ai_current_bet, raise_state, game_state, ai_initial_chips)