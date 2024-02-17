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
        
        # not working yet, need to fix
        # check for 4 folds in hand before flop
        fold_count = 0
        for line in hand.split('\n'):
            # print(line) # prints out every line of .txt file
            if line.startswith('*** FLOP ***'):
                break
            if line == '*** SUMMARY ***':
                break
            if re.match(r'(.+?): folds', line):
                # print(line) # prints all the fold lines out
                fold_count += 1
                # print(fold_count)

        # print('gap')
        # print(fold_count)
        
        # if 4 or more folds continue through rest of hand
        if fold_count < 4:
            continue

            
        # print(fold_count)
        

        # inserting info in player_data table
        seat_player_stack_matches = re.findall(r'Seat (\d+): (.+?) \((\d+) in chips\)', hand)
        
        # uncomment below for loop and the insertion lines to run
        # for seat_num, player_name, starting_stack in seat_player_stack_matches:
            
            # inserting info into player_data table, only need to do this once per file
            # insert_game_query = f"INSERT INTO players (player_name, seat_number, chips) VALUES ('{player_name}', {seat_num}, {starting_stack})"
            # cursor.execute(insert_game_query)
            # cnx.commit()
            
            # print(f"Seat: {seat_num}, Player: {player_name}, Starting Stack: {starting_stack}") # gets seat num, player, starting chips
        
                
        hand_id += 1    # increment hand_id by 1
 
        # add info to hands_data table, need to add button player here but wait until editied to have two players
        # adds all the small and big blinds info for every hand not just when there is two players yet
        
        table_name = re.search(r"Table '(.+)'", hand).group(1)  # works
        blinds_match = re.findall(r"(.+?): posts (small blind|big blind) (\d+)", hand)
        button_player = re.search(r"Seat (\d+): (.+?) \((\d+) in chips\)", hand)

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

        player_name = button_player.group(2)
        cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
        player_ids = cursor.fetchall()
        for player_id in player_ids:
            player_id = player_id[0]
        
        # print(f"Hand ID: {hand_id}, Table: {table_name}, Small Blind Player: {blind_small}, Small Blind Seat: 1, Small Blind Amount: {small_blind_amount}, Big Blind Player: {blind_big}, Big Blind Seat: 2, Big Blind Amount: {big_blind_amount}, Button Player: '{player_id}'")

        # inserting info into hands_data table, only need to do this once per file
        # insert_game_query = f"INSERT INTO hands (table_name, small_blind_player, small_blind_seat, small_blind_chips, big_blind_player, big_blind_seat, big_blind_chips) VALUES ('{table_name}', '{blind_small}', 1, '{small_blind_amount}', '{blind_big}', 2, '{big_blind_amount}')"
        # cursor.execute(insert_game_query)
        # cnx.commit()



        # for hole_cards table insertion, so doesn't go over 80 (amount of hands per .txt file)
        if hand_id > hands_to_process:
            break

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
        
        game_phase = 'pre_flop' # sets game_phase to pre-flop, to start
        for line in hand.split('\n'):

            # starting with pre-flop actions
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
                    insert_fold_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'pre_flop', {player_id}, 'fold', NULL)"
                    cursor.execute(insert_fold_query)
                    cnx.commit()
                
                
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
                    insert_raise_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'pre_flop', {player_id}, 'raise', {pre_flop_raise_match.group(3)})"
                    cursor.execute(insert_raise_query)
                    cnx.commit()
                
                
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
                    insert_call_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'pre_flop', {player_id}, 'call', {pre_flop_call_match.group(2)})"
                    cursor.execute(insert_call_query)
                    cnx.commit()
                
                
                # the uncalled hands
                uncalled_bet_match = re.search(r'Uncalled bet \((\d+)\) returned to (.+)', line)
                if uncalled_bet_match:
                    returned_amount = int(uncalled_bet_match.group(1))
                    player_name = uncalled_bet_match.group(2)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]

                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: pre_flop, Action Type: uncalled_bet, Action Amount: {returned_amount}")
                    
                    # Insert uncalled bet returned action into actions table
                    insert_returned_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'pre_flop', {player_id}, 'uncalled_bet_returned', {returned_amount})"
                    cursor.execute(insert_returned_query)
                    cnx.commit()
                
                
                # for the hand_summanry table now, for if there is a winner before the flop, this works correctly
                board_cards = []
                collected_amount = re.search(r'(.+?) collected (\d+\.\d+) from pot', line)
                if collected_amount:
                    player_name = collected_amount.group(1)
                    pot_amount = float(collected_amount.group(2))
                    formatted_pot_amount = f"{pot_amount:.2f}"
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                        
                    # captures the hole cards of the winner
                    cursor.execute(f"SELECT card1, card2 FROM hole_cards WHERE hand_id = {hand_id} AND player_id = {player_id}")
                    hole_cards = cursor.fetchall()
                    for hole_card in hole_cards:
                        hole_card = hole_card[0] + ' ' + hole_card[1]
                    
                    # print(f"Hand ID: {hand_id}, Pot size: {formatted_pot_amount}, Community cards: '{board_cards}', Winner: {player_id}, Winning hand: '{hole_card}'")
                
                    # Insert collected pot into hand_summary table
                    insert_collected_query = f"INSERT INTO hand_summary (hand_id, pot_size, community_cards, winner_id, winning_hand) VALUES ({hand_id}, {formatted_pot_amount}, '{board_cards}', {player_id}, '{hole_card}')"
                    cursor.execute(insert_collected_query)
                    cnx.commit()
                    
                    
                
                # Check if summary phase reached first then flop phase
                if '*** SUMMARY ***' in line:
                    game_phase = 'summary'
                    # print(line)
                    continue
                elif '*** FLOP ***' in line:
                    flop_cards = re.search(r'\[([2-9TJQKA][cdhs] [2-9TJQKA][cdhs] [2-9TJQKA][cdhs])\]', hand)
                    if flop_cards:
                        board_cards = flop_cards.group(1).split()
                        # print(board_cards)
                    game_phase = 'flop'
                    continue
                

            # flop actions
            elif game_phase == 'flop':
                # print(line)
                # print(game_phase)

                # fold hands
                flop_fold_match = re.match(r'(.+?): folds', line)
                if flop_fold_match:
                    player_name = flop_fold_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: flop, Action Type: fold, Action Amount: NULL")
               
                    # Insert fold action into actions table
                    insert_fold_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'flop', {player_id}, 'fold', NULL)"
                    cursor.execute(insert_fold_query)
                    cnx.commit()
 
 
                # raise hands
                flop_raise_match = re.match(r'(.+?): raises (\d+) to (\d+)', line)
                if flop_raise_match:
                    player_name = flop_raise_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: flop, Action Type: raise, Action Amount: {flop_raise_match.group(3)}")
                
                    # Insert raise action into actions table
                    insert_raise_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'flop', {player_id}, 'raise', {flop_raise_match.group(3)})"
                    cursor.execute(insert_raise_query)
                    cnx.commit()
                
                
                # call the raises hands
                flop_call_match = re.match(r'(.+?): calls (\d+)', line)
                if flop_call_match:
                    player_name = flop_call_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: flop, Action Type: call, Action Amount: {flop_call_match.group(2)}")

                    # Insert call action into actions table
                    insert_call_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'flop', {player_id}, 'call', {flop_call_match.group(2)})"
                    cursor.execute(insert_call_query)
                    cnx.commit()


                # the bet hands
                flop_bet_match = re.match(r'(.+?): bets (\d+)', line)
                if flop_bet_match:
                    player_name = flop_bet_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: flop, Action Type: bet, Action Amount: {flop_bet_match.group(2)}")

                    # Insert bet action into actions table
                    insert_bet_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'flop', {player_id}, 'bet', {flop_bet_match.group(2)})"
                    cursor.execute(insert_bet_query)
                    cnx.commit()
                    

                # the check hands
                flop_check_match = re.match(r'(.+?): checks', line)
                if flop_check_match:
                    player_name = flop_check_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: flop, Action Type: check, Action Amount: NULL")

                    # Insert check action into actions table
                    insert_check_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'flop', {player_id}, 'check', NULL)"
                    cursor.execute(insert_check_query)
                    cnx.commit()
                
                
                # the uncalled hands
                uncalled_bet_match = re.search(r'Uncalled bet \((\d+)\) returned to (.+)', line)
                if uncalled_bet_match:
                    returned_amount = int(uncalled_bet_match.group(1))
                    player_name = uncalled_bet_match.group(2)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: flop, Action Type: uncalled_bet, Action Amount: {returned_amount}")
                    
                    # Insert uncalled bet returned action into actions table
                    insert_returned_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'flop', {player_id}, 'uncalled_bet_returned', {returned_amount})"
                    cursor.execute(insert_returned_query)
                    cnx.commit()
                    
                    
                # for the hand_summanry table now, for if there is a winner before the turn
                board_cards_flop = board_cards
                board_cards_str = ', '.join(board_cards_flop)
                collected_amount = re.search(r'(.+?) collected (\d+\.\d+) from pot', line)
                if collected_amount:
                    player_name = collected_amount.group(1)
                    pot_amount = float(collected_amount.group(2))
                    formatted_pot_amount = f"{pot_amount:.2f}"
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                        
                    # cursor.execute(f"SELECT card1, card2 FROM hole_cards WHERE hand_id = {hand_id} AND player_id = {player_id}")
                    hole_cards = cursor.fetchall()
                    for hole_card in hole_cards:
                        hole_card = hole_card[0] + ' ' + hole_card[1]
                    
                    # print(f"Hand ID: {hand_id}, Pot size: {formatted_pot_amount}, Community cards: '{board_cards_flop}', Winner: {player_id}, Winning hand: '{hole_card}'")
                
                    # Insert collected pot into hand_summary table
                    insert_collected_query = f"INSERT INTO hand_summary (hand_id, pot_size, community_cards, winner_id, winning_hand) VALUES ({hand_id}, {formatted_pot_amount}, '{board_cards_str}', {player_id}, '{hole_card}')"
                    cursor.execute(insert_collected_query)
                    cnx.commit()
                

                if '*** SUMMARY ***' in line:
                    game_phase = 'summary'
                    # print(line)
                    continue
                elif '*** TURN ***' in line:
                    turn_cards = re.search(r'\[([2-9TJQKA][cdhs] [2-9TJQKA][cdhs] [2-9TJQKA][cdhs])\] \[([2-9TJQKA][cdhs])\]', hand)
                    if turn_cards:
                        board_cards = turn_cards.group(1).split() + [turn_cards.group(2)]
                        # print(board_cards)
                    game_phase = 'turn'
                    # print(line)
                    continue


            # turn actions
            elif game_phase == 'turn':
                # print(line)
                # print(game_phase)

                # turn hands
                turn_fold_match = re.match(r'(.+?): folds', line)
                if turn_fold_match:
                    player_name = turn_fold_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: turn, Action Type: fold, Action Amount: NULL")
               
                    # Insert fold action into actions table
                    insert_fold_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'turn', {player_id}, 'fold', NULL)"
                    cursor.execute(insert_fold_query)
                    cnx.commit()
 
 
                # raise hands
                turn_raise_match = re.match(r'(.+?): raises (\d+) to (\d+)', line)
                if turn_raise_match:
                    player_name = turn_raise_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: turn, Action Type: raise, Action Amount: {turn_raise_match.group(3)}")
                
                    # Insert raise action into actions table
                    insert_raise_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'turn', {player_id}, 'raise', {turn_raise_match.group(3)})"
                    cursor.execute(insert_raise_query)
                    cnx.commit()
                
                
                # call the raises hands
                turn_call_match = re.match(r'(.+?): calls (\d+)', line)
                if turn_call_match:
                    player_name = turn_call_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: turn, Action Type: call, Action Amount: {turn_call_match.group(2)}")

                    # Insert call action into actions table
                    insert_call_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'turn', {player_id}, 'call', {turn_call_match.group(2)})"
                    cursor.execute(insert_call_query)
                    cnx.commit()


                # the bet hands
                turn_bet_match = re.match(r'(.+?): bets (\d+)', line)
                if turn_bet_match:
                    player_name = turn_bet_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: turn, Action Type: bet, Action Amount: {turn_bet_match.group(2)}")

                    # Insert bet action into actions table
                    insert_bet_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'turn', {player_id}, 'bet', {turn_bet_match.group(2)})"
                    cursor.execute(insert_bet_query)
                    cnx.commit()
                    

                # the check hands
                turn_check_match = re.match(r'(.+?): checks', line)
                if turn_check_match:
                    player_name = turn_check_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: turn, Action Type: check, Action Amount: NULL")

                    # Insert check action into actions table
                    insert_check_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'turn', {player_id}, 'check', NULL)"
                    cursor.execute(insert_check_query)
                    cnx.commit()
                    
                    
                # the uncalled hands
                uncalled_bet_match = re.search(r'Uncalled bet \((\d+)\) returned to (.+)', line)
                if uncalled_bet_match:
                    returned_amount = int(uncalled_bet_match.group(1))
                    player_name = uncalled_bet_match.group(2)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: turn, Action Type: uncalled_bet, Action Amount: {returned_amount}")
                    
                    # Insert uncalled bet returned action into actions table
                    insert_returned_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'turn', {player_id}, 'uncalled_bet_returned', {returned_amount})"
                    cursor.execute(insert_returned_query)
                    cnx.commit()
                
                
                # for the hand_summanry table now, for if there is a winner before the river
                board_cards_turn = board_cards
                board_cards_str = ', '.join("'" + card + "'" for card in board_cards_turn)
                collected_amount = re.search(r'(.+?) collected (\d+\.\d+) from pot', line)
                if collected_amount:
                    player_name = collected_amount.group(1)
                    pot_amount = float(collected_amount.group(2))
                    formatted_pot_amount = f"{pot_amount:.2f}"
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                        
                    # cursor.execute(f"SELECT card1, card2 FROM hole_cards WHERE hand_id = {hand_id} AND player_id = {player_id}")
                    hole_cards = cursor.fetchall()
                    for hole_card in hole_cards:
                        hole_card = hole_card[0] + ' ' + hole_card[1]
                    
                    # print(f"Hand ID: {hand_id}, Pot size: {formatted_pot_amount}, Community cards: '{board_cards_str}', Winner: {player_id}, Winning hand: '{hole_card}'")
                
                    # Insert collected pot into hand_summary table
                    insert_collected_query = "INSERT INTO hand_summary (hand_id, pot_size, community_cards, winner_id, winning_hand) VALUES (%s, %s, %s, %s, %s)"
                    cursor.execute(insert_collected_query, (hand_id, formatted_pot_amount, board_cards_str, player_id, hole_card))
                    cnx.commit()


                if '*** SUMMARY ***' in line:
                    game_phase = 'summary'
                    # print(line)
                    continue
                elif '*** RIVER ***' in line:
                    river_cards = re.search(r'\[([2-9TJQKA][cdhs] [2-9TJQKA][cdhs] [2-9TJQKA][cdhs])\] \[([2-9TJQKA][cdhs])\] \[([2-9TJQKA][cdhs])\]', hand)
                    if river_cards:
                        board_cards = river_cards.group(1).split() + [river_cards.group(2)] + [river_cards.group(3)]
                        # print(board_cards)
                    game_phase = 'river'
                    # print(line)
                    continue
                            
            
            # river actions
            elif game_phase == 'river':
                # print(line)
                # print(game_phase)

                # fold hands
                river_fold_match = re.match(r'(.+?): folds', line)
                if river_fold_match:
                    player_name = river_fold_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: river, Action Type: fold, Action Amount: NULL")
               
                    # Insert fold action into actions table
                    insert_fold_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'river', {player_id}, 'fold', NULL)"
                    cursor.execute(insert_fold_query)
                    cnx.commit()
 
 
                # raise hands
                river_raise_match = re.match(r'(.+?): raises (\d+) to (\d+)', line)
                if river_raise_match:
                    player_name = river_raise_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: river, Action Type: raise, Action Amount: {river_raise_match.group(3)}")
                
                    # Insert raise action into actions table
                    insert_raise_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'river', {player_id}, 'raise', {river_raise_match.group(3)})"
                    cursor.execute(insert_raise_query)
                    cnx.commit()
                
                
                # call the raises hands
                river_call_match = re.match(r'(.+?): calls (\d+)', line)
                if river_call_match:
                    player_name = river_call_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: river, Action Type: call, Action Amount: {river_call_match.group(2)}")

                    # Insert call action into actions table
                    insert_call_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'river', {player_id}, 'call', {river_call_match.group(2)})"
                    cursor.execute(insert_call_query)
                    cnx.commit()


                # the bet hands
                river_bet_match = re.match(r'(.+?): bets (\d+)', line)
                if river_bet_match:
                    player_name = river_bet_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: river, Action Type: bet, Action Amount: {river_bet_match.group(2)}")

                    # Insert bet action into actions table
                    insert_bet_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'river', {player_id}, 'bet', {river_bet_match.group(2)})"
                    cursor.execute(insert_bet_query)
                    cnx.commit()
                    

                # the check hands
                river_check_match = re.match(r'(.+?): checks', line)
                if river_check_match:
                    player_name = river_check_match.group(1)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: river, Action Type: check, Action Amount: NULL")

                    # Insert check action into actions table
                    insert_check_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'river', {player_id}, 'check', NULL)"
                    cursor.execute(insert_check_query)
                    cnx.commit()
                
                
                # the uncalled hands
                uncalled_bet_match = re.search(r'Uncalled bet \((\d+)\) returned to (.+)', line)
                if uncalled_bet_match:
                    returned_amount = int(uncalled_bet_match.group(1))
                    player_name = uncalled_bet_match.group(2)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: river, Action Type: uncalled_bet, Action Amount: {returned_amount}")
                    
                    # Insert uncalled bet returned action into actions table
                    insert_returned_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'river', {player_id}, 'uncalled_bet_returned', {returned_amount})"
                    cursor.execute(insert_returned_query)
                    cnx.commit()
                
                
                # for the hand_summanry table now, for if there is a winner before the showdown
                board_cards_river = board_cards
                board_cards_str = ', '.join(board_cards_river)
                collected_amount = re.search(r'(.+?) collected (\d+\.\d+) from pot', line)
                if collected_amount:
                    player_name = collected_amount.group(1)
                    pot_amount = float(collected_amount.group(2))
                    formatted_pot_amount = f"{pot_amount:.2f}"
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                        
                    # cursor.execute(f"SELECT card1, card2 FROM hole_cards WHERE hand_id = {hand_id} AND player_id = {player_id}")
                    hole_cards = cursor.fetchall()
                    for hole_card in hole_cards:
                        hole_card = hole_card[0] + ' ' + hole_card[1]
                    
                    # print(f"Hand ID: {hand_id}, Pot size: {formatted_pot_amount}, Community cards: '{board_cards_river}', Winner: {player_id}, Winning hand: '{hole_card}'")
                
                    # Insert collected pot into hand_summary table
                    insert_collected_query = f"INSERT INTO hand_summary (hand_id, pot_size, community_cards, winner_id, winning_hand) VALUES ({hand_id}, {formatted_pot_amount}, '{board_cards_str}', {player_id}, '{hole_card}')"
                    cursor.execute(insert_collected_query)
                    cnx.commit()
                

                if '*** SUMMARY ***' in line:
                    game_phase = 'summary'
                    # print(line)
                    continue
                elif '*** SHOWDOWN ***' in line:
                    game_phase = 'showdown'
                    # print(line)
                    continue


            # showdown actions
            elif game_phase == 'showdown':
                # print(line)
                # print(game_phase)


                # showdown hands
                showdown_match = re.match(r'(.+?) collected (\d+\.\d+) from pot', line)
                if showdown_match:
                    player_name = showdown_match.group(1)
                    # print(player_name)
                    pot_amount = float(showdown_match.group(2))
                    formatted_pot_amount = f"{pot_amount:.2f}"
                    # print(formatted_pot_amount)
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
               
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: showdown, Action Type: win, Action Amount: {formatted_pot_amount}")
               
               
                    # Insert showdown action into actions table
                    insert_showdown_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'showdown', {player_id}, 'win', {formatted_pot_amount})"
                    cursor.execute(insert_showdown_query)
                    cnx.commit()
                
                
                if '*** SUMMARY ***' in line:
                    game_phase = 'summary'
                    # print(line)
                    continue
             

            # summary actions, adds info for showdown winners to hand_summary
            elif game_phase == 'summary':
                # print(line)
                # print(game_phase)
                
                # get pot size
                total_pot_match = re.search(r'Total pot (\d+)', line)
                if total_pot_match:
                    pot_amount = float(total_pot_match.group(1))
                    formatted_pot_amount = f"{pot_amount:.2f}"
                    # print(f"Pot Amount: {formatted_pot_amount}")
                
                # get community cards
                community_cards = re.search(r'Board \[(.*?)\]', hand)
                if community_cards:
                    board_cards = community_cards.group(1).split()
                    community_cards_str = ', '.join(board_cards)
                else:
                    community_cards_str = ""
                
                winner_match = re.search(r'Seat (\d+): (.+?) showed \[(..) (..)\] and won \((\d+\.\d+)\)', line)
                if winner_match:
                    winning_hand = f"{winner_match.group(3)} {winner_match.group(4)}"
                    pot_amount = float(winner_match.group(5))
                    formatted_pot_amount = f"{pot_amount:.2f}"
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
                    
                    # print(f"Hand ID: {hand_id}, Pot size: {formatted_pot_amount}, Community cards: '{board_cards}', Winner: {winner_id}, Winning hand: '{winning_hand}'")
                
                    # Insert showdown summary into hands_summary table, only prints seat number, fix this
                    insert_showdown_query = f"INSERT INTO hand_summary (hand_id, pot_size, community_cards, winner_id, winning_hand) VALUES ({hand_id}, {formatted_pot_amount}, '({community_cards_str})', {player_id}, '{winning_hand}')"
                    cursor.execute(insert_showdown_query)
                    cnx.commit()

 
 
        # print('test to see where printed')
    
    
    # For if get an error as traversing through hands
    except Exception as e:
        print(f"Error processing hand: {hand[:100]}")  # Prints the first 100 characters of the hand for context
        raise e

# Commit and close connection
cnx.commit()
cursor.close()
cnx.close()
