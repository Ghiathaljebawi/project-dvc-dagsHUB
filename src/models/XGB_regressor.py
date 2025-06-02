# In src/models/training.py (replace existing model with XGBoost Regressor)

import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error, r2_score
import joblib

# Load scaled data
X_train = pd.read_csv("data/processed_data/X_train_scaled.csv")
y_train = pd.read_csv("data/processed_data/y_train.csv").values.ravel()
X_test = pd.read_csv("data/processed_data/X_test_scaled.csv")
y_test = pd.read_csv("data/processed_data/y_test.csv").values.ravel()

# Define parameter grid
param_grid = {
    "n_estimators": [35, 50, 75, 200],
    "max_depth": [2, 3, 4, 5, 6, 8],
    "learning_rate": [0.07, 0.08, 0.09, 0.1, 0.2, 0.3]
}

# Set up GridSearchCV
xgb = XGBRegressor(objective="reg:squarederror")
grid_search = GridSearchCV(
    estimator=xgb,
    param_grid=param_grid,
    cv=5,
    scoring="r2",
    n_jobs=-1
)


# Run grid search
grid_search.fit(X_train, y_train)
best_model = grid_search.best_estimator_

# Save model
# joblib.dump(model, "models/xgb_regressor.joblib")

# Evaluate
y_pred = best_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
r2 = r2_score(y_test, y_pred)
print({"BestParams": grid_search.best_params_, "MSE": mse, "RMSE": rmse, "R2": r2})