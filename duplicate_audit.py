"""Compare gross sales before and after exact-row deduplication."""

import argparse
from pathlib import Path

import pandas as pd


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workbook", type=Path, help="Path to Online Retail.xlsx")
    args = parser.parse_args()

    raw = pd.read_excel(args.workbook, dtype={"InvoiceNo": str, "StockCode": str})
    duplicate_rows = raw.duplicated(keep="first")
    all_matching_rows = raw.duplicated(keep=False)

    sales_mask = (
        ~raw["InvoiceNo"].str.upper().str.startswith("C", na=False)
        & raw["Quantity"].gt(0)
        & raw["UnitPrice"].gt(0)
    )

    sales = raw.loc[sales_mask].copy()
    sales["SalesValue"] = sales["Quantity"] * sales["UnitPrice"]
    deduplicated_sales = sales.loc[~duplicate_rows.loc[sales.index]]

    baseline_value = sales["SalesValue"].sum()
    deduplicated_value = deduplicated_sales["SalesValue"].sum()
    difference = baseline_value - deduplicated_value

    print(f"Raw invoice lines: {len(raw):,}")
    print(f"Raw exact repeats beyond the first occurrence: {duplicate_rows.sum():,}")
    print(f"Raw lines in exact-repeat groups, including first occurrences: {all_matching_rows.sum():,}")
    print(f"Filtered invoice lines: {len(sales):,}")
    print(f"Filtered invoice lines after deduplication: {len(deduplicated_sales):,}")
    print(f"Exact repeats removed from filtered data: {len(sales) - len(deduplicated_sales):,}")
    print(f"Gross sales before deduplication: £{baseline_value:,.2f}")
    print(f"Gross sales after deduplication: £{deduplicated_value:,.2f}")
    print(f"Difference: £{difference:,.2f} ({difference / baseline_value:.2%} of baseline)")
    print(f"Distinct sales invoices before deduplication: {sales['InvoiceNo'].nunique():,}")
    print(f"Distinct sales invoices after deduplication: {deduplicated_sales['InvoiceNo'].nunique():,}")

    print("\nLargest gross sales reductions by country")
    removed = sales.loc[duplicate_rows.loc[sales.index]]
    by_country = removed.groupby("Country")["SalesValue"].sum().nlargest(5)
    for country, value in by_country.items():
        print(f"{country}: £{value:,.2f}")


if __name__ == "__main__":
    main()