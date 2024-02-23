import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from HeadsUpPoker.determine_hand import determine_hand

def determine_hand_rank_sql(rank_keys, suit_keys):
    
    suit_mapping_sql = {'1': 'h', '2': 's', '3': 'd', '4': 'c'}
    rank_mapping_sql = {'1': '1', '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                    '7': 7, '8': 8, '9': 9, '10': 10, '11': 11, '12': 12,
                    '13': 13}
    
    suit_keys = [str(suit) for suit in suit_keys]
    rank_keys = [str(rank) for rank in rank_keys]

    # create dictionary of sql format using given cards
    cards_sql = []
    for rank, suit in zip(rank_keys, suit_keys):
        if rank == '0' or 'suit' == '0':
            cards_sql.append({'suit': 100, 'rank': 100}) # 100 is a placeholder for this for now, need to change to appropriate value
                                                         # be able to handle the 0 value
        else:
            cards_sql.append({'suit': suit_mapping_sql[suit], 'rank': rank_mapping_sql[rank]})

    pocket_sql = cards_sql[0:2]
    community_sql = cards_sql[2:7]

    rank_sql = determine_hand(pocket_sql, community_sql)
    
    return rank_sql[0]
