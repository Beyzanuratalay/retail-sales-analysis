import pandas as pd

excluded_codes = {
    "DOT", "POST", "M", "23843", "AMAZONFEE", "B",
    "C2", "BANK CHARGES", "S",
}


def classify_abc(sales):
    products = sales.groupby("StockCode", as_index=False)["SalesValue"].sum()
    products = products.sort_values(
        ["SalesValue", "StockCode"], ascending=[False, True]
    )

    cumulative_share = products["SalesValue"].cumsum() / products["SalesValue"].sum()
    products["ABC"] = pd.cut(
        cumulative_share,
        bins=[0, 0.80, 0.95, float("inf")],
        labels=["A", "B", "C"],
    )
    return products[["StockCode", "SalesValue", "ABC"]]


raw = pd.read_excel(
    "Online Retail.xlsx", dtype={"InvoiceNo": str, "StockCode": str}
)
exact_repeats = raw.duplicated(keep="first")

sales_mask = (
    ~raw["InvoiceNo"].str.upper().str.startswith("C", na=False)
    & raw["Quantity"].gt(0)
    & raw["UnitPrice"].gt(0)
    & ~raw["StockCode"].isin(excluded_codes)
    & ~raw["StockCode"].str.startswith("gift_", na=False)
)
sales = raw.loc[sales_mask].copy()
sales["SalesValue"] = sales["Quantity"] * sales["UnitPrice"]

before = classify_abc(sales)
after = classify_abc(sales.loc[~exact_repeats.loc[sales.index]])

comparison = before.merge(
    after,
    on="StockCode",
    suffixes=("_before", "_after"),
    validate="one_to_one",
)
changed = comparison.loc[comparison["ABC_before"].ne(comparison["ABC_after"])]

print(f"Products changing class: {len(changed):,} / {len(comparison):,}")
print(pd.crosstab(comparison["ABC_before"], comparison["ABC_after"]))
changed.to_csv("abc_class_changes.csv", index=False)