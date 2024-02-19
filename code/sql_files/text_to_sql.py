import re
import mysql.connector
from insert_player_info import insert_player_info
from insert_hand_data import insert_hand_data
from insert_hole_card_info import insert_hole_cards
from insert_actions_info import insert_actions
from insert_hand_summary_info import hand_summary

# connect to mysql
cnx = mysql.connector.connect(user='root', password='12345678',
                              host='localhost', database='poker_ai_db')
cursor = cnx.cursor()

# if cnx.is_connected():
#     print("Connected to the MySQL database.")
# else:
#     print("Not connected to the MySQL database.")

# Read file, going file by file, change for each file loading data in from
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

        # check for 4 folds in hand before flop, if 4 folds continue through rest of hand, else continue to next hand
        fold_count = 0
        for line in hand.split('\n'):
            if line.startswith('*** FLOP ***'):
                break
            if line == '*** SUMMARY ***':
                break
            if re.match(r'(.+?): folds', line):
                fold_count += 1
        
        # if less than 4 folds continue through rest of hand
        if fold_count < 4:
            continue

        

        # inserting info in player_data table, uncomment this first, run, then comment out again
        # insert_player_info(hand, cursor, cnx)


        hand_id += 1    # gets incremented by one each hand


        # add info to hands_data table, uncomment this second, run, then comment out again
        # insert_hand_data(hand, hand_id, cursor, cnx)



        # for hole_cards table insertion, so doesn't go over 80 (amount of hands per .txt file)
        if hand_id > hands_to_process:
            break


        # inserting info into hole_cards table, gets pre-flop cards, uncomment this third, run, then comment out again
        # insert_hole_cards(hand, hand_id, cursor, cnx, rows_per_hand)


        # # Check rows_per_hand divisible by 6
        if rows_per_hand % 6 == 0:
            rows_per_hand = 0


        # inserting info into actions table and hand_summary table, uncomment functions fourth, run, then comment out again
        game_phase = 'pre_flop' # sets game_phase to pre-flop, to start
        for line in hand.split('\n'):

            # starting with pre-flop actions
            if game_phase == 'pre_flop':

                # inserting info for the pre-flop actions first
                # insert_actions(line, hand_id, cursor, cnx, game_phase)


                # for the hand_summanry table now, for if there is a winner before the flop
                board_cards = []
                # hand_summary(line, hand_id, board_cards, cursor, cnx)


                # Check if summary phase reached first then flop phase
                if '*** SUMMARY ***' in line:
                    game_phase = 'summary'
                    continue
                elif '*** FLOP ***' in line:
                    flop_cards = re.search(r'\[([2-9TJQKA][cdhs] [2-9TJQKA][cdhs] [2-9TJQKA][cdhs])\]', hand)
                    if flop_cards:
                        board_cards = flop_cards.group(1).split()
                    game_phase = 'flop'
                    continue
                

            # flop actions
            elif game_phase == 'flop':

                # inserting info for the flop actions
                # insert_actions(line, hand_id, cursor, cnx, game_phase)


                # for the hand_summary table, for if there is a winner before the turn
                board_cards_flop = board_cards
                board_cards_str = ', '.join(board_cards_flop)
                # hand_summary(line, hand_id, board_cards_str, cursor, cnx)


                if '*** SUMMARY ***' in line:
                    game_phase = 'summary'
                    continue
                elif '*** TURN ***' in line:
                    turn_cards = re.search(r'\[([2-9TJQKA][cdhs] [2-9TJQKA][cdhs] [2-9TJQKA][cdhs])\] \[([2-9TJQKA][cdhs])\]', hand)
                    if turn_cards:
                        board_cards = turn_cards.group(1).split() + [turn_cards.group(2)]
                    game_phase = 'turn'
                    continue


            # turn actions
            elif game_phase == 'turn':

                # inserting info for the turn actions
                # insert_actions(line, hand_id, cursor, cnx, game_phase)


                # for the hand_summary table now, for if there is a winner before the river
                board_cards_turn = board_cards
                board_cards_str = ', '.join(board_cards_turn)
                # print(board_cards_str)
                # hand_summary(line, hand_id, board_cards_str, cursor, cnx)


                if '*** SUMMARY ***' in line:
                    game_phase = 'summary'
                    continue
                elif '*** RIVER ***' in line:
                    river_cards = re.search(r'\[([2-9TJQKA][cdhs] [2-9TJQKA][cdhs] [2-9TJQKA][cdhs])\] \[([2-9TJQKA][cdhs])\] \[([2-9TJQKA][cdhs])\]', hand)
                    if river_cards:
                        board_cards = river_cards.group(1).split() + [river_cards.group(2)] + [river_cards.group(3)]
                    game_phase = 'river'
                    continue
                            
            
            # river actions
            elif game_phase == 'river':

                # inserting info for the river actions
                # insert_actions(line, hand_id, cursor, cnx, game_phase)
                
                
                # for the hand_summanry table now, for if there is a winner before the showdown
                board_cards_river = board_cards
                board_cards_str = ', '.join(board_cards_river)
                # print("Board cards string:", board_cards_str)
                # hand_summary(line, hand_id, board_cards_str, cursor, cnx)
                

                if '*** SUMMARY ***' in line:
                    game_phase = 'summary'
                    continue
                elif '*** SHOWDOWN ***' in line:
                    game_phase = 'showdown'
                    continue


            # showdown actions
            elif game_phase == 'showdown':


                # showdown hands
                showdown_match = re.match(r'(.+?) collected (\d+\.\d+) from pot', line)
                if showdown_match:
                    player_name = showdown_match.group(1)
                    pot_amount = float(showdown_match.group(2))
                    formatted_pot_amount = f"{pot_amount:.2f}"
                    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
                    player_ids = cursor.fetchall()
                    for player_id in player_ids:
                        player_id = player_id[0]
               
                    
                    # print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: showdown, Action Type: win, Action Amount: {formatted_pot_amount}")
               
               
                    # Insert showdown action into actions table
                    # insert_showdown_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'showdown', {player_id}, 'win', {formatted_pot_amount})"
                    # cursor.execute(insert_showdown_query)
                    # cnx.commit()
                
                
                if '*** SUMMARY ***' in line:
                    game_phase = 'summary'
                    continue
             

            # summary actions, adds info for showdown winners to hand_summary
            elif game_phase == 'summary':
                
                # get pot size
                total_pot_match = re.search(r'Total pot (\d+)', line)
                if total_pot_match:
                    pot_amount = float(total_pot_match.group(1))
                    formatted_pot_amount = f"{pot_amount:.2f}"
                
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

                    # print(f"Hand ID: {hand_id}, Pot size: {formatted_pot_amount}, Community cards: '{board_cards}', Winner: {player_id}, Winning hand: '{winning_hand}'")
                
                    # Insert showdown summary into hands_summary table, only prints seat number, fix this
                    # insert_showdown_query = f"INSERT INTO hand_summary (hand_id, pot_size, community_cards, winner_id, winning_hand) VALUES ({hand_id}, {formatted_pot_amount}, '{community_cards_str}', {player_id}, '{winning_hand}')"
                    # cursor.execute(insert_showdown_query)
                    # cnx.commit()



        print('test to see where printed')

    # For if get an error as traversing through hands
    except Exception as e:
        print(f"Error processing hand: {hand[:100]}")  # Prints the first 100 characters of the hand for context
        raise e

cnx.commit()
cursor.close()
cnx.close()
