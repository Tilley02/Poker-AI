CREATE TABLE hands (
    hand_id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50), -- Pluribus
    blind_small INT, -- seat number for who was the small blind
    blind_big INT -- seat number for who was the big blind
    -- hand_number INT,
    -- game_type VARCHAR(50),
    -- max_players INT, -- Is 6 but want to have it only for two
);

-- info on each poker hand
-- removed hand_number, game_type, max_players