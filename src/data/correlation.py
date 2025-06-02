#correlation.py

import pandas as pd

# Load features and target
X = pd.read_csv("data/processed_data/X_train_scaled.csv")
y = pd.read_csv("data/processed_data/y_train.csv").squeeze()  # makes y a Series

# Combine into one DataFrame
df = pd.concat([X, y.rename("target")], axis=1)

# Compute Pearson correlation matrix
corr_matrix = df.corr()

print(corr_matrix)