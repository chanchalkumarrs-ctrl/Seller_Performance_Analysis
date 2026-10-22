# ============================================================
# SELLER PERFORMANCE & DELIVERY REVIEW - PYTHON EDA
# Dataset: olist_order_level_dataset.csv
# ============================================================

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -------------------- 1. FILE PATHS --------------------------

CSV_PATH = r"C:\Sellerr Performance And Delivery Review\02_Dataset\olist_order_level_dataset.csv"

OUTPUT_FOLDER = "EDA_Charts"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# -------------------- 2. LOAD DATASET ------------------------

df = pd.read_csv(CSV_PATH, low_memory=False)

print("=" * 60)
print("SELLER PERFORMANCE & DELIVERY REVIEW")
print("=" * 60)

print("\nDataset loaded successfully!")
print("Rows and columns:", df.shape)
print("\nColumn names:")
print(df.columns.tolist())

# -------------------- 3. DATA INSPECTION ---------------------

print("\n--- DATA TYPES ---")
print(df.dtypes)

print("\n--- MISSING VALUES ---")
print(df.isnull().sum())

print("\n--- DUPLICATE ROWS ---")
print(df.duplicated().sum())

print("\n--- STATISTICAL SUMMARY ---")
print(df.describe(include="all").to_string())

# -------------------- 4. DATA PREPARATION --------------------

date_columns = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "review_creation_date"
]

for col in date_columns:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")

numeric_columns = [
    "total_price", "total_freight", "total_payment",
    "review_score", "seller_count", "avg_weight"
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Delivery duration: purchase date to actual delivery date
df["delivery_days"] = (
    df["order_delivered_customer_date"]
    - df["order_purchase_timestamp"]
).dt.total_seconds() / 86400

# Delay duration: actual delivery compared with estimated date
df["delivery_delay_days"] = (
    df["order_delivered_customer_date"]
    - df["order_estimated_delivery_date"]
).dt.total_seconds() / 86400

df["delivery_status_eda"] = np.select(
    [
        df["order_delivered_customer_date"].isna(),
        df["delivery_delay_days"] > 0
    ],
    [
        "Not Delivered",
        "Delayed"
    ],
    default="On Time or Early"
)

# -------------------- 5. KEY PERFORMANCE INDICATORS ----------

total_orders = df["order_id"].nunique()
average_rating = df["review_score"].mean()
total_sales = df["total_payment"].sum(min_count=1)
average_delivery_days = df["delivery_days"].mean()

delayed_orders = df.loc[
    df["delivery_status_eda"] == "Delayed", "order_id"
].nunique()

delivered_orders = df.loc[
    df["order_delivered_customer_date"].notna(), "order_id"
].nunique()

delay_rate = (
    delayed_orders / delivered_orders * 100
    if delivered_orders else 0
)

low_rating_orders = df.loc[
    df["review_score"] <= 2, "order_id"
].nunique()

print("\n--- KEY PERFORMANCE INDICATORS ---")
print("Total Orders:", total_orders)
print("Average Customer Rating:", round(average_rating, 2))
print("Total Payment Value:", round(total_sales, 2))
print("Average Delivery Days:", round(average_delivery_days, 2))
print("Delayed Orders:", delayed_orders)
print("Delivery Delay Rate (% of delivered orders):", round(delay_rate, 2))
print("Low-Rating Orders (rating <= 2):", low_rating_orders)

# -------------------- 6. CHART 1: RATING DISTRIBUTION --------

plt.figure(figsize=(7, 4))
df["review_score"].value_counts().sort_index().plot(kind="bar")
plt.title("Customer Rating Distribution")
plt.xlabel("Review Score")
plt.ylabel("Number of Rows")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FOLDER, "Chart1_Rating_Distribution.png"))
plt.show()

# -------------------- 7. CHART 2: TOP CATEGORIES -------------

plt.figure(figsize=(9, 5))
df["main_category"].value_counts().head(10).sort_values().plot(kind="barh")
plt.title("Top 10 Product Categories by Order Rows")
plt.xlabel("Number of Rows")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FOLDER, "Chart2_Top_Categories.png"))
plt.show()

# -------------------- 8. CHART 3: ORDERS BY STATE ------------

plt.figure(figsize=(9, 5))
df["customer_state"].value_counts().head(10).sort_values().plot(kind="barh")
plt.title("Top 10 Customer States by Order Rows")
plt.xlabel("Number of Rows")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FOLDER, "Chart3_State_Orders.png"))
plt.show()

# -------------------- 9. CHART 4: MONTHLY ORDERS --------------

monthly_orders = (
    df.dropna(subset=["order_purchase_timestamp"])
      .set_index("order_purchase_timestamp")["order_id"]
      .resample("MS")
      .nunique()
)

