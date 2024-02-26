from ai_base_strategy import base
import joblib
import numpy as np


# load in trained model
model = joblib.load('trained_model.pkl')


'''
Orchestrates the overall AI behavior.
Combines the base play style and opponent modeling to make decisions during the game.
'''

def ai(bot, gamestate, pocket, raise_state, ai_current_bet, known_community, player_action, ai_initial_chips):
    action = base(bot, gamestate, pocket, raise_state, ai_current_bet, known_community, ai_initial_chips)
    
    # input here the gamestate info/ variable
    #  i.e.
    # gamestate = [4, 3, 2, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.1666667, 0.005, 0.0045, 0, 0]
    
    # uncomment below to use the model
    # gamestate_array = np.array(list(gamestate.values()))[0:19]
    # gamestate_array = gamestate_array.reshape(1, -1)
    # ai_action = model.predict(gamestate_array)
    
    # # based off what ai_actions returns
    # if ai_action[0] == 0:
    #     ai_action = 'fold'
    # elif ai_action[0] == 1:
    #     ai_action = 'check'
    # elif ai_action[0] == 2:
    #     ai_action = 'raise'

    # print("AI Action:", ai_action)
    # return ai_action
    return action
