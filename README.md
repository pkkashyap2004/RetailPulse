# RetailPulse

Retail analytics using the committed sample data. Existing Days 1–3 artifacts include EDA, preprocessing, processed CSVs, figures and reports. This increment adds feature generation, snapshot RFM, a time-aware monthly baseline, inventory review, tests and a local Streamlit dashboard. See reports/roadmap_completion.md and reports/data_dictionary.md.

## Quick start

Use Python 3.11. Create and activate a virtual environment, install requirements.txt, then run from the repository root: python src/run_pipeline.py; pytest; streamlit run dashboard/app.py.

The pipeline reads data/processed/*_clean.csv and writes derived files under data/processed/. Keep data/raw/ immutable.

## Generated outputs

sales_features.csv, product_features.csv, daily_sales_features.csv, monthly_sales_features.csv, customer_segments.csv, sales_forecast_holdout.csv, forecast_metrics.json and reorder_review.csv.

## Limitations

Forecasting is a baseline demonstration on a small irregular history; the final 2026 month may be partial. Inventory review uses one latest stock snapshot and observed average velocity, with no purchase orders, safety stock policy or stockout correction. RFM tiers are relative to the transaction snapshot. Predictive churn requires defensible labels and observation windows and is not implemented. Catalog margin is not realized transaction profit. Validate assumptions and data governance before production use.
