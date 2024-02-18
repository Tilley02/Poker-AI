CREATE TABLE hole_cards (
    hand_id INT,
    player_id INT,
    card1 CHAR(2),
    card2 CHAR(2),
    FOREIGN KEY (hand_id) REFERENCES hands(hand_id),
    FOREIGN KEY (player_id) REFERENCES players(player_id)
);
