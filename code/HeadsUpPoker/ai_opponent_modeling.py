# need to try get hand_strength working, will start ai model setup for now

import sqlalchemy
import numpy as np
import pandas as pd # for the visualization
import seaborn as sns # for the visualization

# need to check about these
from sklearn.ensemble import RandomForestClassifier # for the machine learning model
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


# Get features from the table, is it a bad idea to use all the features? (doesn't help look for what want to train the ai on)
# y features are the result and also hand_strength or just hand_strength, see results for this
features = df.columns[0:19]
# print(features)
X = df[features]
y = df['result'] 

# print(X.head())
# print(y.head())

# split data
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=42)

# Initialize and train the model, tweaking the hyperparameters
model = RandomForestClassifier(n_estimators=10, random_state=42, max_depth=10)
model.fit(X_train, y_train)

# print('Accuracy on training set: {:.4f}'.format(model.score(X_train, y_train)))
# print('Accuracy on     test set: {:.4f}'.format(model.score(X_test, y_test)))

# Make predictions on the testing set
y_pred = model.predict(X_test)


# Evaluate the model, only works so well so far as dont have hand_strength working
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)



# Plan for ai model (only need to fix hand_strrength column in table then should be good):

# want to use a a supervised machine learning model (research more)

# Problem Definition:
# Clearly define the problem you are trying to solve with machine learning. Identify the type of problem (e.g., classification, regression, clustering) and the desired outcome.

# Data Collection:
# Gather relevant data that will be used to train and evaluate your model. Ensure that the data is clean, properly labeled, and representative of the problem you are addressing.

# Data Preprocessing:
# Prepare the data for training by handling missing values, encoding categorical variables, scaling features, and splitting the data into training and testing sets.

# Model Selection:
# Choose an appropriate machine learning algorithm based on the problem type, data characteristics, and computational resources available. Consider techniques such as decision trees, support vector machines, neural networks, etc.

# Model Training:
# Train the selected model using the training data. Adjust the model's parameters (hyperparameters) as needed to improve performance.


# To Do:

# Model Evaluation:
# Assess the performance of the trained model using the testing data. Evaluate metrics such as accuracy, precision, recall, F1-score, or mean squared error, depending on the problem type.

# Model Optimization:
# Fine-tune the model by adjusting hyperparameters, exploring different algorithms, or performing feature selection to optimize performance further.

# Deployment:
# Deploy the trained model into a production environment where it can be used to make predictions on new, unseen data. Ensure that the deployment process is seamless and scalable.

# Monitoring and Maintenance:
# Continuously monitor the performance of the deployed model and retrain it periodically with new data to maintain accuracy and reliability. Address any issues or drift in model performance as they arise.

# Iterative Improvement:
# Iterate on the entire process by incorporating feedback from users, updating the model with new features or data, and exploring advanced techniques to enhance performance continually.



# input layer: amount of nodes = amount of features from dataset (need to join tables to get the features)
# hidden layers: 2 hidden layers with 100 nodes each (should be enough for now)
# output layer: 1 node for the action taken by the player (to be decided)
# activation function: relu for hidden layers, sigmoid for output layer (used before)
# loss function: huber loss (can also use MAE, check out both these)
# optimization algorithm: Adam optimizer
# hyperparameters: learning rate = 0.001, batch size = 32, epochs = 100, nodes in hidden layers = 100
# training process: train the model using the input-output pairs, visualize the loss to monitor the training process
