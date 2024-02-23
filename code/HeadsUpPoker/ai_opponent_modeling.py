import sqlalchemy
import pandas as pd
from sklearn.ensemble import RandomForestClassifier # for the machine learning model
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

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
features_subset2 = df.columns[14:19] # yields the best results, this doesn't use community cards or dealt cards, to be decided when hand_rank is working
# X = df[features]
X = df[features_subset2] # input layers
y = df['result'] # output layer

# print(X.head())
# print(y.head())


# split data
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=42)

# Initialize and train the model, tweaking the hyperparameters
model = RandomForestClassifier(n_estimators=10, random_state=42, max_depth=12)
model.fit(X_train, y_train)

# print('Accuracy on training set: {:.4f}'.format(model.score(X_train, y_train)))
# print('Accuracy on     test set: {:.4f}'.format(model.score(X_test, y_test)))

# Make predictions on the testing set
y_pred = model.predict(X_test)


# Evaluate the model, only works so well so far as dont have hand_strength working
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)



# Plan for ai model (only need to fix hand_strrength column in table then should be good):

# To Do:

# Model Evaluation:
# Assess the performance of the trained model using the testing data. Evaluate metrics such as accuracy, precision, recall, F1-score, or mean squared error, depending on the problem type.

# Model Optimization:
# Fine-tune the model by adjusting hyperparameters, exploring different algorithms, or performing feature selection to optimize performance further.
