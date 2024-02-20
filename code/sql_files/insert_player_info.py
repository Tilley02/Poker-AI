import re

def insert_player_info(hand, cursor, cnx):
    seat_player_stack_matches = re.findall(r'Seat (\d+): (.+?) \((\d+) in chips\)', hand)
    
    # Get the maximum player_id from the table
    cursor.execute("SELECT MAX(player_id) FROM players")
    max_player_id = cursor.fetchone()[0]

    # checks if a max player id or not
    if max_player_id is None:
        next_player_id = 1
    else:
        next_player_id = max_player_id + 1
        # print(f"Next player ID: {next_player_id}")

    for seat_num, player_name, starting_stack in seat_player_stack_matches:
        cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
        existing_players = cursor.fetchall()
        existing_player = None

        for exisiting_player in existing_players:
            existing_player = exisiting_player[0]

        if existing_player is not None:
            continue # If the player already exists, skip to the next player
        else:
            # If the player doesn't exist, assign the next available player_id
            player_id = next_player_id
            next_player_id += 1
            
            # Inserting info into player_data table
            insert_game_query = f"INSERT INTO players (player_id, player_name, chips) VALUES ({player_id}, '{player_name}', {starting_stack})"
            cursor.execute(insert_game_query)
            cnx.commit()

            print(f"Player_ID: {player_id}, Player: {player_name}, Starting Stack: {starting_stack}") 

