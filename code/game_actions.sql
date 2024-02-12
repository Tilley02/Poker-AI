CREATE TABLE actions (
    action_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    game_phase ENUM('pre_flop', 'flop', 'turn', 'river'),
    action_detail TEXT,
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
