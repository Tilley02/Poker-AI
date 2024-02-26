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
    # print("Base Action:", action)
    
    input_data = np.array(list(gamestate.values())).reshape(1, -1)
    # print(gamestate.values()) # returns a option from ai_actions.py
    
    ai_action = model.predict(input_data)
    print("AI Action:", ai_action[0]) # returns 0, 1 or 2 depending on the action
    
    # return ai_action
    return action


 
# # Sample game state below


bot = None  # Placeholder for the bot
gamestate = {
    'S1': 4,
    'C1': 3,
    'S2': 2,
    'C2': 9,
    'S3': 0,
    'C3': 0,
    'S4': 0,
    'C4': 0,
    'S5': 0,
    'C5': 0,
    'S6': 0,
    'C6': 0,
    'S7': 0,
    'C7': 0,
    'percentage_of_total_chips_hand': 0.1666667,
    'percentage_of_hand_bet_pot': 0.005,
    'percentage_of_total_chips_in_pot': 0.0045,
    'current_stage': 0,
    'move': 0,
    'player_hand_ranking': 1,
}
pocket = [
    {'suit': '1', 'rank': '1'},  # Example: AI's pocket cards
    {'suit': '2', 'rank': '13'}
]
raise_state = 0  # Example: No raise has been made yet
ai_current_bet = 100  # Example: AI's current bet
known_community = [
    {'suit': '3', 'rank': '12'},  # the know community cards
    {'suit': '4', 'rank': '11'},
    {'suit': '1', 'rank': '10'}
]
player_action = '2'  # Example: Last player action
ai_initial_chips = 5000  # Example: AI's initial chip count

# # Call the AI function with the sample game state
action = ai(bot, gamestate, pocket, raise_state, ai_current_bet, known_community, player_action, ai_initial_chips)

# print("AI Action:", action)