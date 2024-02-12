CREATE TABLE actions (
    action_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT, -- links player to a specific action
    game_phase ENUM('pre_flop', 'flop', 'turn', 'river'),
    action_detail TEXT, -- action done by the player
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
