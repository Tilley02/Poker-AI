CREATE TABLE hand_summary (
    hand_id INT,
    pot_size DECIMAL(10, 2),
    community_cards VARCHAR(255),
    winner_id INT,  -- Foreign key to player_id in the players table
    winning_hand VARCHAR(50),
    FOREIGN KEY (hand_id) REFERENCES hands(hand_id),
    FOREIGN KEY (winner_id) REFERENCES players(player_id)
);
