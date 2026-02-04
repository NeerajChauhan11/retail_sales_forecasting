import random
from datetime import datetime, timedelta
from db_engine import get_engine

# -------------------------
# DB engine
# -------------------------

engine = get_engine()

# -------------------------
# Date range
# -------------------------

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

# -------------------------
# Stores & products
# -------------------------

stores = [1, 2, 3, 4, 5]

categories = ["Electronics", "Clothing", "Groceries", "Furniture", "Toys"]

# -------------------------
# City classification
# -------------------------

metro_cities = ["Delhi", "Mumbai", "Bangalore", "Chennai", "Hyderabad"]

tier2_cities = ["Pune", "Jaipur", "Indore", "Lucknow", "Coimbatore", "Chandigarh"]

town_cities = [
    "Alwar",
    "Sitapur",
    "Gaya",
    "Ratlam",
    "Siliguri",
    "Solan",
    "Shimla",
    "Una",
    "Mandi",
    "Bilaspur",
]

city_map = {
    **{c: "Metro" for c in metro_cities},
    **{c: "Tier2" for c in tier2_cities},
    **{c: "Town" for c in town_cities},
}

all_cities = list(city_map.keys())

# -------------------------
# Pricing
# -------------------------

price_map = {
    "Electronics": 500,
    "Clothing": 80,
    "Groceries": 30,
    "Furniture": 300,
    "Toys": 60,
}

# -------------------------
# Generate data
# -------------------------

records = []
current_date = start_date

while current_date <= end_date:

    for store in stores:

        city = random.choice(all_cities)
        store_type = city_map[city]

        for category in categories:

            base_units = random.randint(5, 20)

            # Trend
            days_passed = (current_date - start_date).days
            trend_boost = days_passed * 0.01

            # Weekend boost
            weekend_boost = random.randint(5, 15) if current_date.weekday() >= 5 else 0

            # Seasonal boost (Oct–Dec)
            seasonal_boost = (
                random.randint(10, 30) if current_date.month in [10, 11, 12] else 0
            )

            # Promotion
            promotion = random.choice([True, False])
            promo_boost = random.randint(10, 25) if promotion else 0

            # Store type boost
            if store_type == "Metro":
                location_boost = random.randint(20, 40)
            elif store_type == "Tier2":
                location_boost = random.randint(10, 20)
            else:
                location_boost = random.randint(0, 5)

            units_sold = int(
                base_units
                + trend_boost
                + weekend_boost
                + seasonal_boost
                + promo_boost
                + location_boost
            )

            revenue = units_sold * price_map[category]

            records.append(
                {
                    "sale_date": current_date.date(),
                    "store_id": store,
                    "product_category": category,
                    "units_sold": units_sold,
                    "revenue": revenue,
                    "city": city,
                    "store_type": store_type,
                    "promotion": promotion,
                }
            )

    current_date += timedelta(days=1)

# -------------------------
# Insert using SQLAlchemy
# -------------------------

import pandas as pd

df = pd.DataFrame(records)

df.to_sql("retail_sales_data", engine, if_exists="append", index=False)

print(f"✅ Inserted {len(df)} records successfully with secure engine!")
