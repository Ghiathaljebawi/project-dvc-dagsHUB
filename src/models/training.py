# training.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import pickle
import joblib
import os

os.makedirs("models/deployment_model", exist_ok=True)

X_train = pd.read_csv("data/processed_data/scaled_data/X_train_scaled.csv")
y_train = pd.read_csv("data/processed_data/split_data/y_train.csv").values.ravel()

with open("models/initial_model/grid_initial_model.pkl", "rb") as f:
    best_params = pickle.load(f)

model = RandomForestRegressor(**best_params, random_state=42)
model.fit(X_train, y_train)

joblib.dump(model, "models/deployment_model/deployment_trained_model.pkl")
