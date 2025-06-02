# evaluation.py
import pandas as pd
import joblib
from sklearn.metrics import mean_squared_error, r2_score
import json
import os

os.makedirs("metrics", exist_ok=True)
os.makedirs("data/prediction_data", exist_ok=True)

X_test = pd.read_csv("data/processed_data/scaled_data/X_test_scaled.csv")
y_test = pd.read_csv("data/processed_data/split_data/y_test.csv").values.ravel()

model = joblib.load("models/deployment_model/deployment_trained_model.pkl")
preds = model.predict(X_test)

pd.DataFrame(preds, columns=["prediction"]).to_csv(
    "data/prediction_data/predictions.csv", index=False)

mse = mean_squared_error(y_test, preds)
rmse = mse ** 0.5
r2 = r2_score(y_test, preds)

scores = {"MSE": mse, "RMSE": rmse, "R2": r2}
with open("metrics/scores.json", "w") as f:
    json.dump(scores, f)