# RetailPulse — Day 1 EDA Findings

**Source:** actual CSV files committed under `data/raw/` in `pkkashyap2004/RetailPulse`.

## Dataset inventory

| Dataset | Rows | Columns | Duplicate rows | Missing cells |
|---|---:|---:|---:|---:|
| sales.csv | 500 | 8 | 0 | 0 |
| customers.csv | 500 | 6 | 0 | 0 |
| products.csv | 500 | 5 | 0 | 0 |
| inventory.csv | 500 | 6 | 0 | 0 |

## Sales findings

- Transaction date range: **2025-01-01 to 2026-10-07**.
- Transactions: **500**.
- Distinct customers appearing in sales: **305**.
- Distinct products appearing in sales: **323**.
- Recorded revenue: **₹12,174,728.26**.
- Quantity sold: **2,792 units**.
- Average transaction value: **₹24,349.46**.
- Average discount: **13.19%**.
- Gross amount before discount: **₹13,968,403.31**.
- Calculated total from quantity × unit price − discount: **₹12,174,728.13**.
- Mean absolute difference between recorded and calculated totals: **₹0.0025**; maximum absolute difference: **₹0.005**. This indicates the stored total is numerically consistent with the supplied transaction fields up to rounding precision.

## Customer key integrity issue

The raw files use different ID formats:

- `sales.csv`: customer IDs such as `C0328`
- `customers.csv`: customer IDs such as `1328`

A direct string join therefore reports **500 unmatched sales customer IDs**. However, a deterministic numeric-offset reconciliation (`C0001 → 1001`, `C0002 → 1002`, etc.) matches **all 500 sales records** to the customer master.

**Day-2 action:** normalize customer IDs in the processed layer rather than modifying the immutable raw files.

## Product integrity

- All sales product IDs matched `products.csv`.
- All inventory product IDs matched `products.csv`.
- No duplicate product IDs were found.

## Inventory findings

- Inventory records: **500**.
- Records below reorder level: **59 (11.80%)**.
- Minimum stock: **1**.
- Maximum stock: **500**.
- Average lead time: **15.36 days**.
- Maximum lead time: **30 days**.

These below-reorder records should become candidates for the inventory optimization workflow.

## Revenue by category

| Category | Revenue |
|---|---:|
| Home & Kitchen | ₹1,924,489.40 |
| Stationery | ₹1,883,535.42 |
| Grocery | ₹1,632,837.93 |
| Sports | ₹1,609,612.08 |
| Beauty | ₹1,512,941.69 |
| Fashion | ₹1,288,599.89 |
| Electronics | ₹1,181,059.29 |
| Personal Care | ₹1,141,652.56 |

**Highest-revenue category:** Home & Kitchen.

## Top products by recorded revenue

| Rank | Product | Revenue |
|---:|---|---:|
| 1 | P0334 — Essential Drawing Book 42 | ₹144,793.10 |
| 2 | P0426 — Essential Lunch Box 54 | ₹143,488.09 |
| 3 | P0198 — Advanced A4 Paper Pack 25 | ₹143,400.58 |
| 4 | P0152 — Pro Blush 19 | ₹122,235.99 |
| 5 | P0174 — Smart A4 Paper Pack 22 | ₹120,253.48 |
| 6 | P0227 — Essential Oats 29 | ₹116,675.89 |
| 7 | P0047 — Eco Gym Gloves 6 | ₹110,967.26 |
| 8 | P0027 — Advanced Toor Dal 4 | ₹108,711.43 |
| 9 | P0459 — Eco Toor Dal 58 | ₹108,405.50 |
| 10 | P0068 — Eco Face Cream 9 | ₹100,174.16 |

## Highest-revenue months

| Month | Revenue |
|---|---:|
| 2025-09 | ₹797,816.80 |
| 2025-04 | ₹756,642.26 |
| 2026-01 | ₹755,088.08 |
| 2026-02 | ₹667,795.35 |
| 2026-09 | ₹657,771.14 |

## Day-1 conclusions

1. The four raw datasets are complete at the row/cell level: no missing cells or duplicate rows were detected.
2. The principal immediate data-quality issue is **customer ID format mismatch**, not missing customer records.
3. Sales totals are internally consistent with quantity, price, and discount to rounding precision.
4. Home & Kitchen is the strongest revenue category in the current sample.
5. Inventory contains **59 below-reorder observations**, which is a direct input for later inventory-risk modeling.
6. The raw layer should remain immutable. Customer-key normalization belongs in `data/processed/` and the transformation should be documented.
