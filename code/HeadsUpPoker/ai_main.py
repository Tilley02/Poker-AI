from ai_base_strategy import base
import joblib


# load in trained model
model = joblib.load('trained_model.pkl')


'''
Orchestrates the overall AI behavior.
Combines the base play style and opponent modeling to make decisions during the game.
'''

def ai(bot, gamestate, pocket, raise_state, ai_current_bet, known_community, player_action, ai_initial_chips):
    action = base(bot, gamestate, pocket, raise_state, ai_current_bet, known_community, ai_initial_chips)
    # ai_action = model.predict([gamestate])
    # print(action)

    # return ai_action
    return action

# ai(None, None, None, None, None, None, None, None)
