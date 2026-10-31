import pandas as pd
from src.segmentation.customer_segmentation import build_rfm
from src.forecasting.forecast_sales import evaluate_baseline
from src.inventory.reorder_analysis import build_reorder_review
def test_rfm_metrics():
 s=pd.DataFrame({"customer_id":["a","a","b"],"transaction_id":["1","2","3"],"date":["2025-01-01","2025-01-05","2025-01-03"],"total_amount":[10,20,5]})
 r=build_rfm(s,"2025-01-06").set_index("customer_id")
 assert r.loc["a","recency_days"]==1 and r.loc["a","frequency"]==2 and r.loc["a","monetary"]==30
def test_forecast_temporal_holdout():
 s=pd.DataFrame({"date":pd.date_range("2025-01-01",periods=6,freq="MS"),"total_amount":[10,12,14,16,18,20]})
 tr,te,m=evaluate_baseline(s,2)
 assert tr.index.max()<te.index.min() and list(te.forecast)==[16,16] and m["observations"]==6
def test_reorder_latest_snapshot():
 s=pd.DataFrame({"product_id":["p","p"],"date":["2025-01-01","2025-01-11"],"quantity":[10,10]})
 i=pd.DataFrame({"product_id":["p","p"],"date":["2025-01-01","2025-01-10"],"stock_quantity":[100,2],"reorder_level":[5,5],"lead_time":[2,2]})
 p=pd.DataFrame({"product_id":["p"],"product_name":["item"],"category":["x"],"unit_cost":[3]})
 r=build_reorder_review(s,i,p).iloc[0]
 assert r.stock_quantity==2 and r.review_flag and r.suggested_reorder_qty>=0
