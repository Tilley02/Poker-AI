import re
import mysql.connector

# Connect to MySQL database
cnx = mysql.connector.connect(user='root', password='12345678',
                              host='localhost', database='poker_ai_db')
cursor = cnx.cursor()

# Read file, going file by file
with open('/Users/conortilley/Desktop/CA326_project/holdem_dataset/pluribus_30.txt', 'r') as file:
    data = file.read()

# Splitting data
hands = re.split(r'PokerStars Hand #\d+:', data)[0:]

# Going through each hand
for hand in hands:
    try:
        # Taking data from hand
        table_name = re.search(r"Table '(.+)'", hand).group(1)  # Gets table name i.e. Plurburis
        player_name = re.search(r'Seat \d+: (.+)', hand).group(1)
        seat_num = re.search(r'Seat (\d+)', hand).group(1)
        starting_stack = re.search(r'(\d+) in chips', hand).group(1)  # Players starting chips
        small_blind_player = re.search(r'Seat \d+: (.+?) posts small blind', hand).group(1)
        big_blind_player = re.search(r'Seat \d+: (.+?) posts big blind', hand).group(1)
        hand_strength = re.search(r'Dealt to .+ \[(.+)\]', hand).group(1)  # Gets players dealt hand
        pre_flop_actions = re.search(r'\*\*\* HOLE CARDS \*\*\*(.+?)\*\*\* SUMMARY \*\*\*', hand, re.DOTALL).group(1).strip()  # Gets string of players dealt cards & actions before flop
        flop_actions = re.search(r'\*\*\* FLOP \*\*\*(.+?)\*\*\* SUMMARY \*\*\*', hand, re.DOTALL).group(1).strip()  # Gets string of flop cards & actions before the turn
        turn_actions = re.search(r'\*\*\* TURN \*\*\*(.+?)\*\*\* SUMMARY \*\*\*', hand, re.DOTALL).group(1).strip()  # Gets turn card & actions before river
        river_actions = re.search(r'\*\*\* RIVER \*\*\*(.+?)\*\*\* SHOWDOWN \*\*\*', hand, re.DOTALL).group(1).strip()  # Gets river card & actions before showdown
        outcome = re.search(r'and (won|lost)', hand).group(1) # not in every hand in the data, need to change
        final_hand_strength = re.search(r'Board \[(.+)\]', hand).group(1) # not in every hand in the data, need to change
        community_cards = re.search(r'Board \[.+?\] (.+)', hand)
        pot_size = re.search(r'Total pot (\d+)', hand).group(1)

        # Put game data in games table
        insert_game_query = f"INSERT INTO games (table_name, small_blind_player, big_blind_player, community_cards, pot_size) VALUES ('{table_name}', '{small_blind_player}', '{big_blind_player}', '{community_cards}', {pot_size})"
        cursor.execute(insert_game_query)
        game_id = cursor.lastrowid # lastrow of game table

        # Put player data in players table
        insert_player_query = f"INSERT INTO players (game_id, player_name, seat_num, starting_stack, final_stack, outcome, hand_strength) VALUES ({game_id}, '{player_name}', {seat_num}, {starting_stack}, {starting_stack}, '{outcome}', '{hand_strength}')"
        cursor.execute(insert_player_query)
        player_id = cursor.lastrowid # lastrow of player table

        # Put action data in actions table
        insert_action_query = f"INSERT INTO actions (player_id, game_phase, action_detail) VALUES ({player_id}, 'pre_flop', '{pre_flop_actions}')"
        cursor.execute(insert_action_query)
        insert_action_query = f"INSERT INTO actions (player_id, game_phase, action_detail) VALUES ({player_id}, 'flop', '{flop_actions}')"
        cursor.execute(insert_action_query)
        insert_action_query = f"INSERT INTO actions (player_id, game_phase, action_detail) VALUES ({player_id}, 'turn', '{turn_actions}')"
        cursor.execute(insert_action_query)
        insert_action_query = f"INSERT INTO actions (player_id, game_phase, action_detail) VALUES ({player_id}, 'river', '{river_actions}')"
        cursor.execute(insert_action_query)
    
    # For if get an error as traversing through hands
    except Exception as e:
        print(f"Error processing hand: {hand[:100]}")  # Prints the first 100 characters of the hand for context
        raise e

# Commit and close connection
cnx.commit()
cursor.close()
cnx.close()