plt.figure(figsize=(10, 4))
monthly_orders.plot()
plt.title("Monthly Order Trend")
plt.xlabel("Month")
plt.ylabel("Unique Orders")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FOLDER, "Chart4_Monthly_Orders.png"))
plt.show()

# -------------------- 10. CHART 5: LOWEST RATINGS BY CATEGORY -

category_rating = (
    df.groupby("main_category")["review_score"]
      .mean()
      .dropna()
      .sort_values()
      .head(10)
)

plt.figure(figsize=(9, 5))
category_rating.sort_values().plot(kind="barh")
plt.title("10 Categories with Lowest Average Rating")
plt.xlabel("Average Review Score")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FOLDER, "Chart5_Lowest_Ratings.png"))
plt.show()

# -------------------- 11. CHART 6: DELIVERY DAYS --------------

plt.figure(figsize=(8, 4))
df.loc[
    df["delivery_days"].between(0, 90), "delivery_days"
].dropna().hist(bins=30)

plt.title("Delivery Duration Distribution (0–90 Days)")
plt.xlabel("Days from Purchase to Delivery")
plt.ylabel("Number of Rows")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FOLDER, "Chart6_Delivery_Days.png"))
plt.show()

# -------------------- 12. CHART 7: PAYMENT TYPES --------------

payment_counts = df["payment_type"].fillna("Unknown").value_counts()

plt.figure(figsize=(7, 6))
payment_counts.plot(kind="pie", autopct="%1.1f%%")
plt.title("Payment Type Distribution")
plt.ylabel("")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FOLDER, "Chart7_Payment_Types.png"))
plt.show()

# -------------------- 13. CHART 8: SALES BY STATE -------------

state_sales = (
    df.groupby("customer_state")["total_payment"]
      .sum(min_count=1)
      .dropna()
      .sort_values(ascending=False)
      .head(10)
      .sort_values()
)

plt.figure(figsize=(9, 5))
state_sales.plot(kind="barh")
plt.title("Top 10 Customer States by Total Payment Value")
plt.xlabel("Total Payment Value")
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FOLDER, "Chart8_State_Sales.png"))
plt.show()

# -------------------- 14. EXTRA: DELAY STATUS -----------------

plt.figure(figsize=(7, 4))
df["delivery_status_eda"].value_counts().plot(kind="bar")
plt.title("Delivery Status Breakdown")
plt.xlabel("Delivery Status")
plt.ylabel("Number of Rows")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FOLDER, "Chart9_Delivery_Status.png"))
plt.show()

# -------------------- 15. EXTRA: DELAY VS RATING ---------------

delay_rating = (
    df.groupby("delivery_status_eda")["review_score"]
      .mean()
      .dropna()
)

plt.figure(figsize=(8, 4))
delay_rating.plot(kind="bar")
plt.title("Average Customer Rating by Delivery Status")
plt.xlabel("Delivery Status")
plt.ylabel("Average Review Score")
plt.xticks(rotation=15)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_FOLDER, "Chart10_Delay_vs_Rating.png"))
plt.show()

# -------------------- 16. SAVE SUMMARY TABLES ----------------

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

df.groupby("customer_state", dropna=False).agg(
    unique_orders=("order_id", "nunique"),
    average_rating=("review_score", "mean"),
    total_payment=("total_payment", "sum"),
    average_delivery_days=("delivery_days", "mean")
).to_csv(os.path.join(OUTPUT_FOLDER, "State_Analysis.csv"))

df.groupby("main_category", dropna=False).agg(
    unique_orders=("order_id", "nunique"),
    average_rating=("review_score", "mean"),
    total_payment=("total_payment", "sum")
).to_csv(os.path.join(OUTPUT_FOLDER, "Category_Analysis.csv"))

df.groupby("delivery_status_eda", dropna=False).agg(
    unique_orders=("order_id", "nunique"),
    average_rating=("review_score", "mean")
).to_csv(os.path.join(OUTPUT_FOLDER, "Delivery_Status_Analysis.csv"))

# -------------------- 17. AUTOMATIC INSIGHTS -----------------

print("\n--- KEY INSIGHTS ---")

if df["main_category"].notna().any():
    print("Most frequent category:", df["main_category"].mode().iloc[0])

if df["customer_state"].notna().any():
    print("State with most order rows:", df["customer_state"].mode().iloc[0])

if not category_rating.empty:
    print("Lowest-rated category:", category_rating.index[0])
    print("Its average rating:", round(category_rating.iloc[0], 2))

if not state_sales.empty:
    print("State with highest total payment value:", state_sales.idxmax())

print("\nCharts and summary CSV files saved in:", os.path.abspath(OUTPUT_FOLDER))
print("\nPython EDA completed successfully!")