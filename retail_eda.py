import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from db_engine import get_engine

# load the data from postgres

engine = get_engine()
query = "SELECT * FROM retail_sales_data"
df = pd.read_sql(query, engine)
print(df.head())
print(df.shape)

# Data formatting
df["sale_date"] = pd.to_datetime(df["sale_date"])

# overall daily revenue trend

daily_sales = df.groupby("sale_date")["revenue"].sum().reset_index()

plt.figure(figsize=(12, 5))
sns.lineplot(data=daily_sales, x="sale_date", y="revenue")
plt.title("Daily Total Revenue Trend")
plt.xlabel("Date")
plt.ylabel("Revenue")
plt.show()

# Monthly seasonlity

df["month"] = df["sale_date"].dt.month
monthly_sales = df.groupby("month")["revenue"].sum().reset_index()

plt.figure(figsize=(10, 5))
sns.barplot(data=monthly_sales, x="month", y="revenue")
plt.title("Monthly Revenue Seasonality")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.show()

# -----------------------------
# 3️⃣ Store type comparison
# -----------------------------

store_type_sales = df.groupby("store_type")["revenue"].sum().reset_index()

plt.figure(figsize=(8, 5))
sns.barplot(data=store_type_sales, x="store_type", y="revenue")
plt.title("Revenue by Store Type")
plt.xlabel("Store Type")
plt.ylabel("Revenue")
plt.show()

# -----------------------------
# 4️⃣ Promotion impact
# -----------------------------

promo_sales = df.groupby("promotion")["revenue"].mean().reset_index()

plt.figure(figsize=(6, 5))
sns.barplot(data=promo_sales, x="promotion", y="revenue")
plt.title("Average Revenue: Promotion vs No Promotion")
plt.xlabel("Promotion")
plt.ylabel("Average Revenue")
plt.show()

avg_store_revenue_df = (
    df.groupby("store_type")["revenue"]
    .mean()
    .reset_index()
)

plt.figure(figsize=(8,5))
sns.barplot(data=avg_store_revenue_df, x="store_type", y="revenue")
plt.title("Average Revenue per Store Type")
plt.xlabel("Store Type")
plt.ylabel("Average Revenue")
plt.show()

