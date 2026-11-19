

import pandas as pd


sales = pd.read_csv("sales_filtered.csv", dtype={"InvoiceNo": str})


sales["SalesValue"] = sales["Quantity"] * sales["UnitPrice"]

total_sales = sales["SalesValue"].sum()

print(f"Total Sales: £{total_sales:,.2f}")

import pandas as pd

# Read the filtered sales dataset
sales = pd.read_csv(
    "sales_filtered.csv",
    dtype={"InvoiceNo": str}
)

# Calculate sales value for each transaction
sales["SalesValue"] = sales["Quantity"] * sales["UnitPrice"]

# Calculate total gross sales
total_sales = sales["SalesValue"].sum()

# Display results
print("Total Sales Analysis")
print("--------------------")
print("Total Transactions:", len(sales))
print(f"Total Gross Sales: £{total_sales:,.2f}")
# Calculate sales by country
country_sales = sales.groupby("Country")["SalesValue"].sum()

# Sort countries by sales
country_sales = country_sales.sort_values(ascending=False)

# Display top 10 countries
print("\nTop 10 Countries by Sales:")
print(country_sales.head(10))

# Calculate each country's sales percentage
country_share = (country_sales / total_sales) * 100

# Display top 10 countries
print("\nTop 10 Countries - Sales Percentage:")
print(country_share.head(10).round(2))

import matplotlib.pyplot as plt

# Select top 10 countries
top10 = country_share.head(10)

# Create bar chart
plt.figure(figsize=(10, 6))

plt.barh(top10.index, top10.values)

# Add title and labels
plt.title("Top 10 Countries by Sales Share")
plt.xlabel("Percentage of Total Sales (%)")
plt.ylabel("Country")

# Show highest country at the top
plt.gca().invert_yaxis()

# Save chart
plt.tight_layout()
plt.savefig("country_sales.png", dpi=300)

# Display chart
plt.close()
# Top 10 countries excluding the UK
non_uk_sales = country_sales.drop("United Kingdom").head(10)

plt.figure(figsize=(10, 6))

plt.barh(non_uk_sales.index, non_uk_sales.values)

plt.title("Top 10 International Markets by Sales")
plt.xlabel("Gross Sales (£)")
plt.ylabel("Country")

plt.gca().invert_yaxis()

plt.tight_layout()
plt.savefig("international_sales.png", dpi=300)

plt.close()
# Monthly Sales Analysis

# Convert InvoiceDate to datetime
sales["InvoiceDate"] = pd.to_datetime(
    sales["InvoiceDate"],
    errors="coerce"
)

# Calculate monthly sales
monthly_sales = sales.groupby(
    sales["InvoiceDate"].dt.to_period("M")
)["SalesValue"].sum()

# Sort months chronologically
monthly_sales = monthly_sales.sort_index()

# Display results
print("\nMonthly Sales Analysis:")
print(monthly_sales.round(2))# Monthly sales trend chart
plt.figure(figsize=(10, 6))

plt.plot(monthly_sales.index.astype(str), monthly_sales.values, marker="o")

plt.title("Monthly Gross Sales Trend")
plt.xlabel("Month")
plt.ylabel("Gross Sales (£)")

plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig("monthly_sales_trend.png", dpi=300)
plt.close()

# Product Sales Analysis

product_sales = sales.groupby("StockCode")[
    ["Quantity", "SalesValue"]
].sum()

# Sort products by total sales value
product_sales = product_sales.sort_values(
    by="SalesValue",
    ascending=False
)

# Display top 10 products
print("\nTop 10 Products by Sales Value:")
print(product_sales.head(10))
# Investigate unusual product codes

codes = ["DOT", "M", "POST", "23843"]

for code in codes:
    product = sales[sales["StockCode"] == code]

    print("\nStockCode:", code)
    print("Descriptions:")
    print(product["Description"].dropna().unique()[:5])
    print("Number of rows:", len(product))
    print("Maximum Quantity:", product["Quantity"].max())

# Prepare product data for ABC analysis

excluded_codes = [
    "DOT",
    "POST",
    "M",
    "23843",
    "AMAZONFEE",
    "B",
    "C2",
    "BANK CHARGES",
    "S"
]



product_data = sales[
    ~sales["StockCode"].astype(str).isin(excluded_codes)
].copy()

product_ranking = product_data.groupby(
    "StockCode"
)["SalesValue"].sum()

product_ranking = product_ranking.sort_values(
    ascending=False
)

print("\nTop 10 Products - Updated:")
print(product_ranking.head(10))

# ABC Analysis

abc = product_ranking.reset_index()

# Calculate each product's sales contribution
abc["SalesShare"] = (
    abc["SalesValue"] / abc["SalesValue"].sum()
) * 100

# Calculate cumulative percentage
abc["CumulativeShare"] = abc["SalesShare"].cumsum()

