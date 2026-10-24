SELECT
    COUNT(*) AS rejected_count
FROM {{ ref('orders_rejected') }}
HAVING COUNT(*) * 1.0 / (
    SELECT COUNT(*) FROM {{ ref('int_orders_checked') }}
) >= 0.20