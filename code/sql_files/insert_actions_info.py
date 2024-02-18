import re

def insert_actions(line, hand_id, cursor, cnx, game_phase):

    # fold hands
    player_fold = re.match(r'(.+?): folds', line)
    if player_fold:
        player_name = player_fold.group(1)
        cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
        player_ids = cursor.fetchall()
        for player_id in player_ids:
            player_id = player_id[0]

        print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: {game_phase}, Action Type: fold, Action Amount: NULL")

        # Insert fold action into actions table
        # insert_fold_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'pre_flop', {player_id}, 'fold', NULL)"
        # cursor.execute(insert_fold_query)
        # cnx.commit()


    # raise hands
    player_raise = re.match(r'(.+?): raises (\d+) to (\d+)', line)
    if player_raise:
        player_name = player_raise.group(1)
        cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
        player_ids = cursor.fetchall()
        for player_id in player_ids:
            player_id = player_id[0]
                    
        print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: {game_phase}, Action Type: raise, Action Amount: {player_raise.group(3)}")
                
        # Insert raise action into actions table
        # insert_raise_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'pre_flop', {player_id}, 'raise', {pre_flop_raise_match.group(3)})"
        # cursor.execute(insert_raise_query)
        # cnx.commit()


    # call the raises hands
    player_call = re.match(r'(.+?): calls (\d+)', line)
    if player_call:
        player_name = player_call.group(1)
        cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
        player_ids = cursor.fetchall()
        for player_id in player_ids:
            player_id = player_id[0]
                    
        print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: {game_phase}, Action Type: call, Action Amount: {player_call.group(2)}")

        # Insert call action into actions table
        # insert_call_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'pre_flop', {player_id}, 'call', {pre_flop_call_match.group(2)})"
        # cursor.execute(insert_call_query)
        # cnx.commit()
                
                
    # the uncalled hands
    uncalled_bet = re.search(r'Uncalled bet \((\d+)\) returned to (.+)', line)
    if uncalled_bet:
        returned_amount = int(uncalled_bet.group(1))
        player_name = uncalled_bet.group(2)
        cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
        player_ids = cursor.fetchall()
        for player_id in player_ids:
            player_id = player_id[0]

        print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: {game_phase}, Action Type: uncalled_bet, Action Amount: {returned_amount}")

        # Insert uncalled bet returned action into actions table
        # insert_returned_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'pre_flop', {player_id}, 'uncalled_bet_returned', {returned_amount})"
        # cursor.execute(insert_returned_query)
        # cnx.commit()
    
    # the bet hands
    player_bet = re.match(r'(.+?): bets (\d+)', line)
    if player_bet:
        player_name = player_bet.group(1)
        cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
        player_ids = cursor.fetchall()
        for player_id in player_ids:
            player_id = player_id[0]

        print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: {game_phase}, Action Type: bet, Action Amount: {player_bet.group(2)}")

        # Insert bet action into actions table
        # insert_bet_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'flop', {player_id}, 'bet', {flop_bet_match.group(2)})"
        # cursor.execute(insert_bet_query)
        # cnx.commit()
                    

    # the check hands
    player_check = re.match(r'(.+?): checks', line)
    if player_check:
        player_name = player_check.group(1)
        cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
        player_ids = cursor.fetchall()
        for player_id in player_ids:
            player_id = player_id[0]

        print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: {game_phase}, Action Type: check, Action Amount: NULL")

        # Insert check action into actions table
        # insert_check_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'flop', {player_id}, 'check', NULL)"
        # cursor.execute(insert_check_query)
        # cnx.commit()

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

        print(f"Hand ID: {hand_id}, Player: {player_name}, Player id: {player_id}, Game Phase: {game_phase}, Action Type: win, Action Amount: {formatted_pot_amount}")

        # Insert showdown action into actions table
        # insert_showdown_query = f"INSERT INTO actions (hand_id, game_phase, player_id, action_type, action_amount) VALUES ({hand_id}, 'showdown', {player_id}, 'win', {formatted_pot_amount})"
        # cursor.execute(insert_showdown_query)
        # cnx.commit()
