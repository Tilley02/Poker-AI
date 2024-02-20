# file to model the poker ai using pytorch
import torch # for the neural network
import torch.nn as nn
import torch.optim as optim # for the optimizer
import mysql.connector
import numpy as np
from scipy.special import huber # for the loss function (can also use MAE)
import matplotlib.pyplot as plt # for plotting the loss to visualize the training process

cnx = mysql.connector.connect(host="localhost",
                               user="root",
                               password="12345678",
                               database="poker_ai_db")
cursor = cnx.cursor()

# if cnx.is_connected():
#     print("Connected to the MySQL database.")
# else:
#     print("Not connected to the MySQL database.")


# query = """
# SELECT hc.hand_id, a.game_phase, a.action_type, a.action_amount, p.chips, hs.community_cards, hs.pot_size
# FROM hole_cards hc
# JOIN actions a ON hc.hand_id = a.hand_id
# JOIN players p ON hc.player_id = p.player_id
# JOIN hand_summary hs on hc.hand_id = hs.hand_id
# """

# want to have table formatted like this somewhat
query = """
SELECT a.hand_id, a.game_phase, a.player_id, a.action_type, a.action_amount, hs.community_cards, hs.pot_size, hs.winner_id, hs.winning_hand
FROM actions a
JOIN hand_summary hs ON a.hand_id = hs.hand_id
"""


# Execute SQL query and fetch all rows
cursor = cnx.cursor()
cursor.execute(query)
rows = cursor.fetchall()


# Process the data and generate input-output pairs
input_output_pairs = []
for row in rows:
    # Process each row and extract relevant information
    hand_id, game_phase, player_id, action_type, action_amount, community_cards, pot_size, winner_id, winning_hand = row
    # Encode the state of the game and the action taken by the player
    # Append the input-output pair to the list
    # input_output_pairs.append((state_encoding, action_encoding))
    # print(row)
    print(f"Hand ID: {hand_id}, Phase: {game_phase}, Player ID: {player_id}, Action: {action_type}, Amount: {action_amount}, Board Cards: {community_cards}, Pot: {pot_size}, Winner: {winner_id}, Hand: {winning_hand}")
    print('')

# Convert data to PyTorch tensors
# features = torch.tensor([pair[0] for pair in input_output_pairs], dtype=torch.float32)
# labels = torch.tensor([pair[1] for pair in input_output_pairs], dtype=torch.long)

# # Verify shapes of tensors
# print("Features shape:", features.shape)
# print("Labels shape:", labels.shape)


# Close the cursor and database connection
cursor.close()
cnx.close()



# Plan for ai model (need to finish formatting data first):

# want to use a simple feedforward neural network (research more)

# input layer: amount of nodes = amount of features from dataset (need to join tables to get the features)
# hidden layers: 2 hidden layers with 100 nodes each (should be enough for now)
# output layer: 1 node for the action taken by the player (to be decided)
# activation function: relu for hidden layers, sigmoid for output layer (used before)
# loss function: huber loss (can also use MAE, check out both these)
# optimization algorithm: Adam optimizer
# hyperparameters: learning rate = 0.001, batch size = 32, epochs = 100, nodes in hidden layers = 100
# training process: train the model using the input-output pairs, visualize the loss to monitor the training process
