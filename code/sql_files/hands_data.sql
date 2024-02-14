CREATE TABLE hands (
    hand_id INT AUTO_INCREMENT PRIMARY KEY,
    hand_number INT,
    game_type VARCHAR(50), -- Texas Hold'em
    table_name VARCHAR(50), -- Pluribus
    max_players INT, -- Is 6 but want to have it only for two
    blind_small INT,
    blind_big INT
);

-- info on each poker hand