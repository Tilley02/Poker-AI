'''
All the information from the poker files has been converted to numeric values for the ai to be able to read i.e. a fold is 0, a call is 1, a raise is 2
and the suits and ranks of the cards are also converted to numeric values.

Its then passed to the model here, can uncomment print(df.head()) to see the data that is being passed to the model on line 62

it looks like this:
S1  C1  S2  C2  S3  C3  ...  percentage_of_hand_bet_pot  percentage_of_total_chips_in_pot  current_stage  move  player_hand_ranking  result
0   4   3   2   9   0   0  ...                      0.0050                          0.004583              0     0                    1       0
1   3   6   2   5   0   0  ...                      0.0100                          0.004583              0     0                    1       0
2   3   9   2  10   0   0  ...                      0.0000                          0.004583              0     0                    1       0
3   2   2   2  12   0   0  ...                      0.0000                          0.004583              0     0                    1       0
4   3   1   3  13   0   0  ...                      0.0125                          0.004583              0     2                    1       1

so in the ai_main.py file the gamestate dictionary is the only one that is read by the model, the rest of the variables are just placeholders for the model to work


and the output of the model is if it will fold, call or raise then by outputting 0, 1 or 2
'''



import os
import sys
import sqlalchemy
import pandas as pd
from sklearn.ensemble import RandomForestClassifier # for the machine learning model
from sklearn.model_selection import train_test_split, RandomizedSearchCV, cross_val_score
from sklearn.metrics import accuracy_score, precision_score
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

# gets path for poker hands dataset
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
dataset_dir = os.path.join(parent_dir, 'sql_files', 'poker_dataset')
sys.path.append(parent_dir)


# connect to database
engine = sqlalchemy.create_engine('mysql+mysqlconnector://root:12345678@localhost/poker_ai_db')


query = """
SELECT S1, C1, S2, C2, S3, C3, S4, C4, S5, C5, S6, C6, S7, C7, 
       percentage_of_total_chips_hand, percentage_of_hand_bet_pot, percentage_of_total_chips_in_pot,
       current_stage, move, player_hand_ranking, result
FROM GameData
"""


df = pd.read_sql(query, engine)
engine.dispose()
# print(df.head())


# Getting input and output layers, testing different subsets
features = df.columns[0:20]
features_subset = ['S1', 'C1', 'S2', 'C2', 'S3', 'C3', 'S4', 'C4', 'S5', 'C5', 'S6', 'C6', 'S7', 'C7', 'percentage_of_total_chips_hand', 'percentage_of_hand_bet_pot', 'percentage_of_total_chips_in_pot', 'current_stage', 'player_hand_ranking']
features_subset_2 = ['S1', 'C1', 'S2', 'C2', 'S3', 'C3', 'S4', 'C4', 'S5', 'C5', 'S6', 'C6', 'S7', 'C7', 'percentage_of_total_chips_hand', 'percentage_of_total_chips_in_pot', 'current_stage', 'player_hand_ranking']
X = df[features_subset]
y = df['move']


X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=42)

# Initialize the model
rf = RandomForestClassifier()


# hyperperameters for randomised search
param_dist = {
    'n_estimators': [10, 50, 100, 200],
    'max_depth': [None, 5, 10, 20],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False]
}


# finds best hyperparameters
rf_random = RandomizedSearchCV(estimator=rf, param_distributions=param_dist, n_iter=100, cv=3, verbose=2, random_state=42, n_jobs=-1)
rf_random.fit(X_train, y_train)
best_params = rf_random.best_params_
# print(best_params)

# using best hyperparameters to train model
model = RandomForestClassifier(n_estimators=best_params['n_estimators'],
                               max_depth=best_params['max_depth'],
                               min_samples_split=best_params['min_samples_split'],
                               min_samples_leaf=best_params['min_samples_leaf'],
                               bootstrap=best_params['bootstrap'],
                               random_state=42)
model.fit(X_train, y_train)

# saves the trained model if it has not been saved already
if 'trained_model.pkl' in os.listdir():
    pass
else:
    joblib.dump(model, 'trained_model.pkl')


# Perform cross-validation i.e. splits dataset into multiple subsets, then trains and tests the model on each subset
cv_scores = cross_val_score(model, X, y, cv=5)


# Make predictions on the testing set
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average='weighted')


# Print evaluation metrics
print('Accuracy on training set: {:.4f}'.format(model.score(X_train, y_train))) # correct predictions made on the training set
print('Accuracy on     test set: {:.4f}'.format(model.score(X_test, y_test))) # correct predictions made on the test set
print("Cross-Validation Scores:", cv_scores) # how well the model generalizes to new data
print("Accuracy:", accuracy) # how many predictions were correct in the test set
print("Precision:", precision) # how many positive predictions were correct in the test set


# # Visualizing feature importance, shows what columns the AI is prioritizing
feature_importance = model.feature_importances_
feature_names = X.columns
plt.figure(figsize=(10, 6))
sns.barplot(x=feature_importance, y=feature_names)
plt.title('Feature Importance')
plt.xlabel('Importance')
plt.ylabel('Feature')

# uncomment to show diagram
plt.show()



# reads in player action file for live action hands from poker game to work on, working on this
file_path = os.path.join(dataset_dir, 'player_action.txt')
with open(file_path, 'r') as file:
    actions_info = file.read()

# can add actions to database tables then, and have it read by the model here

# clears file
# with open(file_path, 'w') as file:
#     file.write('')

# checks if file got emptied
file_size = os.path.getsize(file_path)
# if file_size == 0:
#     print("The file is empty.")
# else:
#     print("The file is not empty.")
