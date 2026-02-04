import pandas as pd
from db_engine import get_engine

# -----------------------------
# Load data
# -----------------------------

engine = get_engine()
query = "SELECT * FROM retail_sales_data"
df = pd.read_sql(query, engine)

# -----------------------------
# Date handling
# -----------------------------

df["sale_date"] = pd.to_datetime(df["sale_date"])

# -----------------------------
# Time based features
# -----------------------------

df["day"] = df["sale_date"].dt.day
df["month"] = df["sale_date"].dt.month
df["year"] = df["sale_date"].dt.year
df["day_of_week"] = df["sale_date"].dt.dayofweek

# Weekend flag
df["is_weekend"] = df["day_of_week"].apply(lambda x: 1 if x >= 5 else 0)

# -----------------------------
# One hot encoding categorical
# -----------------------------

df = pd.get_dummies(
    df, columns=["store_type", "city", "product_category"], drop_first=True
)

# -----------------------------
# Final dataset preview
# -----------------------------

print(df.head())
print(df.shape)

# Save for modeling
df.to_csv("retail_features.csv", index=False)

print("\nFeature engineered dataset saved as retail_features.csv")
