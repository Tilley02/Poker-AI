import re

def insert_hole_cards(hand, hand_id, cursor, cnx, rows_per_hand):
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
        insert_game_query = f"INSERT INTO hole_cards (hand_id, player_id, card1, card2) VALUES ({hand_id}, {player_id}, '{card1}', '{card2}')"
        cursor.execute(insert_game_query)
        cnx.commit()

        rows_per_hand += 1
