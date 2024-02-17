-- info on each poker hand

CREATE TABLE actions (
    action_id INT AUTO_INCREMENT PRIMARY KEY,
    hand_id INT,
    game_phase VARCHAR(50), -- preflop, flop, turn, river, showdown
    player_id INT,
    action_type VARCHAR(50), -- bet, raise, call, fold, check or win (for showdown)
    action_amount DECIMAL(10, 2), -- amount of money if any, for bet, raise, call or uncalled bet
    FOREIGN KEY (hand_id) REFERENCES hands(hand_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
