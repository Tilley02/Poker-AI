CREATE TABLE flop_table (
    hand_id INT,
    flop1 CHAR(2),
    flop2 CHAR(2),
    flop3 CHAR(2),
    FOREIGN KEY (hand_id) REFERENCES Hands(hand_id)
);

-- info on the flop