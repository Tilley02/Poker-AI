import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from HeadsUpPoker.determine_hand import determine_hand


# Arguments taken as:
# rank_keys = ['3','7','8','9','10','11','12']
# suit_keys = ['1','2','2','3','4','1','2']

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
            cards_sql.append({'suit': '30', 'rank': '30'}) # need to see what to do for this, has to be an int value, the problem is 
                                                           # that when there are not community cards, the rank and suit keys are 0
                                                           # so need to find a work around for that, just put 30 for now   
        else:
            cards_sql.append({'suit': suit_mapping_sql[suit], 'rank': rank_mapping_sql[rank]})

    # print("Cards SQL:", cards_sql)
    
    
    # print("Suit keys:", suit_keys)
    # print("Rank keys:", rank_keys)
    # print("Suit mapping:", suit_mapping_sql)
    # print("Rank mapping:", rank_mapping_sql)

    pocket_sql = cards_sql[0:2]
    community_sql = cards_sql[2:7]
    
    
    # print("Pocket SQL:", pocket_sql)
    # print("Community SQL:", community_sql)
    
    rank_sql = determine_hand(pocket_sql, community_sql)
    
    return rank_sql[0]





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

result = determine_hand_rank_sql(rank_keys, suit_keys)
# print("Card Rank:", result)

