# file to model the poker ai using pytorch
import torch
import torch.nn as nn
import torch.optim as optim
import mysql.connector

cnx = mysql.connector.connect(host="localhost",
                               user="root",
                               password="12345678",
                               database="poker_ai_db")
cursor = cnx.cursor()

if cnx.is_connected():
    print("Connected to the MySQL database.")
else:
    print("Not connected to the MySQL database.")


query = """
SELECT hands.hand_id, hands.table_name, actions.player_id, actions.game_phase, actions.action_type, actions.action_amount
FROM hands
JOIN actions ON hands.hand_id = actions.hand_id
"""

cursor = cnx.cursor()
cursor.execute(query)

# Fetch all rows
rows = cursor.fetchall()

# Process the data and generate input-output pairs
input_output_pairs = []
for row in rows:
    # Process each row and extract relevant information
    hand_id, table_name, player_id, game_phase, action_type, action_amount = row
    if action_amount != None:
        action_amount = int(action_amount)
    # Encode the state of the game and the action taken by the player
    # Append the input-output pair to the list
    # input_output_pairs.append((state_encoding, action_encoding))
    print(row)

# Close the cursor and database connection
cursor.close()
cnx.close()


# want to use a neural network (policy network) using supervised learning

