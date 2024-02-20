import re

def hand_summary(line, hand_id, board_cards, cursor, cnx):
    collected_amount = re.search(r'(.+?) collected (\d+\.\d+) from pot', line)
    if collected_amount:
        player_name = collected_amount.group(1)
        pot_amount = int(float(collected_amount.group(2)))
        # formatted_pot_amount = f"{pot_amount:.2f}"
        cursor.execute(f"SELECT player_id FROM players WHERE player_name = '{player_name}'")
        player_ids = cursor.fetchall()
        for player_id in player_ids:
            player_id = player_id[0]

        # captures the hole cards of the winner
        cursor.execute(f"SELECT card1, card2 FROM hole_cards WHERE hand_id = {hand_id} AND player_id = {player_id}")
        hole_cards = cursor.fetchall()
        for hole_card in hole_cards:
            hole_card = hole_card[0] + ', ' + hole_card[1]

        # print(f"Hand ID: {hand_id}, Pot size: {pot_amount}, Community cards: '{board_cards}', Winner: {player_id}, Winning hand: '{hole_card}'")

        # Insert collected pot into hand_summary table
        insert_collected_query = f"INSERT INTO hand_summary (hand_id, pot_size, community_cards, winner_id, winning_hand) VALUES ({hand_id}, {pot_amount}, '{board_cards}', {player_id}, '{hole_card}')"
        cursor.execute(insert_collected_query)
        cnx.commit()
