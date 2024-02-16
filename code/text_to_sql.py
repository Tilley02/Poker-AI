# Left off wanting to only look at cases where everyone bar two people fold before the flop or during the flop
# edit the txt files for missing info, ie board at end of hand etc, might have to add more stuff to be added to the database


import re
import mysql.connector

# connect to mysql
cnx = mysql.connector.connect(user='root', password='12345678',
                              host='localhost', database='poker_ai_db')
cursor = cnx.cursor()

# if cnx.is_connected():
#     print("Connected to the MySQL database.")
# else:
#     print("Not connected to the MySQL database.")

# Read file, going file by file
with open('/Users/conortilley/Desktop/CA326_project/holdem_dataset/pluribus_30.txt', 'r') as file:
    data = file.read()

# Splitting data
hands = re.split(r'PokerStars Hand #\d+:', data)[1:]


# declaring variables
hand_id = 0 # start at first hand
hands_to_process = 80 # number of hands to process, knows when to stop then
rows_per_hand = 0 # tracks num of hands processed
blind_small = None
blind_big = None
small_blind_amount = None
big_blind_amount = None
game_phase = None

# Going through each hand
for hand in hands:
    try:
        
        hand_id += 1
        
        # for hole_cards table insertion
        if hand_id > hands_to_process:
            break

        # add info to hands_data table, need to add button player here but wait until editied to have two players
        # adds all the small and big blinds info for every hand not just when there is two players yet
        table_name = re.search(r"Table '(.+)'", hand).group(1)  # works
        # print(table_name)
        
        # findall gets all occurences of pattern
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
        seat_player_stack_matches = re.findall(r'Seat (\d+): (.+?) \((\d+) in chips\)', hand)
        num_of_folds = 0 # to keep track of players folded, not in use yet
        
        # uncomment below for loop and the insertion lines to run
        # for seat_num, player_name, starting_stack in seat_player_stack_matches:
            
            # inserting info into player_data table, only need to do this once per file
            # insert_game_query = f"INSERT INTO players (player_name, seat_number, chips) VALUES ('{player_name}', {seat_num}, {starting_stack})"
            # cursor.execute(insert_game_query)
            # cnx.commit()
            
            # print(f"Seat: {seat_num}, Player: {player_name}, Starting Stack: {starting_stack}") # gets seat num, player, starting chips
        

        # inserting info into hole_cards table, gets pre-flop cards
        hole_cards_matches = re.findall(r'Dealt to (.+?) \[(..) (..)\]', hand)
        for player_name, card1, card2 in hole_cards_matches:
            cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
            player_ids = cursor.fetchall()
            for player_id in player_ids:
                player_id = player_id[0]
            
            # prints only their last given player id values
            # need to fix, but works for now
            # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Card 1: {card1}, Card 2: {card2}")
            
            # Insert hole cards into the hole_cards table
            # insert_game_query = f"INSERT INTO hole_cards (hand_id, player_id, card1, card2) VALUES ({hand_id}, {player_id}, '{card1}', '{card2}')"
            # cursor.execute(insert_game_query)
            # cnx.commit()
            rows_per_hand += 1

        # Check rows_per_hand divisible by 6
        if rows_per_hand % 6 == 0:
            rows_per_hand = 0
        
        # print('test to see where printed')
        
        
        # inserting info into actions table
        
        # starting with pre-flop actions
        for line in hand.split('\n'):
            
            game_phase = 'pre_flop' # sets game_phase to pre-flop
            # print(game_phase)

            if game_phase == 'pre_flop':
                # fold hands
                pre_flop_fold_match = re.match(r'(.+?): folds', line)
                if pre_flop_fold_match:
                    player_name = pre_flop_fold_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: pre_flop, Action Type: fold, Action Amount: NULL")
                
                    # Insert fold action into actions table
                    # insert_fold_query = f"INSERT INTO actions (hand_id, player_id, game_phase, action_type, action_amount) VALUES ({hand_id}, {player_id}, 'pre_flop', 'fold', NULL)"
                    # cursor.execute(insert_fold_query)
                    # cnx.commit()
                
                
                # raise hands
                pre_flop_raise_match = re.match(r'(.+?): raises (\d+) to (\d+)', line)
                if pre_flop_raise_match:
                    player_name = pre_flop_raise_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: pre_flop, Action Type: raise, Action Amount: {pre_flop_raise_match.group(3)}")
                
                    # Insert raise action into actions table
                    # insert_raise_query = f"INSERT INTO actions (hand_id, player_id, game_phase, action_type, action_amount) VALUES ({hand_id}, {player_id}, 'pre_flop', 'raise', {pre_flop_raise_match.group(3)})"
                    # cursor.execute(insert_raise_query)
                    # cnx.commit()
                
                
                # call the raises hands
                pre_flop_call_match = re.match(r'(.+?): calls (\d+)', line)
                if pre_flop_call_match:
                    player_name = pre_flop_call_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: pre_flop, Action Type: call, Action Amount: {pre_flop_call_match.group(2)}")

                    # Insert call action into actions table
                    # insert_call_query = f"INSERT INTO actions (hand_id, player_id, game_phase, action_type, action_amount) VALUES ({hand_id}, {player_id}, 'pre_flop', 'call', {pre_flop_call_match.group(2)})"
                    # cursor.execute(insert_call_query)
                    # cnx.commit()
                    
                    
                    # left off below here
                    
                
                # Check if flop phase is reached
                if '*** FLOP ***' in line:
                    game_phase = 'flop'
                    print(line)
                    # Exit the loop once the flop line is encountered
                    break


            if game_phase == 'flop':
                # print('in flop stage')
                continue
            elif '*** SUMMARY ***' in line:
                community_cards = re.search(r'Board \[(.*?)\]', hand) # gets community cards, to be added somewhere, nowhere yet
                if community_cards:
                    board_cards = community_cards.group(1).split()
                else:
                    board_cards = []

                # prints community cards
                # if board_cards:
                #     print(board_cards)
                # else:
                #     print([])

            
        
        # print('test to see where printed')
    


        # if "Table" in hand:
        #     # print(f"Hand Number: {hand_id}")  # Print hand number for debugging
        #     hand_id += 1
        #     game_phase = 'preflop'  # Reset game phase for each new hand

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
