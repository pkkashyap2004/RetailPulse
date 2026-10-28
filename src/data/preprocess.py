"""RetailPulse Day 2 cleaning pipeline. Run from repo root: python src/data/preprocess.py"""
from pathlib import Path
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW, OUT, REPORTS = ROOT / "data/raw", ROOT / "data/processed", ROOT / "reports"

def clean_data():
    OUT.mkdir(parents=True, exist_ok=True)
    REPORTS.mkdir(parents=True, exist_ok=True)
    sales = pd.read_csv(RAW / "sales.csv")
    customers = pd.read_csv(RAW / "customers.csv")
    products = pd.read_csv(RAW / "products.csv")
    inventory = pd.read_csv(RAW / "inventory.csv")

    # Normalize customer master IDs: observed source relationship is 1001 -> C0001.
    customers["customer_id"] = customers["customer_id"].astype(int).map(lambda x: f"C{x - 1000:04d}")
    sales["customer_id"] = sales["customer_id"].astype("string").str.strip().str.upper()
    for df, col in [(sales, "date"), (customers, "registration_date"), (inventory, "date")]:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    for col in ["quantity", "unit_price", "discount", "total_amount"]:
        sales[col] = pd.to_numeric(sales[col], errors="coerce")
    customers["age"] = pd.to_numeric(customers["age"], errors="coerce")
    for col in ["unit_cost", "selling_price"]:
        products[col] = pd.to_numeric(products[col], errors="coerce")
    for col in ["stock_quantity", "reorder_level", "lead_time"]:
        inventory[col] = pd.to_numeric(inventory[col], errors="coerce")

    frames = {"sales": sales, "customers": customers, "products": products, "inventory": inventory}
    nulls = {k: int(v.isna().sum().sum()) for k, v in frames.items()}
    if any(nulls.values()):
        raise ValueError(f"Missing/invalid values after conversion: {nulls}")
    keys = [(sales, ["transaction_id"]), (customers, ["customer_id"]), (products, ["product_id"]), (inventory, ["product_id", "date"])]
    for df, cols in keys:
        if df.duplicated(subset=cols).any():
            raise ValueError(f"Duplicate business key detected: {cols}")
    if not sales["discount"].between(0, 100).all() or not (sales["quantity"] > 0).all():
        raise ValueError("Invalid sales quantity or discount")
    if not (sales[["unit_price", "total_amount"]] >= 0).all().all():
        raise ValueError("Negative sales price/amount")
    if not (products[["unit_cost", "selling_price"]] >= 0).all().all():
        raise ValueError("Negative product cost/price")
    if not (inventory[["stock_quantity", "reorder_level", "lead_time"]] >= 0).all().all():
        raise ValueError("Negative inventory values")
    missing_customers = sorted(set(sales.customer_id) - set(customers.customer_id))
    missing_products = sorted((set(sales.product_id) | set(inventory.product_id)) - set(products.product_id))
    if missing_customers or missing_products:
        raise ValueError(f"Referential integrity failure: customer={missing_customers[:10]}, product={missing_products[:10]}")

    sales["gross_amount"] = (sales.quantity * sales.unit_price).round(2)
    sales["discount_amount"] = (sales.gross_amount * sales.discount / 100).round(2)
    sales["calculated_total"] = (sales.gross_amount - sales.discount_amount).round(2)
    sales["calculation_difference"] = (sales.total_amount - sales.calculated_total).round(2)
    sales["year"] = sales.date.dt.year
    sales["month"] = sales.date.dt.strftime("%m")
    sales["day_of_week"] = sales.date.dt.dayofweek
    products["unit_margin"] = (products.selling_price - products.unit_cost).round(2)
    products["margin_pct"] = (products.unit_margin / products.selling_price.replace(0, pd.NA) * 100).round(2)
    inventory["stock_gap"] = inventory.stock_quantity - inventory.reorder_level
    inventory["below_reorder"] = inventory.stock_quantity < inventory.reorder_level

    for df in frames.values():
        for col in df.select_dtypes(include=["datetime64[ns]", "datetimetz"]).columns:
            df[col] = df[col].dt.strftime("%Y-%m-%d")
    outputs = {"sales_clean.csv": sales, "customers_clean.csv": customers, "products_clean.csv": products, "inventory_clean.csv": inventory}
    for name, df in outputs.items():
        df.to_csv(OUT / name, index=False)
    report = {"rows": {k: len(v) for k, v in frames.items()}, "missing_after_conversion": nulls,
              "unmatched_sales_customers": len(missing_customers), "unmatched_product_ids": len(missing_products),
              "revenue": round(float(sales.total_amount.sum()), 2),
              "inventory_below_reorder": int(inventory.below_reorder.sum()),
              "max_abs_sales_calculation_difference": round(float(sales.calculation_difference.abs().max()), 2),
              "outputs": list(outputs)}
    (REPORTS / "day2_data_quality.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return report

if __name__ == "__main__":
    clean_data()
