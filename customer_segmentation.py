
import pandas as pd

# Load cleaned data
df = pd.read_csv("cleaned_retail_data.csv")
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Customer ID missing rows cannot be used for customer segmentation
df = df.dropna(subset=["CustomerID"]).copy()
df["CustomerID"] = df["CustomerID"].astype(int).astype(str)

# Set analysis date one day after the last transaction
analysis_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)

# Calculate RFM metrics for each customer
rfm = df.groupby("CustomerID").agg(
    Recency=("InvoiceDate", lambda dates: (analysis_date - dates.max()).days),
    Frequency=("InvoiceNo", "nunique"),
    Monetary=("Revenue", "sum")
)

# Assign scores: 5 is better for each metric
rfm["R_Score"] = pd.qcut(
    rfm["Recency"].rank(method="first"),
    5, labels=[5, 4, 3, 2, 1]
).astype(int)

rfm["F_Score"] = pd.qcut(
    rfm["Frequency"].rank(method="first"),
    5, labels=[1, 2, 3, 4, 5]
).astype(int)

rfm["M_Score"] = pd.qcut(
    rfm["Monetary"].rank(method="first"),
    5, labels=[1, 2, 3, 4, 5]
).astype(int)

# Simple, explainable customer segments
def segment_customer(row):
    if row["R_Score"] >= 4 and row["F_Score"] >= 4:
        return "Loyal / Active"
    elif row["R_Score"] >= 4:
        return "Recent Customers"
    elif row["F_Score"] >= 4:
        return "Frequent Customers"
    else:
        return "Needs Attention"

rfm["Segment"] = rfm.apply(segment_customer, axis=1)

# Save results
rfm.to_csv("customer_segments.csv")

print("\n===== CUSTOMER SEGMENTATION REPORT =====")
print("Total customers analyzed:", len(rfm))
print("\nCustomers in each segment:")
print(rfm["Segment"].value_counts())
print("\nTop 10 customers by total spending:")
print(rfm.sort_values("Monetary", ascending=False)[
    ["Recency", "Frequency", "Monetary", "Segment"]
].head(10).round(2))

print("\nSaved customer_segments.csv successfully!")
