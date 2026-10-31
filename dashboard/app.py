"""Local Streamlit view of RetailPulse metrics."""
from pathlib import Path
import pandas as pd
import streamlit as st
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/"data/processed"
st.set_page_config(page_title="RetailPulse",layout="wide");st.title("RetailPulse | Retail performance")
s=pd.read_csv(DATA/"sales_clean.csv",parse_dates=["date"]);p=pd.read_csv(DATA/"products_clean.csv");i=pd.read_csv(DATA/"inventory_clean.csv",parse_dates=["date"])
period=st.date_input("Sales date range",(s.date.min().date(),s.date.max().date()))
v=s[s.date.ge(pd.Timestamp(period[0]))&s.date.lt(pd.Timestamp(period[-1])+pd.Timedelta(days=1))]
a,b,c=st.columns(3);a.metric("Net recorded sales",f"₹{v.total_amount.sum():,.0f}");b.metric("Transactions",f"{v.transaction_id.nunique():,}");c.metric("Units",f"{v.quantity.sum():,.0f}")
st.subheader("Monthly sales");st.line_chart(v.set_index("date").resample("MS").total_amount.sum())
st.subheader("Category performance");st.bar_chart(v.merge(p[["product_id","category"]],on="product_id").groupby("category").total_amount.sum().sort_values(ascending=False))
st.subheader("Below reorder level");latest=i.sort_values("date").groupby("product_id").tail(1);st.dataframe(latest[latest.stock_quantity<=latest.reorder_level].merge(p[["product_id","product_name","category"]],on="product_id"),use_container_width=True)
st.caption("RFM is snapshot-relative. Forecast and inventory suggestions are educational planning estimates.")
