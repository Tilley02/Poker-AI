# Left off wanting to only look at cases where everyone bar two people fold before the flop or during the flop
# edit the txt files for missing info, ie board at end of hand etc, might have to add more stuff to be added to the database


import re
import mysql.connector

# Connect to MySQL database
cnx = mysql.connector.connect(user='root', password='12345678',
                              host='localhost', database='poker_ai_db')
cursor = cnx.cursor()

if cnx.is_connected():
    print("Connected to the MySQL database.")
else:
    print("Not connected to the MySQL database.")

# Read file, going file by file
with open('/Users/conortilley/Desktop/CA326_project/holdem_dataset/pluribus_30.txt', 'r') as file:
    data = file.read()
    # print(data)  # Print contents of the file

# Splitting data
hands = re.split(r'PokerStars Hand #\d+:', data)[1:]
# print(hands[0:1])

hand_id = 1 # start at first hand

# Going through each hand
for hand in hands:
    try:
        # Taking data from hand
        table_name = re.search(r"Table '(.+)'", hand).group(1)  # works
        
        if "Table" in hand:
            print(f"Hand Number: {hand_id}")  # Print hand number for debugging
            hand_id += 1
            if action.startswith("*** FLOP ***"):
                game_phase = "flop"
            elif action.startswith("*** TURN ***"):
                game_phase = "turn"
            elif action.startswith("*** RIVER ***"):
                game_phase = "river"
            elif action.startswith("*** SHOWDOWN ***"):
                game_phase = "showdown" 

        seat_player_stack_matches = re.findall(r'Seat (\d+): (.+?) \((\d+) in chips\)', hand)
        for seat_num, player_name, starting_stack in seat_player_stack_matches:
            # Extracting player_id from players table
            query_player_id = f"SELECT player_id FROM players WHERE player_name = '{player_name}'"
            cursor.execute(query_player_id)
            result = cursor.fetchone()
            if result:
                player_id = result[0]

            hand_strength = re.search(rf'Dealt to {player_name} \[(.+)\]', hand)
            if hand_strength:
                hand_strength = hand_strength.group(1)
            else:
                hand_strength = None

        # Extract player actions
        actions = re.findall(r'(.+?): (.+)$', hand, re.MULTILINE)
        
        for player, action in actions:
            print("Action:", action)  # Debugging statement to check the action encountered

            # Debugging statement to check the game_phase
            print("Game Phase:", game_phase)

            # Extracting action type
            action_type_match = re.match(r'(?:posts bets|raises|calls|folds)', action)
            if action_type_match:
                action_type = action_type_match.group()

                # Extracting action amount
                action_amount_match = re.search(r'\b(\d+)\b', action)  # Gets the amount of chips
                if action_amount_match:
                    action_amount = action_amount_match.group(1)
                else:
                    action_amount = None

                if action_type != "unknown":  # So we dont include it in the database
                    # Printing the action details (for debugging purposes)
                    print(f"Hand ID: {hand_id}, Player: {player}, Action: {action}, Action Type: {action_type}, Action Amount: {action_amount}, Game Phase: {game_phase}")

        # working on this
        # pre_flop_actions_match = re.search(r'\*\*\* HOLE CARDS \*\*\*(.*?)\*\*\*', hand, re.DOTALL)
        # if pre_flop_actions_match:
        #     pre_flop_actions = pre_flop_actions_match.group(1).strip()
        #     # print(pre_flop_actions)

        #     # Extracting player actions
        #     player_actions = re.findall(r'(.+): (.+)$', pre_flop_actions, re.MULTILINE)
        #     for player, action in player_actions:
        #         print(f'{player}: {action}')
        #     print('-' * 20) # separates each hand
        
        
        # turn_actions = re.search(r'\*\*\* TURN \*\*\*(.+?)\*\*\* SUMMARY \*\*\*', hand, re.DOTALL).group(1).strip()  # Gets turn card & actions before river
        # river_actions = re.search(r'\*\*\* RIVER \*\*\*(.+?)\*\*\* SHOWDOWN \*\*\*', hand, re.DOTALL).group(1).strip()  # Gets river card & actions before showdown
        # outcome = re.search(r'and won', hand).group(1) # not in every hand in the data, need to change, look in data for who collected pot, add them in as winner
        # final_hand_strength = re.search(r'Board \[(.+)\]', hand).group(1) # not in every hand in the data, need to change
        # community_cards = re.search(r'Board \[.+?\] (.+)', hand)
        # pot_size = re.search(r'Total pot (\d+)', hand).group(1)

        # Put game data in games table
        # insert_game_query = f"INSERT INTO games (table_name, small_blind_player, big_blind_player, community_cards, pot_size) VALUES ('{table_name}', '{small_blind_player}', '{big_blind_player}', '{community_cards}', {pot_size})"
        # cursor.execute(insert_game_query)
        # game_id = cursor.lastrowid # lastrow of game table

        # # Put player data in players table
        # insert_player_query = f"INSERT INTO players (game_id, player_name, seat_num, starting_stack, final_stack, outcome, hand_strength) VALUES ({game_id}, '{player_name}', {seat_num}, {starting_stack}, {starting_stack}, '{outcome}', '{hand_strength}')"
        # cursor.execute(insert_player_query)
        # player_id = cursor.lastrowid # lastrow of player table

        # # Put action data in actions table
        # insert_action_query = f"INSERT INTO actions (player_id, game_phase, action_detail) VALUES ({player_id}, 'pre_flop', '{pre_flop_actions}')"
        # cursor.execute(insert_action_query)
        # insert_action_query = f"INSERT INTO actions (player_id, game_phase, action_detail) VALUES ({player_id}, 'flop', '{flop_actions}')"
        # cursor.execute(insert_action_query)
        # insert_action_query = f"INSERT INTO actions (player_id, game_phase, action_detail) VALUES ({player_id}, 'turn', '{turn_actions}')"
        # cursor.execute(insert_action_query)
        # insert_action_query = f"INSERT INTO actions (player_id, game_phase, action_detail) VALUES ({player_id}, 'river', '{river_actions}')"
        # cursor.execute(insert_action_query)
    
    # For if get an error as traversing through hands
    except Exception as e:
        print(f"Error processing hand: {hand[:100]}")  # Prints the first 100 characters of the hand for context
        raise e

# Commit and close connection
cnx.commit()
cursor.close()
cnx.close()
