import pandas as pd
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error

# Load dataset
df = pd.read_csv("data/labels/dataset_labels.csv")

# Drop non-numeric columns
df = df.drop(columns=["file", "source_di"])

# Fill missing values
df = df.fillna(0)

# Split features / targets
X = df[["rms", "centroid", "zcr"]]

y = df.drop(columns=["rms", "centroid", "zcr"])

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = MultiOutputRegressor(
    lgb.LGBMRegressor(
        n_estimators=100,
        learning_rate=0.05,
        max_depth=6
    )
)

# Train
model.fit(X_train, y_train)

# Evaluate success
preds = model.predict(X_test)

mse = mean_squared_error(y_test, preds)
print(f"MSE: {mse}")

# Save model
import joblib
joblib.dump(model, "tone_model.pkl")
