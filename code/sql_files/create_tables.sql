-- info one players
CREATE TABLE players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(255) NOT NULL,
    user_name VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255),
    street_address VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    postal_code VARCHAR(20),
	balance DECIMAL(10, 2) NOT NULL,
    total_winnings DECIMAL(10, 2) DEFAULT 0.00,
    games_played INT DEFAULT 0,
    games_won INT DEFAULT 0,
    games_lost INT DEFAULT 0,
    win_rate DECIMAL (5, 2),
    join_date DATE DEFAULT (CURRENT_DATE) /* when player first join */
);

-- info on game data
CREATE TABLE game_data (
	date_played DATETIME DEFAULT CURRENT_TIMESTAMP,
    game_id INT AUTO_INCREMENT PRIMARY KEY,
    hand_id INT,
    player_id INT,
    ai_id INT,
    community_cards VARCHAR(50),
    ai_hand VARCHAR(30) DEFAULT NULL, -- default null if they fold we don't see their cards
    player_hand VARCHAR(30) DEFAULT NULL,
    player_final_balance DECIMAL(10, 2),
    ai_final_balance DECIMAL(10, 2),
    total_rounds INT,
    player_wins INT, -- hands won
    ai_wins INT,
    result ENUM('player_win', 'ai_win', 'draw'),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);

-- info on game rounds
CREATE TABLE game_rounds (
    round_id INT AUTO_INCREMENT PRIMARY KEY,
    game_id INT,
    round_number INT,
    player_hand VARCHAR(30),
    ai_hand VARCHAR(30),
    community_cards VARCHAR(50),
    round_winner ENUM('player', 'ai', 'draw'),
    FOREIGN KEY (game_id) REFERENCES game_data(game_id)
);

-- AI training data table
CREATE TABLE ai_training_data (
    training_id INT AUTO_INCREMENT PRIMARY KEY,
    game_scenario VARCHAR(255),
    ai_decision VARCHAR(255),
    outcome ENUM('win', 'lose', 'draw')
);
