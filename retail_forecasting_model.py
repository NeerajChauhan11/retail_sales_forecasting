import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.ensemble import RandomForestRegressor

# -----------------------------
# Load engineered data
# -----------------------------

df = pd.read_csv("retail_features.csv")

# -----------------------------
# Define features & target
# -----------------------------

X = df.drop(columns=["revenue", "sale_date"])
y = df["revenue"]

# -----------------------------
# Train-test split (time aware)
# -----------------------------

split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

# -----------------------------
# Train Random Forest model
# -----------------------------

model = RandomForestRegressor(n_estimators=150, random_state=42, n_jobs=-1)

model.fit(X_train, y_train)

# -----------------------------
# Predictions
# -----------------------------

y_pred = model.predict(X_test)

# -----------------------------
# Evaluation
# -----------------------------

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n📊 Forecasting Model Performance:")
print("MAE:", round(mae, 2))
print("R2 Score:", round(r2, 3))

# -----------------------------
# Sample future prediction
# -----------------------------

sample_input = X_test.iloc[0].values.reshape(1, -1)
future_prediction = model.predict(sample_input)

print("\n🔮 Sample Predicted Revenue:", round(future_prediction[0], 2))
print("Actual Revenue:", round(y_test.iloc[0], 2))
