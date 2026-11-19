
import pandas as pd

# Excel dosyasini oku
df = pd.read_excel("Online Retail.xlsx")

# Satir ve sutun sayisini goster
print("Dataset size:", df.shape)

# Ilk 5 satiri goster
print(df.head())

# Check missing values
print("\nMissing Values:")
print(df.isnull().sum())

# Check data types
print("\nData Types:")
print(df.dtypes)

# Check duplicate rows
print("\nDuplicate Rows:")
print(df.duplicated().sum())

# Check negative quantities
print("\nNegative Quantities:")
print((df["Quantity"] < 0).sum())

# Check zero or negative prices
print("\nZero or Negative Prices:")
print((df["UnitPrice"] <= 0).sum())

# Check cancelled invoices
print("\nCancelled Invoices:")
print(df["InvoiceNo"].astype(str).str.startswith("C").sum())

# Identify cancelled invoices
cancelled = df["InvoiceNo"].astype(str).str.startswith("C")

# Identify negative quantities
negative = df["Quantity"] < 0

# Negative quantities without cancellation
print("\nNegative but not cancelled:")
print((negative & ~cancelled).sum())

# Cancelled invoices with positive quantities
print("\nCancelled with positive quantity:")
print((cancelled & (df["Quantity"] > 0)).sum())
# Filter valid sales transactions
sales = df[
    (~cancelled) &
    (df["Quantity"] > 0) &
    (df["UnitPrice"] > 0)
].copy()

# Compare dataset sizes
print("\nOriginal rows:", len(df))
print("Filtered sales rows:", len(sales))

# Save filtered dataset
sales.to_csv("sales_filtered.csv", index=False)

print("Filtered dataset saved successfully!")
# Calculate sales value for each row
sales["SalesValue"] = sales["Quantity"] * sales["UnitPrice"]

# Calculate total sales value
total_sales = sales["SalesValue"].sum()

print("\nTotal Gross Sales Value:")
print(f"{total_sales:,.2f}")

# Investigate product 23843 in original data

suspicious = df[
    df["StockCode"].astype(str) == "23843"
]

print("\nInvestigation of StockCode 23843:")
print(
    suspicious[
        ["InvoiceNo", "Quantity", "UnitPrice", "InvoiceDate"]
    ].to_string(index=False)
)


