# RetailPulse

AI-powered retail analytics platform for customer intelligence, demand forecasting, churn prediction, and inventory optimization.

## Project Status

🚧 Day 1 — Repository and project foundation initialized.

## Architecture

- **data/** — raw, processed, and external datasets
- **notebooks/** — exploratory analysis and experiments
- **src/** — production data, feature, modeling, forecasting, segmentation, churn, and inventory code
- **dashboard/** — analytics dashboard
- **tests/** — automated tests
- **reports/** — data dictionaries, EDA, and project reports
- **monitoring/** — model and data monitoring
- **airflow/** — workflow orchestration
- **k8s/** — Kubernetes deployment manifests
- **models/** — model artifacts (large/generated artifacts should not be committed)

## Planned Capabilities

1. Retail sales and customer EDA
2. Customer segmentation
3. Demand forecasting
4. Churn prediction
5. Inventory optimization
6. Interactive dashboard
7. ML experiment tracking and monitoring
8. Production deployment

## Development

Python 3.11 is the target runtime. Keep raw datasets immutable and place generated/processed data in the appropriate data directories.
