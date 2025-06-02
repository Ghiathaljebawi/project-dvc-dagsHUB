# splitting.py
import pandas as pd
from sklearn.model_selection import train_test_split
import os

os.makedirs("data/processed_data/split_data", exist_ok=True)

df = pd.read_csv("data/raw_data/raw.csv")
X = df.drop(["date","silica_concentrate"], axis=1)
y = df["silica_concentrate"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.23, random_state=42
)

X_train.to_csv("data/processed_data/split_data/X_train.csv", index=False)
X_test.to_csv("data/processed_data/split_data/X_test.csv", index=False)
y_train.to_csv("data/processed_data/split_data/y_train.csv", index=False)
y_test.to_csv("data/processed_data/split_data/y_test.csv", index=False)
