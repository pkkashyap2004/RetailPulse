"""Generate analytics outputs from processed inputs only."""
from pathlib import Path
import json
import pandas as pd
from features.build_features import build_features
from segmentation.customer_segmentation import build_rfm
from forecasting.forecast_sales import evaluate_baseline
from inventory.reorder_analysis import build_reorder_review
ROOT=Path(__file__).resolve().parents[1];DATA=ROOT/"data/processed"
def run():
    d=build_features(DATA)
    for n,f in d.items():f.to_csv(DATA/f"{n}_features.csv" if n=="sales" else DATA/f"{n}.csv",index=False)
    s=d["sales"];build_rfm(s).to_csv(DATA/"customer_segments.csv",index=False)
    build_reorder_review(s,pd.read_csv(DATA/"inventory_clean.csv"),pd.read_csv(DATA/"products_clean.csv")).to_csv(DATA/"reorder_review.csv",index=False)
    _,h,m=evaluate_baseline(s);h.reset_index().to_csv(DATA/"sales_forecast_holdout.csv",index=False)
    (DATA/"forecast_metrics.json").write_text(json.dumps(m,indent=2));return m
if __name__=="__main__":print(json.dumps(run(),indent=2))
