CREATE TABLE hands (
    hand_id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50), -- Pluribus
    small_blind_player VARCHAR(50),
    small_blind_seat INT, -- always seat one
    small_blind_amount INT,
    big_blind_player VARCHAR(50),
    big_blind_seat INT, -- always seat two
    big_blind_amount INT,
    button_player INT -- always seat 6
);

-- info on each poker hand
