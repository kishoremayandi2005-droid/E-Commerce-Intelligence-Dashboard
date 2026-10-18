
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Create a folder for charts
Path("charts").mkdir(exist_ok=True)

# Load cleaned data
df = pd.read_csv("cleaned_retail_data.csv")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
df["Month"] = df["InvoiceDate"].dt.to_period("M").astype(str)

# Chart 1: Monthly Revenue
monthly_sales = df.groupby("Month")["Revenue"].sum()

plt.figure(figsize=(12, 6))
monthly_sales.plot(kind="line", marker="o")
plt.title("Monthly Revenue Trend", fontsize=16)
plt.xlabel("Month")
plt.ylabel("Revenue (£)")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("charts/monthly_revenue.png", dpi=150)
plt.show()
plt.close()

# Chart 2: Top 10 Products
top_products = (
    df.groupby("Description")["Revenue"]
    .sum()
    .nlargest(10)
    .sort_values()
)

plt.figure(figsize=(12, 7))
top_products.plot(kind="barh")
plt.title("Top 10 Products by Revenue", fontsize=16)
plt.xlabel("Revenue (£)")
plt.ylabel("Product")
plt.tight_layout()
plt.savefig("charts/top_products.png", dpi=150)
plt.show()
plt.close()

# Chart 3: Top 10 Countries
country_sales = (
    df.groupby("Country")["Revenue"]
    .sum()
    .nlargest(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))
country_sales.plot(kind="barh")
plt.title("Top 10 Countries by Revenue", fontsize=16)
plt.xlabel("Revenue (£)")
plt.ylabel("Country")
plt.tight_layout()
plt.savefig("charts/country_sales.png", dpi=150)
plt.show()
plt.close()

print("All 3 charts created successfully!")
print("Check the charts folder for PNG files.")
