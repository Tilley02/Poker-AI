# Gets some hand info from hands and inserts into hands_data table

import re

def insert_hand_data(hand, hand_id, cursor, cnx):
    table_name = re.search(r"Table '(.+)'", hand).group(1)
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
            elif blind_type == "big blind":
                blind_big = player_name
                big_blind_amount = blind_amount

    player_name = button_player.group(2)
    cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
    player_ids = cursor.fetchall()
    for player_id in player_ids:
        player_id = player_id[0]


    # print(f"Hand ID: {hand_id}, Table: {table_name}, Small Blind Player: {blind_small}, Small Blind Seat: 1, Small Blind Amount: {small_blind_amount}, Big Blind Player: {blind_big}, Big Blind Seat: 2, Big Blind Amount: {big_blind_amount}, Button Player: '{player_id}'")

    # inserting info into hands_data table, only need to do this once per file
    insert_game_query = f"INSERT INTO hands (table_name, small_blind_player, small_blind_seat, small_blind_amount, big_blind_player, big_blind_seat, big_blind_amount, button_player) VALUES ('{table_name}', '{blind_small}', 1, '{small_blind_amount}', '{blind_big}', 2, '{big_blind_amount}', {player_id})"
    cursor.execute(insert_game_query)
    cnx.commit()
