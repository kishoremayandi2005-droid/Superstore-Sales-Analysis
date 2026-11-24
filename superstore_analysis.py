
import pandas as pd

# Load Original Dataset
df = pd.read_csv("superstore_sales.csv")

print("ORIGINAL DATASET")
print("Rows:", df.shape[0])

# Step 1: Convert Date Columns
df["Order Date"] = pd.to_datetime(
    df["Order Date"], format="mixed", errors="coerce"
)

df["Ship Date"] = pd.to_datetime(
    df["Ship Date"], format="mixed", errors="coerce"
)

# Step 2: Convert Numeric Columns
numeric_columns = ["Sales", "Quantity", "Discount", "Profit"]

for col in numeric_columns:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Step 3: Remove Invalid Records
required_columns = [
    "Order Date",
    "Ship Date",
    "Sales",
    "Quantity",
    "Discount",
    "Profit",
    "Category",
    "Region",
    "Segment"
]

df = df.dropna(subset=required_columns)

# Step 4: Remove Exact Duplicates
df = df.drop_duplicates()

# Step 5: Reset Index
df = df.reset_index(drop=True)

# Step 6: Check Cleaned Dataset
print("\nCLEANED DATASET")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\nMISSING VALUES")
print(df.isnull().sum())

print("\nDUPLICATE RECORDS")
print(df.duplicated().sum())

# Step 7: Save Cleaned Dataset
df.to_csv("superstore_cleaned.csv", index=False)

print("\nCleaned dataset saved successfully!")

# ==================================
# STEP 5: OVERALL BUSINESS ANALYSIS
# ==================================

print("\n========== BUSINESS ANALYSIS ==========")

# 1. Total Sales
total_sales = df["Sales"].sum()
print(f"Total Sales: ${total_sales:,.2f}")

# 2. Total Profit
total_profit = df["Profit"].sum()
print(f"Total Profit: ${total_profit:,.2f}")

# 3. Total Orders
total_orders = df["Order ID"].nunique()
print(f"Total Orders: {total_orders}")

# 4. Total Customers
total_customers = df["Customer ID"].nunique()
print(f"Total Customers: {total_customers}")

# 5. Total Quantity
total_quantity = df["Quantity"].sum()
print(f"Total Quantity Sold: {total_quantity:,.0f}")

# 6. Average Discount
avg_discount = df["Discount"].mean() * 100
print(f"Average Discount: {avg_discount:.2f}%")

# 7. Category-wise Sales
print("\n--- CATEGORY-WISE SALES & PROFIT ---")

category_analysis = df.groupby("Category")[
    ["Sales", "Profit"]
].sum().sort_values(by="Sales", ascending=False)

print(category_analysis.round(2))

# 8. Region-wise Sales
print("\n--- REGION-WISE SALES & PROFIT ---")

region_analysis = df.groupby("Region")[
    ["Sales", "Profit"]
].sum().sort_values(by="Sales", ascending=False)

print(region_analysis.round(2))

# 9. Customer Segment Analysis
print("\n--- CUSTOMER SEGMENT ANALYSIS ---")

segment_analysis = df.groupby("Segment")[
    ["Sales", "Profit"]
].sum().sort_values(by="Sales", ascending=False)

print(segment_analysis.round(2))

print("\n========== ANALYSIS COMPLETED ==========")

# ==================================
# STEP 6: MONTHLY SALES ANALYSIS
# ==================================

import matplotlib.pyplot as plt
import seaborn as sns

print("\n========== MONTHLY SALES ANALYSIS ==========")

# Extract Year-Month
df["Year-Month"] = df["Order Date"].dt.to_period("M").astype(str)

# Group Monthly Sales
monthly_sales = df.groupby("Year-Month")["Sales"].sum().reset_index()

# Sort by date
monthly_sales = monthly_sales.sort_values("Year-Month")

# Display Monthly Sales
print("\n--- MONTHLY SALES ---")
print(monthly_sales.to_string(index=False))

# Find Highest Sales Month
best_month = monthly_sales.loc[
    monthly_sales["Sales"].idxmax()
]

print("\nHighest Sales Month:", best_month["Year-Month"])
print("Highest Monthly Sales: $", round(best_month["Sales"], 2))

# Save Monthly Results
monthly_sales.to_csv("monthly_sales_analysis.csv", index=False)

# Create Monthly Sales Chart
plt.figure(figsize=(14, 6))

sns.lineplot(
    data=monthly_sales,
    x="Year-Month",
    y="Sales",
    marker="o",
    linewidth=2
)

