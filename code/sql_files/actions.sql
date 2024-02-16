-- info on each poker hand

CREATE TABLE actions (
    action_id INT AUTO_INCREMENT PRIMARY KEY,
    hand_id INT,
    game_phase VARCHAR(50), -- preflop, flop, turn, river, showdown
    player_id INT,
    action_type VARCHAR(50), -- bet, raise, call, fold
    action_amount INT, -- amount of money if any
    FOREIGN KEY (hand_id) REFERENCES Hands(hand_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id)
);
