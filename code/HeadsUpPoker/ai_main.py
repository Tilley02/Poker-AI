from ai_base_strategy import base
#import joblib


# load in trained model
#model = joblib.load('trained_model.pkl')


'''
Orchestrates the overall AI behavior.
Combines the base play style and opponent modeling to make decisions during the game.
'''

def ai(bot, gamestate, pocket, raise_state, ai_current_bet, known_community, player_action, ai_initial_chips):
    action = base(bot, gamestate, pocket, raise_state, ai_current_bet, known_community, ai_initial_chips)
    # ai_action = model.predict([gamestate])
    # print("Base Action:", action)
    # print("AI Action:", ai_action)

    # return ai_action
    return action



# # Sample game state below


# bot = None  # Placeholder for the bot
# gamestate = {
#     'current_round': 2,  # Example: Current round of the game
#     'current_pot': 1000,  # Example: Current pot size
#     # Add other relevant game state variables here
# }
# pocket = [
#     {'suit': 'Hearts', 'rank': 'Ace'},  # Example: AI's pocket cards
#     {'suit': 'Spades', 'rank': 'King'}
# ]
# raise_state = (False, 0)  # Example: No raise has been made yet
# ai_current_bet = 100  # Example: AI's current bet
# known_community = [
#     {'suit': 'Diamonds', 'rank': 'Queen'},  # Example: Community cards
#     {'suit': 'Clubs', 'rank': 'Jack'},
#     {'suit': 'Hearts', 'rank': 'Ten'}
# ]
# player_action = 'raise'  # Example: Last player action
# ai_initial_chips = 5000  # Example: AI's initial chip count

# # Call the AI function with the sample game state
# action = ai(bot, gamestate, pocket, raise_state, ai_current_bet, known_community, player_action, ai_initial_chips)

# print("AI Action:", action)