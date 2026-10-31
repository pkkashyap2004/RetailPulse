"""Snapshot RFM tiers relative to the latest transaction in the source file."""
import pandas as pd
def build_rfm(sales,as_of=None):
    f=sales.copy();f["date"]=pd.to_datetime(f.date)
    as_of=pd.Timestamp(as_of) if as_of is not None else f.date.max()+pd.Timedelta(days=1)
    r=f.groupby("customer_id").agg(last_purchase=("date","max"),frequency=("transaction_id","nunique"),monetary=("total_amount","sum")).reset_index()
    r["recency_days"]=(as_of-r.last_purchase).dt.days
    r["R"]=pd.qcut(r.recency_days.rank(method="first"),5,labels=[5,4,3,2,1]).astype(int)
    for c in ["frequency","monetary"]:r[c+"_score"]=pd.qcut(r[c].rank(method="first"),5,labels=[1,2,3,4,5]).astype(int)
    r["segment"]="Potential Loyalist"
    r.loc[(r.R>=4)&(r.frequency_score>=4)&(r.monetary_score>=4),"segment"]="Champions"
    r.loc[(r.R>=3)&(r.frequency_score>=3),"segment"]="Loyal Customers"
    r.loc[(r.R<=2)&(r.frequency_score>=3),"segment"]="At Risk"
    r.loc[(r.R<=2)&(r.frequency_score<=2),"segment"]="Hibernating"
    return r
