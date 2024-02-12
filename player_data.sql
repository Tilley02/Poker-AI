CREATE TABLE players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT,
    player_name VARCHAR(255),
    seat_num INT,
    starting_stack INT,
    final_stack INT,
    outcome ENUM('win', 'lose', 'draw'),
    hand_strength VARCHAR(255),
    FOREIGN KEY (game_id) REFERENCES games(game_id) -- links players to a specific game
);
