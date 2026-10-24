SELECT
    order_id,
    order_date,
    customer_id,
    country,
    product,
    quantity,
    unit_price,
    quantity * unit_price AS total_amount
FROM {{ ref('int_orders_checked') }}
WHERE reject_reason IS NULL