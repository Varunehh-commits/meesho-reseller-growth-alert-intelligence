import csv
import os
import sqlite3


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "data", "meesho_reseller.db")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)
    

# ============================================================
# DATABASE CONNECTION
# ============================================================

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


# ============================================================
# HELPER FUNCTION
# ============================================================

def run_query(query, output_file):
    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    output_path = os.path.join(OUTPUT_DIR, output_file)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columns)
        writer.writerows(rows)

    print(f"Created: {output_path}")
    print(f"Rows: {len(rows)}")
    print()


# ============================================================
# QUERY 1
# Monthly revenue by category
# ============================================================

query_1 = """
SELECT
    month,
    category,
    ROUND(SUM(quantity * unit_price), 2) AS revenue,
    COUNT(*) AS n_orders
FROM orders
GROUP BY month, category
ORDER BY
    CASE month
        WHEN 'April' THEN 1
        WHEN 'May' THEN 2
        WHEN 'June' THEN 3
    END,
    category;
"""

run_query(
    query_1,
    "monthly_category_revenue.csv"
)


# ============================================================
# QUERY 2
# Region-wise total revenue and order count
# ============================================================

query_2 = """
SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
    COUNT(*) AS n_orders
FROM orders AS o
JOIN resellers AS r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;
"""

run_query(
    query_2,
    "region_revenue.csv"
)


# ============================================================
# QUERY 3
# Top 5 resellers by total spend
# ============================================================

query_3 = """
SELECT
    r.reseller_id,
    r.reseller_name,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_spend
FROM orders AS o
JOIN resellers AS r
    ON o.reseller_id = r.reseller_id
GROUP BY
    r.reseller_id,
    r.reseller_name
HAVING total_spend > 50000
ORDER BY total_spend DESC
LIMIT 5;
"""

run_query(
    query_3,
    "top_resellers.csv"
)


# ============================================================
# QUERY 4A
# Resellers who never placed an order
# ============================================================

query_4a = """
SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers AS r
LEFT JOIN orders AS o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;
"""

run_query(
    query_4a,
    "zero_order_resellers.csv"
)


# ============================================================
# QUERY 4B
# COUNT(*) vs COUNT(order_id)
# ============================================================

query_4b = """
SELECT
    r.reseller_id,
    r.reseller_name,
    COUNT(*) AS count_star,
    COUNT(o.order_id) AS count_order_id
FROM resellers AS r
LEFT JOIN orders AS o
    ON r.reseller_id = o.reseller_id
WHERE r.reseller_id = 'RS024'
GROUP BY
    r.reseller_id,
    r.reseller_name;
"""

run_query(
    query_4b,
    "zero_order_count_demo.csv"
)


# ============================================================
# QUERY 5
# June Delivered Average Order Value
# ============================================================

query_5 = """
SELECT
    ROUND(
        SUM(quantity * unit_price) * 1.0 / COUNT(*),
        2
    ) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';
"""

run_query(
    query_5,
    "june_delivered_aov.csv"
)


# ============================================================
# CLOSE DATABASE
# ============================================================

conn.close()

print("Part 1 SQL queries completed successfully.")