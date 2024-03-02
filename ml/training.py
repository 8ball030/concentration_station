
"""
We will use this file to train our model.
"""

# we have a multi variate time series data.

# we will use the following features to train our model:
# 1. Delta
# 2. Theta
# 3. Alpha
# 4. Beta

# we will use the following labels to train our model:
# 1. Blinking

# we will use the following models to train our model:
# 1. Random Forest
# 2. KNN
# 3. SVM
# 4. Neural Network

# we will also use the latest in time series forecasting to train our model.

# we will use the following libraries to train our model:
# 1. numpy
# 2. pandas
# 3. matplotlib
# 4. seaborn
# 5. scikit-learn
# 6. keras
# 7. tensorflow

# we will use the following steps to train our model:
# 1. Load the data
# 2. Preprocess the data
# 3. Train the model
# 4. Evaluate the model

# we will use the following metrics to evaluate our model:
# 1. Accuracy
# 2. Precision
# 3. Recall
# 4. F1 Score
# 5. Confusion Matrix
# 6. ROC AUC Score

# we will use the following techniques to improve our model:
# 1. Hyperparameter Tuning
# 2. Cross Validation
# 3. Feature Selection
# 4. Feature Engineering
# 5. Ensemble Learning
# 6. Regularization
# 7. Dropout

# we will use the following techniques to visualize our model:
# 1. Line Plot
# 2. Scatter Plot
# 3. Bar Plot


# we will use the following techniques to save our model:
# 1. Pickle


import numpy as np
import pandas as pd

# Load the data
def load_data():
    data = pd.read_csv("output.csv")
    # we remove all the rows where the value is the same as the header
    data = data[data["Delta"] != "Delta"]
    # we convert the data to the right data type
    data["Blinking"] = data["Blinking"].map({"EYES_OPEN": 0, "BOTH_EYES_CLOSED": 1})
    data = data.astype(float)

    return data

# Preprocess the data
def preprocess_data(data):
    # we map the blinking column to 0 and 1

    data = data.dropna()
    return data

from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import VotingClassifier
from sklearn.model_selection import cross_val_score


# Train the model
def train_model(data):
    X = data.drop("Blinking", axis=1)
    y = data["Blinking"]
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model1 = RandomForestClassifier()
    model2 = KNeighborsClassifier()
    model3 = SVC()
    model4 = MLPClassifier(max_iter=500)

    model = model1
    model.fit(X_train, y_train)
    return model

# Evaluate the model
def evaluate_model(model, data):
    X = data.drop("Blinking", axis=1)
    y = data["Blinking"]
    from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred)
    recall = recall_score(y, y_pred)
    f1 = f1_score(y, y_pred)
    confusion = confusion_matrix(y, y_pred)
    roc_auc = roc_auc_score(y, y_pred)
    return accuracy, precision, recall, f1, confusion, roc_auc

# Save the model
def save_model(model):
    import pickle
    with open("model.pkl", "wb") as file:
        pickle.dump(model, file)

# Load the data
data = load_data()

# Preprocess the data
data = preprocess_data(data)

# Train the model
model = train_model(data)

# Evaluate the model
accuracy, precision, recall, f1, confusion, roc_auc = evaluate_model(model, data)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:", confusion)
print("ROC AUC Score:", roc_auc)

save_model(model)