# Classify products
def abc_class(value):
    if value <= 80:
        return "A"
    elif value <= 95:
        return "B"
    else:
        return "C"

abc["ABC_Class"] = abc["CumulativeShare"].apply(abc_class)

# Summarize ABC groups
summary = abc.groupby("ABC_Class").agg(
    ProductCount=("StockCode", "count"),
    TotalSales=("SalesValue", "sum")
)

summary["SalesSharePercent"] = (
    summary["TotalSales"] / summary["TotalSales"].sum() * 100
)

print("\nABC Analysis Summary:")
print(summary.round(2))

# ABC Pareto Chart

plt.figure(figsize=(10, 6))

# Cumulative sales percentage by product rank
plt.plot(
    range(1, len(abc) + 1),
    abc["CumulativeShare"],
    color="green"
)

# ABC thresholds
plt.axhline(y=80, linestyle="--", color="orange")
plt.axhline(y=95, linestyle="--", color="red")

plt.title("ABC Analysis - Cumulative Sales Share")
plt.xlabel("Products Ranked by Sales Value")
plt.ylabel("Cumulative Sales Share (%)")

plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("abc_pareto.png", dpi=300)
plt.close()

# ABC Pareto Chart

plt.figure(figsize=(10, 6))

# Cumulative sales percentage by product rank
plt.plot(
    range(1, len(abc) + 1),
    abc["CumulativeShare"],
    color="green"
)

# ABC thresholds
plt.axhline(y=80, linestyle="--", color="orange")
plt.axhline(y=95, linestyle="--", color="red")

plt.title("ABC Analysis - Cumulative Sales Share")
plt.xlabel("Products Ranked by Sales Value")
plt.ylabel("Cumulative Sales Share (%)")

plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("abc_pareto.png", dpi=300)
plt.close()

# ABC Pareto Chart

plt.figure(figsize=(10, 6))

# Cumulative sales percentage by product rank
plt.plot(
    range(1, len(abc) + 1),
    abc["CumulativeShare"],
    color="green"
)

# ABC thresholds
plt.axhline(y=80, linestyle="--", color="orange")
plt.axhline(y=95, linestyle="--", color="red")

plt.title("ABC Analysis - Cumulative Sales Share")
plt.xlabel("Products Ranked by Sales Value")
plt.ylabel("Cumulative Sales Share (%)")

plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("abc_pareto.png", dpi=300)
plt.close()

# ABC Pareto Chart

plt.figure(figsize=(10, 6))

# Cumulative sales percentage by product rank
plt.plot(
    range(1, len(abc) + 1),
    abc["CumulativeShare"],
    color="green"
)

# ABC thresholds
plt.axhline(y=80, linestyle="--", color="orange")
plt.axhline(y=95, linestyle="--", color="red")

plt.title("ABC Analysis - Cumulative Sales Share")
plt.xlabel("Products Ranked by Sales Value")
plt.ylabel("Cumulative Sales Share (%)")

plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("abc_pareto.png", dpi=300)
plt.close()
# ABC Pareto Chart

plt.figure(figsize=(10, 6))

# Cumulative sales percentage by product rank
plt.plot(
    range(1, len(abc) + 1),
    abc["CumulativeShare"],
    color="green"
)

# ABC thresholds
plt.axhline(y=80, linestyle="--", color="orange")
plt.axhline(y=95, linestyle="--", color="red")

plt.title("ABC Analysis - Cumulative Sales Share")
plt.xlabel("Products Ranked by Sales Value")
plt.ylabel("Cumulative Sales Share (%)")

plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("abc_pareto.png", dpi=300)
plt.close()


# ABC Pareto Chart

plt.figure(figsize=(10, 6))

# Cumulative sales percentage by product rank
plt.plot(
    range(1, len(abc) + 1),
    abc["CumulativeShare"],
    color="green"
)

# ABC thresholds
plt.axhline(y=80, linestyle="--", color="orange")
plt.axhline(y=95, linestyle="--", color="red")

plt.title("ABC Analysis - Cumulative Sales Share")
plt.xlabel("Products Ranked by Sales Value")
plt.ylabel("Cumulative Sales Share (%)")

plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("abc_pareto.png", dpi=300)
plt.close()

# Check unusual stock codes

standard_codes = sales["StockCode"].astype(str).str.fullmatch(
    r"\d{5}[A-Za-z]*"
)

unusual_products = sales[~standard_codes]

unusual_summary = unusual_products.groupby(
    ["StockCode", "Description"],
    dropna=False
)["SalesValue"].sum().sort_values(ascending=False)

print("\nUnusual Stock Codes:")
print(unusual_summary.head(15).round(2))
# Export preliminary ABC analysis results

abc.to_csv("abc_analysis_preliminary.csv", index=False)

print("\nABC analysis file saved successfully!")

