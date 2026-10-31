"""Inventory review from the latest snapshot and observed sales velocity."""
import pandas as pd
def build_reorder_review(sales,inventory,products):
    s=sales.copy();s["date"]=pd.to_datetime(s.date);i=inventory.copy();i["date"]=pd.to_datetime(i.date)
    span=max(1,(s.date.max()-s.date.min()).days+1)
    latest=i.sort_values("date").groupby("product_id").tail(1)
    velocity=s.groupby("product_id").quantity.sum().div(span).rename("units_per_day")
    r=latest.merge(velocity,on="product_id",how="left").merge(products[["product_id","product_name","category","unit_cost"]],on="product_id",how="left")
    r["units_per_day"]=r.units_per_day.fillna(0);r["lead_time_demand"]=r.units_per_day*r.lead_time
    r["suggested_reorder_qty"]=(r.lead_time_demand+r.reorder_level-r.stock_quantity).clip(lower=0).round().astype(int)
    r["review_flag"]=r.stock_quantity<=r.reorder_level;r["estimated_order_cost"]=r.suggested_reorder_qty*r.unit_cost;r["sales_window_days"]=span
    return r.sort_values(["review_flag","suggested_reorder_qty"],ascending=[False,False])
