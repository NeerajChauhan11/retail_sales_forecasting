import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

# Load data
df = pd.read_csv("retail_features.csv")

X = df.drop(columns=["revenue", "sale_date"])
y = df["revenue"]

# Time-based split
split_index = int(len(df) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]

# Train model
model = RandomForestRegressor(n_estimators=150, random_state=42)
model.fit(X_train, y_train)

# Predict
y_pred = model.predict(X_test)

# Plot
plt.figure(figsize=(12,5))
plt.plot(y_test.values[:200], label="Actual Revenue")
plt.plot(y_pred[:200], label="Predicted Revenue")
plt.title("Actual vs Predicted Revenue (Sample)")
plt.xlabel("Time Steps")
plt.ylabel("Revenue")
plt.legend()
plt.show()
