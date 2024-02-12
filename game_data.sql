CREATE TABLE games (
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(255),
    community_cards VARCHAR(255),
    pot_size INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
