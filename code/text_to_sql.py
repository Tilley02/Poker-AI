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


# declaring variables
hand_id = 1 # start at first hand
blind_small = None
blind_big = None
small_blind_amount = None
big_blind_amount = None

# Going through each hand
for hand in hands:
    try:
        # add info to hands_data table first

        table_name = re.search(r"Table '(.+)'", hand).group(1)  # works
        # print(table_name)
        
        blinds_match = re.findall(r"(.+?): posts (small blind|big blind) (\d+)", hand)
        if blinds_match:
            for match in blinds_match:
                player_name = match[0]
                blind_type = match[1]
                blind_amount = int(match[2])
                if blind_type == "small blind":
                    blind_small = player_name
                    small_blind_amount = blind_amount
                    # print(f'small blind player - {blind_small}')
                    # print(f'small blind amount - {small_blind_amount}')
                elif blind_type == "big blind":
                    blind_big = player_name
                    big_blind_amount = blind_amount
                    # print(f'big blind player - {blind_big}')
                    # print(f'big blind amount - {big_blind_amount}')

                # print('test to see where printed')


            # inserting info into hands_data table, only need to do this once per file
            # insert_game_query = f"INSERT INTO hands (table_name, small_blind_player, small_blind_seat, small_blind_chips, big_blind_player, big_blind_seat, big_blind_chips) VALUES ('{table_name}', '{blind_small}', 1, '{small_blind_amount}', '{blind_big}', 2, '{big_blind_amount}')"
            # cursor.execute(insert_game_query)
            # cnx.commit()


        # inserting info in player_data table
        
        
        
        # if "Table" in hand:
        #     # print(f"Hand Number: {hand_id}")  # Print hand number for debugging
        #     hand_id += 1
        #     game_phase = 'preflop'  # Reset game phase for each new hand

        # seat_player_stack_matches = re.findall(r'Seat (\d+): (.+?) \((\d+) in chips\)', hand)
        # num_of_folds = 0 # to keep track of players folded
        # for seat_num, player_name, starting_stack in seat_player_stack_matches:
        #     # print(f"Seat: {seat_num}, Player: {player_name}, Starting Stack: {starting_stack}") # gets seat num, player, starting chips

        #     hand_strength = re.search(rf'Dealt to {player_name} \[(.+)\]', hand)
        #     if hand_strength:
        #         hand_strength = hand_strength.group(1) # prints out all dealt hands from the hole, line by line
        #         # print(hand_strength)

        # # Extract player actions
        # actions = re.findall(r'(.+?): (.+)$', hand, re.MULTILINE) # captures all actions, in sets in list
        # # print(actions)
        
        # for player, action in actions:
        #     if action.startswith("*** FLOP ***"):
        #         game_phase = "flop"
        #         if num_of_folds == len(seat_player_stack_matches) - 2: # checks only two players left, continue with this
        #             # Process the hand further (e.g., insert into database)
        #             pass

        #     if action.startswith("*** FLOP ***"):
        #         game_phase = "flop"
        #     elif action.startswith("*** TURN ***"):
        #         game_phase = "turn"
        #     elif action.startswith("*** RIVER ***"):
        #         game_phase = "river"
        #     elif action.startswith("*** SHOWDOWN ***"):
        #         game_phase = "showdown"

        #     # Extracting action type
        #     action_type_match = re.match(r'(?:posts bets|raises|calls|folds)', action)
        #     if action_type_match:
        #         action_type = action_type_match.group() # captures all action types
        #         if action_type == "folds":
        #             num_of_folds += 1

        #         # Extracting action amount
        #         action_amount_match = re.search(r'\b(\d+)\b', action)  # Gets the amount of chips
        #         if action_amount_match:
        #             action_amount = action_amount_match.group(1)
        #             # print(action_amount) # missing gogo's last bet of 1000
        #         else:
        #             action_amount = None

                # if action_type != "unknown":  # So we dont include it in the database
                    # Printing the action details (for debugging purposes)
                    # print(f"Hand ID: {hand_id}, Player: {player}, Action: {action}, Action Type: {action_type}, Action Amount: {action_amount}, Game Phase: {game_phase}")

        
        # turn_actions = re.search(r'\*\*\* TURN \*\*\*(.+?)\*\*\* SUMMARY \*\*\*', hand, re.DOTALL).group(1).strip()  # Gets turn card & actions before river
        # river_actions = re.search(r'\*\*\* RIVER \*\*\*(.+?)\*\*\* SHOWDOWN \*\*\*', hand, re.DOTALL).group(1).strip()  # Gets river card & actions before showdown
        # outcome = re.search(r'and won', hand).group(1) # not in every hand in the data, need to change, look in data for who collected pot, add them in as winner
        # final_hand_strength = re.search(r'Board \[(.+)\]', hand).group(1) # not in every hand in the data, need to change
        # community_cards = re.search(r'Board \[.+?\] (.+)', hand)
        # pot_size = re.search(r'Total pot (\d+)', hand).group(1)
        
        
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
