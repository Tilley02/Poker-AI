# Tests the AI on the testing data, after it has been trained

import joblib
import pandas as pd
import sqlalchemy
from sklearn.metrics import accuracy_score, precision_score

# load in trained model
model = joblib.load('trained_model.pkl')


# connect to database
engine = sqlalchemy.create_engine('mysql+mysqlconnector://root:12345678@localhost/poker_ai_db')


query = """
SELECT S1, C1, S2, C2, S3, C3, S4, C4, S5, C5, S6, C6, S7, C7, 
       percentage_of_total_chips_hand, percentage_of_hand_bet_pot, percentage_of_total_chips_in_pot,
       current_stage, move, player_hand_ranking, result
FROM GameData
"""

# load in data (testing data)
df = pd.read_sql(query, engine)
engine.dispose()

features = df.columns[0:20]
X_test = df[features]
y_test = df['result']



y_pred = model.predict(X_test)

# evaluation
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)

print('Accuracy:', accuracy)
print('Precision:', precision)
