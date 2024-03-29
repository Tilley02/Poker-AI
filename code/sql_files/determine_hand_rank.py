import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from HeadsUpPoker.determine_hand import determine_hand

# Arguments taken as:
# rank_keys = ['3','7','8','9','10','11','12']
# suit_keys = ['1','2','2','3','4','1','2']'

def determine_hand_rank(rank_keys, suit_keys):
    # Mapping them to my format
    suit_mapping = {'1': 'Hearts', '2': 'Spades', '3': 'Diamonds', '4': 'Clubs'}
    rank_mapping = {'1': '14', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6',
                    '7': '7', '8': '8', '9': '9', '10': '10', '11': '11',
                    '12': '12', '13': '13'}

    # Create dictionary of my format using given cards.
    cards = [{'suit': suit_mapping[suit], 'rank': rank_mapping[rank]} for suit, rank in zip(suit_keys, rank_keys)]

    pocket = cards [0:2]
    community = cards[2:7]
    rank = determine_hand(pocket, community)

    return rank[0]


# testing
rank_keys = ['3','7','8','9','10','11','12']
suit_keys = ['1','2','2','3','4','1','2']

# what cards_sql would look like
# cards_sql = [
#     {'S': 1, 'C': 3},  # 3 of hearts
#     {'S': 2, 'C': 7},  # 7 of spades
#     {'S': 2, 'C': 8},  # 8 of spades
#     {'S': 3, 'C': 9},  # 9 of diamonds
#     {'S': 4, 'C': 10}, # 10 of clubs
#     {'S': 1, 'C': 11}, # Jack of hearts
#     {'S': 2, 'C': 12}  # Queen of spades
# ]

result = determine_hand_rank(rank_keys, suit_keys)
print(result)
