import sqlalchemy
import pandas as pd
from sklearn.ensemble import RandomForestClassifier # for the machine learning model
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
# print(current_dir)
parent_dir = os.path.dirname(current_dir)
# print(parent_dir)
dataset_dir = os.path.join(parent_dir, 'sql_files', 'poker_dataset')
# print(dataset_dir)
sys.path.append(parent_dir)

# connect to database
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

df = pd.read_sql(query, engine)
# print(df.head())
engine.dispose()

# Getting input and output layers
features = df.columns[0:19]
features_subset = df.columns[14:19] # yields the best results, this doesn't use community cards or dealt cards, to be decided when hand_rank is working
# X = df[features]
X = df[features_subset] # input layers
y = df['result'] # output layer

# print(X.head())
# print(y.head())


# split data
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=42)

# rf = RandomForestClassifier()

# hyperperameters for randomised search
# param_dist = {
#     'n_estimators': [10, 50, 100, 200],
#     'max_depth': [None, 5, 10, 20],
#     'min_samples_split': [2, 5, 10],
#     'min_samples_leaf': [1, 2, 4],
#     'bootstrap': [True, False]
# }

# finds best hyperparameters
# rf_random = RandomizedSearchCV(estimator=rf, param_distributions=param_dist, n_iter=100, cv=3, verbose=2,
#                                random_state=42, n_jobs=-1)
# rf_random.fit(X_train, y_train)
# best_params = rf_random.best_params_
# print(best_params)


# Initialize and train the model, tweaking the hyperparameters
model = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=5, min_samples_split=10, min_samples_leaf=1, bootstrap=True)
model.fit(X_train, y_train)

# print('Accuracy on training set: {:.4f}'.format(model.score(X_train, y_train)))
# print('Accuracy on     test set: {:.4f}'.format(model.score(X_test, y_test)))

# Make predictions on the testing set
y_pred = model.predict(X_test)



# Evaluate the model, only works so well so far as dont have hand_strength working

# model evaluation
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Print evaluation metrics
print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:\n", conf_matrix)



# need to read in  data from the player_action.txt file in the poker dataset folder
#  how to do that, need to call the table every time? getting last row of table?

file_path = os.path.join(dataset_dir, 'player_action.txt')
with open(file_path, 'r') as file:
    data = file.read().replace('\n', '')
    print(data)


# how to implement the ai model into the game


# ai will also not know players dealt cards when in the game so need to figure out how to implement that
