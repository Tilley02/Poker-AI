CREATE TABLE hands (
    hand_id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50), -- Pluribus
    small blind player VARCHAR(50),
    small_blind_seat INT, -- always seat one
    small blind amount INT,
    big blind player VARCHAR(50),
    big_blind_seat INT -- always seat two
    big blind amount INT
    button_player INT, -- always seat 6
);

-- info on each poker hand
