"""RetailPulse feature generation."""
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[2]
DATA=ROOT/"data/processed"
def build_features(data_dir=DATA):
    s=pd.read_csv(data_dir/"sales_clean.csv",parse_dates=["date"])
    p=pd.read_csv(data_dir/"products_clean.csv")
    i=pd.read_csv(data_dir/"inventory_clean.csv",parse_dates=["date"])
    s["year"]=s.date.dt.year;s["month"]=s.date.dt.month;s["day_of_week"]=s.date.dt.dayofweek
    s["gross_amount"]=s.quantity*s.unit_price;s["discount_amount"]=s.gross_amount*s.discount/100
    sales=p.merge(s.groupby("product_id",as_index=False).agg(transactions=("transaction_id","nunique"),units_sold=("quantity","sum"),net_revenue=("total_amount","sum")),on="product_id",how="left").fillna({"transactions":0,"units_sold":0,"net_revenue":0})
    sales["unit_margin"]=sales.selling_price-sales.unit_cost
    sales["margin_pct"]=sales.unit_margin.div(sales.selling_price.where(sales.selling_price.ne(0))).mul(100).round(2)
    latest=i.sort_values("date").groupby("product_id").tail(1)
    product=sales.merge(latest,on="product_id",how="left",suffixes=("","_inventory"))
    product["stock_gap"]=product.stock_quantity-product.reorder_level
    product["below_reorder"]=product.stock_gap<0
    daily=s.groupby("date",as_index=False).agg(net_revenue=("total_amount","sum"),units=("quantity","sum"),transactions=("transaction_id","nunique"))
    monthly=s.set_index("date").resample("MS").agg(net_revenue=("total_amount","sum"),units=("quantity","sum"),transactions=("transaction_id","nunique")).reset_index()
    return {"sales":s,"product_features":product,"daily_sales_features":daily,"monthly_sales_features":monthly}
