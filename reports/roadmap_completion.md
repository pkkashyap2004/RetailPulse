# RetailPulse roadmap completion

## Audit findings
Day 1 EDA findings, Day 2 preprocessing and four processed files, and Day 3 notebook/report/figures are present. Day 4–5 source folders and subsequent forecast, inventory, churn, test, dashboard and orchestration folders were placeholders. Earlier analyses were not re-run in this increment.

## Added capabilities
- Day 4: transaction calendar and product performance features.
- Days 5–6: snapshot RFM metrics and readable rule-based segments.
- Days 7–9: monthly naive baseline with chronological three-month holdout, MAE and MAPE.
- Days 10–11: latest inventory snapshot, observed sales velocity and reorder review.
- Days 14–15: product/category metrics.
- Days 16–18: local Streamlit KPI and inventory dashboard.
- Days 19–20: focused unit tests.
- Days 21–30: one-command pipeline and setup, limitations and review guidance.

## Boundaries
Predictive churn is not supported: the available snapshot does not establish an observation window, churn definition or defensible labels. Forecast history is short and the latest October 2026 period may be partial. Inventory estimates omit purchase orders, stockout censoring, seasonality and explicit safety-stock policy. RFM tiers are relative to this file, not lifetime customer status. No output metrics are claimed until the pipeline is run.

Run from the repository root: python src/run_pipeline.py; pytest; streamlit run dashboard/app.py. Raw files are inputs only; derived outputs go in data/processed/.
