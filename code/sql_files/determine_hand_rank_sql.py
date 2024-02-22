import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from HeadsUpPoker.determine_hand import determine_hand


# Arguments taken as:
# rank_keys = ['3','7','8','9','10','11','12']
# suit_keys = ['1','2','2','3','4','1','2']'

def determine_hand_rank_sql(rank_keys, suit_keys):

    # mapping to sql format
    suit_mapping_sql = {'h': 1, 's': 2, 'd': 3, 'c': 4}
    rank_mapping_sql = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
                        '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12,
                        'K': 13}
    
    # create dictionary of sql format using given cards
    cards_sql = [{'S': suit_mapping_sql[suit], 'C': rank_mapping_sql[rank]} for suit, rank in zip(suit_keys, rank_keys)]

    pocket_sql = cards_sql[0:2]
    community_sql = cards_sql[2:7]
    rank_sql = determine_hand(pocket_sql, community_sql)
    
    return rank_sql[0]
