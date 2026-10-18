
import pandas as pd

# Load the cleaned dataset
df = pd.read_csv("cleaned_retail_data.csv")

# Convert invoice date into datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print("\n===== E-COMMERCE BUSINESS INSIGHTS =====")

# 1. Total revenue
print("\n1. Total Revenue:")
print(f"£{df['Revenue'].sum():,.2f}")

# 2. Top 10 products by revenue
print("\n2. TOP 10 PRODUCTS BY REVENUE:")
top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print(top_products.round(2))

# 3. Monthly revenue
df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)
monthly_sales = df.groupby("Month")["Revenue"].sum()

print("\n3. MONTHLY REVENUE:")
print(monthly_sales.round(2))

# 4. Top 10 countries by revenue
print("\n4. TOP 10 COUNTRIES:")
country_sales = (
    df.groupby("Country")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)
print(country_sales.round(2))

# 5. Save analysis results
top_products.to_csv("top_products.csv", header=["Revenue"])
monthly_sales.to_csv("monthly_revenue.csv", header=["Revenue"])
country_sales.to_csv("country_sales.csv", header=["Revenue"])

print("\nAnalysis complete!")
print("Saved: top_products.csv, monthly_revenue.csv, country_sales.csv")

