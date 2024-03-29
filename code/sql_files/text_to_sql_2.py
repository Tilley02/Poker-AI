import glob # for reading all files in a directory
import re
import mysql.connector
from convert_card import suit_rank, card_rank
from player_actions_info import Player_Game


# that will be used to add the columns that will be used to insert the data into the table
Columns = [
    'S1','C1','S2','C2','S3','C3','S4','C4','S5','C5','S6','C6','S7','C7',
    'percentage_of_total_chips_hand', # chips held by player
    'percentage_of_hand_bet_pot', # size of bet relative to their chips
    'percentage_of_total_chips_in_pot', # chips in pot
    'current_stage', # stage of game i.e. flop, turn, river
    'move', # last action of player
    'player_hand_ranking', # ranking of player hand in current game
    'result' # result of game for player 1 = win, 0 = loss
]


# connect to mysql
connection = mysql.connector.connect(user='root', 
                              password='12345678',
                              host='localhost', 
                              database='poker_ai_db')
cursor = connection.cursor()


def data_reader():
    games = []
    for data_path in glob.glob("poker_dataset/*.txt"):
        data_file = open(data_path, "r")

        game = []
        fold_count = 0
        is_valid_game = True
        
        # only added games that have more than 4 folds before the flop line
        for line in data_file:
            if re.match(r'(.+?): folds', line):
                fold_count += 1

            if '*** FLOP ***' in line:
                if fold_count < 4:
                    is_valid_game = False

            if 'PokerStars Hand' in line:
                if is_valid_game:
                    games.append(game)

                game = []
                fold_count = 0
                is_valid_game = True

            game.append(line)

    return games

def gather_players(game):
    players = []
    for line in game:

        if 'Seat' in line and 'button' not in line and 'won' not in line and 'lost' not in line:
            seat_player_stack_matches = re.match(r'Seat (\d+): (.+?) \((\d+) in chips\)', line, re.IGNORECASE)
            name = seat_player_stack_matches.group(2)
            chips = int(seat_player_stack_matches.group(3))
            players.append({'name':name, 'chips':chips})

        elif 'Player' in line and 'folds' in line: # skips lines showing players folding
            continue

    return players


def process_game(game):
    players = gather_players(game)
    total_chips = 0

    for player in players:
        total_chips += player['chips']
    
    for player in players:
        records = process_player(player, total_chips, game)
        insert_records(records, cursor)


def process_player(player, total_chips, game):
    pg = Player_Game(player, game, total_chips)
    records = pg.gather_full_game_data()

    return records

def insert_records(records, cursor):
    placeholders = ','.join(['%s'] * len(records[0]))
    columns = ','.join(Columns)
    query = f"INSERT INTO GameData ({columns}) VALUES ({placeholders})"
    for record in records:
        data = (
            record['S1'], record['C1'], record['S2'], record['C2'], record['S3'], record['C3'],
            record['S4'], record['C4'], record['S5'], record['C5'], record['S6'], record['C6'],
            record['S7'], record['C7'], record['percentage_of_total_chips_hand'],
            record['percentage_of_hand_bet_pot'], record['percentage_of_total_chips_in_pot'],
            record['current_stage'], record['move'], record['player_hand_ranking'], record['result']
        )
        cursor.execute(query, data)


if __name__ == "__main__":
    games = data_reader()
    games_len = len(games)
    current_game = 0
    try:
        for game in games:
            current_game += 1
            print(f'{current_game}/{games_len}') # shows what hand is being processed
            process_game(game)
            if current_game % 50 == 0:
                print("Saving")
                connection.commit()
    except KeyboardInterrupt:
        print("Insertion stopped")
    finally:
        connection.commit()

    cursor.close()
    connection.close()


# 1411 hands in tables, table overwrties itself if more added, this could conflict when adding more data from poker game to table


# for testing functions outputs
sample_game = [
    "PokerStars Hand #30006: Hold'em No Limit (50/100) - 2019/07/11 08:20:06 ET",
    "Table 'PokerStars Session 30' 6-max Seat #1 is the button",
    "Seat 1: Player1 (1000 in chips)",
    "Seat 2: Player2 (1500 in chips)",
    "Seat 3: Player3 (2000 in chips)",
    "Seat 4: Player4 (2500 in chips)",
    "Seat 5: Player5 (3000 in chips)",
    "Seat 6: Player6 (3500 in chips)",
    "Player1: posts small blind 10",
    "Player2: posts big blind 20",
    "*** HOLE CARDS ***",
    "Dealt to Player1 [As 7d]",
    "Dealt to Player2 [Tc 4d]",
    "Dealt to Player3 [3s 4h]",
    "Dealt to Player4 [Qc Jd]",
    "Dealt to Player5 [6c Ad]",
    "Dealt to Player6 [9c 7d]",
    "Player1: folds",
    "Player2: checks",
    "Player3: checks",
    "Player4: folds",
    "Player5: folds",
    "Player6: folds",
    "*** FLOP *** [9d 8s 2c]",
    "Player2: checks",
    "Player3: checks",
    "*** TURN *** [9d 8s 2c] [5c]",
    "Player2: checks",
    "Player3: checks",
    "*** RIVER *** [9d 8s 2c] [5c] [3d]",
    "Player2: checks",
    "Player3: checks",
    "*** SHOWDOWN ***"
    "Player3: shows [3c 4d]",
    "Player3 collected 140 from pot",
    "*** SUMMARY ***",
    "Total pot 140 | Rake 0",
    "Board [9d 8c 2c 5c 3d]",
    "Seat 2: Player2 showed [Tc 4d] and lost",
    "Seat 3: Player3 showed [3c 4d] and won (30)",  
]

# process_game(sample_game) # for testing
