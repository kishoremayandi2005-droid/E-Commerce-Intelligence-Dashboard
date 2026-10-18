
import pandas as pd

# Keep the file path that worked in your previous code
file_path = r"online+retail (2)\Online Retail.xlsx"

print("Loading dataset...")
df = pd.read_excel(file_path)

print("\n===== DATA CLEANING REPORT =====")
print("Original rows:", len(df))

# Remove rows with missing product descriptions
df = df.dropna(subset=["Description"])

# Remove cancelled invoices (invoice numbers starting with C)
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

# Keep only positive quantities and unit prices
df = df[(df["Quantity"] > 0) & (df["UnitPrice"] > 0)]

# Calculate revenue for each line item
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

print("Rows after cleaning:", len(df))
print("Missing customer IDs remaining:", df["CustomerID"].isna().sum())
print("Total revenue: £{:,.2f}".format(df["Revenue"].sum()))
print("Unique countries:", df["Country"].nunique())
print("Unique invoices:", df["InvoiceNo"].nunique())

# Save cleaned dataset
df.to_csv("cleaned_retail_data.csv", index=False)

print("\nCleaned dataset saved successfully!")
print("File: cleaned_retail_data.csv")
