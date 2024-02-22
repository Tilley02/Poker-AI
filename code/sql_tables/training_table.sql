CREATE TABLE GameData (
    S1 INT,
    C1 Int,
    S2 Int,
    C2 Int,
    S3 Int,
    C3 Int,
    S4 Int,
    C4 Int,
    S5 Int,
    C5 Int,
    S6 Int,
    C6 Int,
    S7 Int,
    C7 Int,
    percentage_of_total_chips_hand FLOAT,
    percentage_of_hand_bet_pot FLOAT,
    percentage_of_total_chips_in_pot FLOAT,
    current_stage INT, -- 0 = pre-flop, 1 = flop, 2 = turn, 3 = river
    move INT, -- 0 = fold, 1 = check, 2 = call, 3 = bet, 4 = raise
    player_hand_ranking INT, -- 1 = high card, 2 = pair, 3 = two pair, 4 = three of a kind, 5 = straight, 6 = flush, 7 = full house, 8 = four of a kind, 9 = straight flush, 10 = royal flush
    result INT -- 0 = loss, 1 = win
);

-- all info to be converted to numerical values for training