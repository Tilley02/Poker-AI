'''
    Virtual Environment Needed?
    Builds upon the base play style and introduces opponent profiling and modeling.
    Adapts the AI's strategy based on observed opponent behavior.
    Predicts opponents' likely actions using the learned profiles.
    Classification Algorithm?
    Decision Tree
'''
'''
Need to use Virtual Environment!!!

'Example Decision Tree Model Below "CA3109" - Predicitng House Prices in India'
'''

### DECISION TREE MODEL ###

# import necessary libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import sklearn
from sklearn.preprocessing import LabelEncoder
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier,plot_tree


# load in data using pandas and trim to relevant features
data = pd.read_csv('House_Rent_Dataset.csv', sep=',')
data = data[["BHK", "Rent", "Size", "Furnishing Status", "City", "Bathroom"]]

# convert furnishing status into integers
data["Furnishing Status"] = data["Furnishing Status"].replace({
    'Unfurnished': 0,
    'Semi-Furnished': 0.5,
    'Furnished': 1
})

# convert city into integers
data["City"] = data["City"].replace({
    "Kolkata" : 1,
    "Mumbai" : 2,
    "Bangalore" : 3,
    "Delhi" : 4,
    "Chennai" : 5,
    "Hyderabad" : 6
})


# seperate label from features
prediction = "Rent"

le = LabelEncoder()
data["BHK_n"]=le.fit_transform(data["BHK"])
data["Rent_n"]=le.fit_transform(data["Rent"])
data["Size_n"]=le.fit_transform(data["Size"])
data["Furnishing Status_n"]=le.fit_transform(data["Furnishing Status"])
data["Bathroom_n"]=le.fit_transform(data["Bathroom"])
data["City_n"]=le.fit_transform(data["City"])

x = np.array(data.drop([prediction], 1)) # features
y = np.array(data[prediction]) # labels

# split into testing and training data using sklearn
x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size = 0.1)

# create model
model = tree.DecisionTreeClassifier()

# train model
model.fit(x_train, y_train)

plt.figure(figsize=(120,80))
plot_tree(model,filled=True,feature_names=data.columns)
plt.show()

# record model accuracy by using test values
accuracy = model.score(x_test, y_test)
print('Accuracy: ', accuracy * 100, '%')
