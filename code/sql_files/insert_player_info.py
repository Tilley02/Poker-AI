# Gets player info from hands and inserts into player_data table

import re

def insert_player_info(hand, cursor, cnx):
    seat_player_stack_matches = re.findall(r'Seat (\d+): (.+?) \((\d+) in chips\)', hand)

    # uncomment below for loop and the insertion lines to run
    for seat_num, player_name, starting_stack in seat_player_stack_matches:

        # inserting info into player_data table, only need to do this once per file
        insert_game_query = f"INSERT INTO players (player_name, seat_number, chips) VALUES ('{player_name}', {seat_num}, {starting_stack})"
        cursor.execute(insert_game_query)
        cnx.commit()

        # print(f"Seat: {seat_num}, Player: {player_name}, Starting Stack: {starting_stack}") # gets seat num, player, starting chips
