CREATE TABLE hands (
    hand_id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50), -- Pluribus
    -- small blind player name
    small_blind_seat INT, -- seat number for who was the small blind
    -- small blind amount
    -- big blind player name
    big_blind_seat INT -- seat number for who was the big blind
    -- big blind amount
);

-- info on each poker hand
-- added small blind and big blind player name, and the amount of the small and big blind
 