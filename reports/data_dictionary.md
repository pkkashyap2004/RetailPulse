# RetailPulse Data Dictionary — Day 1

## sales.csv
| Column | Meaning |
|---|---|
| transaction_id | Unique transaction identifier |
| customer_id | Customer identifier linked to customers.csv |
| product_id | Product identifier linked to products.csv |
| date | Transaction date |
| quantity | Units sold |
| unit_price | Transaction unit price |
| discount | Discount percentage |
| total_amount | Recorded transaction total |

## customers.csv
| Column | Meaning |
|---|---|
| customer_id | Customer identifier |
| customer_name | Customer name |
| age | Customer age |
| gender | Customer gender |
| city | Customer city |
| registration_date | Customer registration date |

## products.csv
| Column | Meaning |
|---|---|
| product_id | Product identifier |
| product_name | Product name |
| category | Product category |
| unit_cost | Product cost |
| selling_price | Product selling price |

## inventory.csv
| Column | Meaning |
|---|---|
| index | Source row/index identifier |
| product_id | Product identifier linked to products.csv |
| date | Inventory observation date |
| stock_quantity | Available stock quantity |
| reorder_level | Stock threshold for reorder |
| lead_time | Lead time associated with replenishment |

## Day 1 derived metrics
- Gross amount = quantity × unit_price
- Discount amount = gross amount × discount / 100
- Calculated total = gross amount − discount amount
- Unit margin = selling_price − unit_cost
- Margin % = unit margin / selling_price × 100
- Stock gap = stock_quantity − reorder_level
- Below reorder = stock_quantity < reorder_level
