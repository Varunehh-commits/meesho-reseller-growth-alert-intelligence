-- ============================================================
-- PART 1: SQL BUSINESS QUERY ENGINE
-- Meesho Reseller Growth & Alert Intelligence Pipeline
-- ============================================================


-- ============================================================
-- QUERY 1
-- Monthly revenue by category
-- ============================================================

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


-- ============================================================
-- QUERY 2
-- Region-wise total revenue and order count
-- ============================================================

SELECT
    r.region,
    ROUND(SUM(o.quantity * o.unit_price), 2) AS total_revenue,
    COUNT(*) AS n_orders
FROM orders AS o
JOIN resellers AS r
    ON o.reseller_id = r.reseller_id
GROUP BY r.region
ORDER BY total_revenue DESC;


-- ============================================================
-- QUERY 3
-- Top 5 resellers by total spend
-- ============================================================

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


-- ============================================================
-- QUERY 4A
-- Resellers who have never placed an order
-- ============================================================

SELECT
    r.reseller_id,
    r.reseller_name,
    r.region
FROM resellers AS r
LEFT JOIN orders AS o
    ON r.reseller_id = o.reseller_id
WHERE o.order_id IS NULL;


-- ============================================================
-- QUERY 4B
-- Demonstrate COUNT(*) vs COUNT(order_id)
-- for the zero-order reseller
-- ============================================================

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


-- ============================================================
-- QUERY 5
-- June Delivered Average Order Value (AOV)
-- ============================================================

SELECT
    ROUND(
        SUM(quantity * unit_price) * 1.0 / COUNT(*),
        2
    ) AS june_delivered_aov
FROM orders
WHERE month = 'June'
  AND status = 'Delivered';