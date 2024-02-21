# file to model the poker ai using pytorch, probably wont need all these imports

import torch # for the neural network
import torch.nn as nn
import torch.optim as optim # for the optimizer
import mysql.connector
import numpy as np
import scipy
import sklearn
import sys
import matplotlib
import matplotlib.pyplot as plt # for plotting the loss to visualize the training process
import seaborn as sns # for the visualization
import pandas as pd # for the visualization
import matplotlib.pyplot as plt # for the visualization
from itertools import islice # for the visualization
from types import SimpleNamespace
from packaging.version import Version
from scipy.special import huber # for the loss function (can also use MAE)

cnx = mysql.connector.connect(host="localhost",
                               user="root",
                               password="12345678",
                               database="poker_ai_db")
cursor = cnx.cursor()

# if cnx.is_connected():
#     print("Connected to the MySQL database.")
# else:
#     print("Not connected to the MySQL database.")

query = """
SELECT gd.S1, gd.C1, gd.S2, gd.C2, gd.S3, gd.C3, gd.S4, gd.C4, gd.S5, gd.C5, gd.S6, gd.C6, gd.S7, gd.C7, 
       gd.percentage_of_total_chips_hand, gd.percentage_of_hand_bet_pot, gd.percentage_of_total_chips_in_pot,
       gd.current_stage, gd.move, gd.result, gd.player_hand_ranking
FROM GameData gd
"""

# Execute SQL query and fetch all rows
cursor = cnx.cursor()
cursor.execute(query)
rows = cursor.fetchall()


# Left off here thinking about using jupyter for visualization and easier implementation of the model
# trying to load a scatterplot in, need to also fix hand_strength code



# Process the data and generate input-output pairs
input_output_pairs = []
for row in rows:
    # print(row)
    # print(len(rows) / 6)
    # Process each row and extract relevant information
    S1, C1, S2, C2, S3, C3, S4, C4, S5, C5, S6, C6, S7, C7, percentage_of_total_chips_hand, percentage_of_hand_bet_pot, percentage_of_total_chips_in_pot, current_stage, move, result, player_hand_ranking = row
    # Encode the state of the game and the action taken by the player
    # Append the input-output pair to the list
    # input_output_pairs.append((state_encoding, action_encoding))
    # print(row)
    # print('S1:', S1, 'C1:', C1, 'S2:', S2, 'C2:', C2, 'S3:', S3, 'C3:', C3, 'S4:', S4, 'C4:', C4, 'S5:', S5, 'C5:', C5, 'S6:', S6, 'C6:', C6, 'S7:', S7, 'C7:', C7, 'percentage_of_total_chips_hand:', percentage_of_total_chips_hand, 'percentage_of_hand_bet_pot:', percentage_of_hand_bet_pot, 'percentage_of_total_chips_in_pot:', percentage_of_total_chips_in_pot, 'current_stage:', current_stage, 'move:', move, 'result:', result, 'player_hand_ranking:', player_hand_ranking)
    # print('')
    # print(row)

# sns.scatterplot(data=rows, x="move", y="result")


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