plt.title("Monthly Sales Trend Analysis", fontsize=16)
plt.xlabel("Year-Month")
plt.ylabel("Total Sales ($)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig("monthly_sales_trend.png", dpi=300)
plt.show()

print("\nMonthly Sales Analysis Completed!")

# ==========================================
# STEP 7: CATEGORY & SUB-CATEGORY ANALYSIS
# ==========================================

print("\n========== CATEGORY ANALYSIS ==========")

# Category-wise Sales and Profit
category_data = df.groupby("Category").agg({
    "Sales": "sum",
    "Profit": "sum",
    "Quantity": "sum"
}).sort_values(by="Sales", ascending=False)

print("\n--- CATEGORY PERFORMANCE ---")
print(category_data.round(2))

# Sub-category Analysis
subcategory_data = df.groupby("Sub-Category").agg({
    "Sales": "sum",
    "Profit": "sum",
    "Quantity": "sum"
}).sort_values(by="Sales", ascending=False)

print("\n--- SUB-CATEGORY PERFORMANCE ---")
print(subcategory_data.round(2))

# Highest Revenue Sub-category
best_subcategory = subcategory_data["Sales"].idxmax()

print("\nHighest Revenue Sub-Category:", best_subcategory)

# Lowest Profit Sub-category
lowest_profit = subcategory_data["Profit"].idxmin()

print("Lowest Profit Sub-Category:", lowest_profit)

# Save Results
category_data.to_csv("category_analysis.csv")
subcategory_data.to_csv("subcategory_analysis.csv")

# Visualization 1: Category Sales
plt.figure(figsize=(9, 5))

sns.barplot(
    x=category_data.index,
    y=category_data["Sales"]
)

plt.title("Category-wise Sales")
plt.xlabel("Category")
plt.ylabel("Sales ($)")
plt.tight_layout()
plt.savefig("category_sales.png", dpi=300)
plt.show()

# Visualization 2: Sub-category Profit
plt.figure(figsize=(12, 6))

sns.barplot(
    x=subcategory_data.index,
    y=subcategory_data["Profit"]
)

plt.title("Sub-Category-wise Profit")
plt.xlabel("Sub-Category")
plt.ylabel("Profit ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("subcategory_profit.png", dpi=300)
plt.show()

print("\nCategory Analysis Completed!")

# ==========================================
# STEP 8: REGION & CUSTOMER ANALYSIS
# ==========================================

# Region Analysis
region_data = df.groupby("Region").agg({
    "Sales": "sum",
    "Profit": "sum"
}).sort_values(by="Sales", ascending=False)

print("\n--- REGION ANALYSIS ---")
print(region_data.round(2))

# Customer Segment Analysis
segment_data = df.groupby("Segment").agg({
    "Sales": "sum",
    "Profit": "sum"
}).sort_values(by="Sales", ascending=False)

print("\n--- CUSTOMER SEGMENT ANALYSIS ---")
print(segment_data.round(2))

# Save CSV files
region_data.to_csv("region_analysis.csv")
segment_data.to_csv("customer_segment_analysis.csv")

# Region Sales Chart
plt.figure(figsize=(9, 5))
sns.barplot(x=region_data.index, y=region_data["Sales"])
plt.title("Region-wise Sales Analysis")
plt.xlabel("Region")
plt.ylabel("Sales ($)")
plt.tight_layout()
plt.savefig("region_sales.png", dpi=300)
plt.show()

# Customer Segment Chart
plt.figure(figsize=(9, 5))
sns.barplot(x=segment_data.index, y=segment_data["Sales"])
plt.title("Customer Segment Sales Analysis")
plt.xlabel("Customer Segment")
plt.ylabel("Sales ($)")
plt.tight_layout()
plt.savefig("customer_segment_sales.png", dpi=300)
plt.show()

print("\nRegion & Customer Analysis Completed!")
# STEP 9: TOP 10 PRODUCTS ANALYSIS

print("\n========== TOP 10 PRODUCTS ANALYSIS ==========")

product_data = df.groupby("Product Name").agg({
    "Sales": "sum",
    "Profit": "sum",
    "Quantity": "sum"
})

top_products = product_data.sort_values(
    by="Sales", ascending=False
).head(10)

print("\n--- TOP 10 PRODUCTS BY SALES ---")
print(top_products.round(2))

top_products.to_csv("top_10_products.csv")

plt.figure(figsize=(12, 6))
sns.barplot(
    data=top_products.reset_index(),
    x="Sales",
    y="Product Name"
)

plt.title("Top 10 Products by Sales")
plt.xlabel("Total Sales ($)")
plt.ylabel("Product Name")
plt.tight_layout()
plt.savefig("top_10_products.png", dpi=300)
plt.show()
plt.close()

print("\nTop 10 Products Analysis Completed!")
# STEP 10: PROFIT ANALYSIS

print("\n========== PROFIT ANALYSIS ==========")

profit_products = df.groupby("Sub-Category")["Profit"].sum()

top_profit = profit_products.sort_values(
    ascending=False
).head(10)

low_profit = profit_products.sort_values().head(10)

print("\n--- TOP 10 PROFITABLE SUB-CATEGORIES ---")
print(top_profit.round(2))

print("\n--- LOWEST PROFIT SUB-CATEGORIES ---")
print(low_profit.round(2))

top_profit.to_csv("top_10_profitable_categories.csv")
low_profit.to_csv("lowest_profit_categories.csv")

plt.figure(figsize=(12, 6))
sns.barplot(x=top_profit.values, y=top_profit.index)
plt.title("Top 10 Profitable Sub-Categories")
plt.xlabel("Total Profit ($)")
plt.ylabel("Sub-Category")
plt.tight_layout()
plt.savefig("top_10_profit.png", dpi=300)
plt.show()
plt.close()

print("\nProfit Analysis Completed!")