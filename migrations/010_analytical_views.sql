-- =============================================================================
-- NovaCommerce Analytical Materialized Views & Operational Reporting Queries
-- =============================================================================

-- Daily Sales Performance View
CREATE OR REPLACE VIEW view_daily_sales_performance AS
SELECT
    DATE(created_at) AS sales_date,
    currency,
    COUNT(*) AS total_orders_count,
    COUNT(*) FILTER (WHERE status = 'DELIVERED') AS delivered_orders_count,
    COUNT(*) FILTER (WHERE status = 'CANCELLED') AS cancelled_orders_count,
    SUM(subtotal_cents) AS gross_subtotal_cents,
    SUM(tax_cents) AS total_tax_collected_cents,
    SUM(shipping_cents) AS total_shipping_billed_cents,
    SUM(discount_cents) AS total_promotions_applied_cents,
    SUM(total_cents) AS net_revenue_settled_cents,
    ROUND(AVG(total_cents)) AS average_order_value_cents
FROM orders
GROUP BY DATE(created_at), currency
ORDER BY sales_date DESC;

-- Warehouse Inventory Health & Stockout Risk View
CREATE OR REPLACE VIEW view_inventory_stockout_risk AS
SELECT
    s.sku,
    w.code AS warehouse_code,
    w.name AS warehouse_name,
    s.on_hand_quantity,
    s.reserved_quantity,
    (s.on_hand_quantity - s.reserved_quantity) AS available_quantity,
    s.safety_stock_threshold,
    s.reorder_quantity,
    CASE
        WHEN (s.on_hand_quantity - s.reserved_quantity) <= 0 THEN 'CRITICAL_STOCKOUT'
        WHEN (s.on_hand_quantity - s.reserved_quantity) <= s.safety_stock_threshold THEN 'LOW_STOCK_WARNING'
        ELSE 'OPTIMAL_LEVEL'
    END AS stock_health_status,
    s.updated_at AS last_inventory_mutation_at
FROM inventory_stocks s
JOIN warehouses w ON s.warehouse_id = w.id
ORDER BY available_quantity ASC;

-- Financial Ledger Trial Balance Verification View
CREATE OR REPLACE VIEW view_financial_trial_balance AS
SELECT
    a.account_number,
    a.name AS account_name,
    a.type AS account_category,
    a.currency,
    COALESCE(SUM(CASE WHEN l.entry_type = 'DEBIT' THEN l.amount_cents ELSE 0 END), 0) AS total_debits_cents,
    COALESCE(SUM(CASE WHEN l.entry_type = 'CREDIT' THEN l.amount_cents ELSE 0 END), 0) AS total_credits_cents,
    (
        COALESCE(SUM(CASE WHEN l.entry_type = 'DEBIT' THEN l.amount_cents ELSE 0 END), 0) -
        COALESCE(SUM(CASE WHEN l.entry_type = 'CREDIT' THEN l.amount_cents ELSE 0 END), 0)
    ) AS net_balance_cents
FROM ledger_accounts a
LEFT JOIN ledger_lines l ON a.id = l.account_id
GROUP BY a.account_number, a.name, a.type, a.currency
ORDER BY a.account_number ASC;
