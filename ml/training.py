"""
We will use this file to train our model.
"""

import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, roc_auc_score
import pandas as pd

# Load the data
def load_data():
    """
    Load the data from the output.csv file.
    """
    data = pd.read_csv("output.csv")
    data = data[data["Delta"] != "Delta"]
    data["Blinking"] = data["Blinking"].map({"EYES_OPEN": 0, "BOTH_EYES_CLOSED": 1})
    data = data.astype(float)
    return data

def preprocess_data(data):
    """
    Preprocess the data by removing any rows with missing values.
    """
    data = data.dropna()
    return data

def train_model(data):
    """
    Train the model using the random forest classifier.
    """
    X = data.drop("Blinking", axis=1)
    y = data["Blinking"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model1 = RandomForestClassifier()
    model = model1
    model.fit(X_train, y_train)
    return model

def evaluate_model(model, data):
    """
    Evaluate the model using accuracy, precision, recall, f1 score, confusion matrix, and roc auc score.
    """
    X = data.drop("Blinking", axis=1)
    y = data["Blinking"]
    y_pred = model.predict(X)
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred)
    recall = recall_score(y, y_pred)
    f1 = f1_score(y, y_pred)
    confusion = confusion_matrix(y, y_pred)
    roc_auc = roc_auc_score(y, y_pred)
    return accuracy, precision, recall, f1, confusion, roc_auc

def save_model(model):
    with open("model.pkl", "wb") as file:
        pickle.dump(model, file)

data = load_data()
data = preprocess_data(data)
model = train_model(data)

accuracy, precision, recall, f1, confusion, roc_auc = evaluate_model(model, data)

print("Accuracy:", accuracy)
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
print("Confusion Matrix:", confusion)
print("ROC AUC Score:", roc_auc)

save_model(model)