# need to try get hand_strength working, will start ai model setup for now

import sqlalchemy
import numpy as np
import pandas as pd # for the visualization
import seaborn as sns # for the visualization

# need to check about these
from sklearn.ensemble import RandomForestClassifier # for the model
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from tqdm.auto import tqdm # used for real time feeback, i.e. progress bar of loops
from sklearn.metrics import accuracy_score

# check this also
from scipy.special import huber # for the loss function (can also use MAE)

engine = sqlalchemy.create_engine('mysql+mysqlconnector://root:12345678@localhost/poker_ai_db')

# if engine.connect():
#     print("Connected to the MySQL database.")
# else:
#     print("Not connected to the MySQL database.")


query = """
SELECT S1, C1, S2, C2, S3, C3, S4, C4, S5, C5, S6, C6, S7, C7, 
       percentage_of_total_chips_hand, percentage_of_hand_bet_pot, percentage_of_total_chips_in_pot,
       current_stage, move, result, player_hand_ranking
FROM GameData
"""

# Get information from the table in MySQL
df = pd.read_sql(query, engine)
# print(df.head())
engine.dispose()



# Left off here thinking about using jupyter for visualization and need to also fix hand_strength code


# Get features from the table
features = df.columns[0:19]
# print(features)
X = df[features]
y = df['result'] 

# print(X.head())
# print(y.head())

X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=42)

# Initialize and train the model
model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(X_train, y_train)

# print('Accuracy on training set: {:.4f}'.format(model.score(X_train, y_train)))
# print('Accuracy on     test set: {:.4f}'.format(model.score(X_test, y_test)))

# Make predictions on the testing set
y_pred = model.predict(X_test)


# Evaluate the model, only works so well so far as dont have hand_strength working
accuracy = accuracy_score(y_test, y_pred)
# print("Accuracy:", accuracy)



# Plan for ai model (only need to fix hand_strrength column in table then should be good):

# want to use a a supervised machine learning model (research more)

# input layer: amount of nodes = amount of features from dataset (need to join tables to get the features)
# hidden layers: 2 hidden layers with 100 nodes each (should be enough for now)
# output layer: 1 node for the action taken by the player (to be decided)
# activation function: relu for hidden layers, sigmoid for output layer (used before)
# loss function: huber loss (can also use MAE, check out both these)
# optimization algorithm: Adam optimizer
# hyperparameters: learning rate = 0.001, batch size = 32, epochs = 100, nodes in hidden layers = 100
# training process: train the model using the input-output pairs, visualize the loss to monitor the training process
