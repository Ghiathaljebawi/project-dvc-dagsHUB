# gridsearch.py
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
import pickle
import os

os.makedirs("models/initial_model", exist_ok=True)

X_train = pd.read_csv("data/processed_data/scaled_data/X_train_scaled.csv")
y_train = pd.read_csv("data/processed_data/split_data/y_train.csv").values.ravel()

param_grid = {
    "n_estimators":      [50, 100, 150, 200, 250],
    "max_depth":         [None, 5, 10, 15, 20],
    "min_samples_split": [2, 3, 5, 10, 20]
}

model = RandomForestRegressor(random_state=122)
grid = GridSearchCV(model, param_grid, cv=5, n_jobs=-1)
grid.fit(X_train, y_train)

with open("models/initial_model/grid_initial_model.pkl", "wb") as f:
    pickle.dump(grid.best_params_, f)
