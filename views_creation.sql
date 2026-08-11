select * from customer_features
select * from validation_report
select * from revenue_forecasts
select * from model_metrics

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public';

SELECT column_name
FROM information_schema.columns
WHERE table_name = 'revenue_opportunity_summary';

-- CREATING VIEWS TO MAKE A POWER BI DASHBOARDS 
-- RATHER THAN CREATING A 20 SMALL VIEWS WE ARE CREATING JUST 8 BUSINESS VIEWS 

-- 1] EXECUTIVE DASHBOARD VIEWS 
CREATE OR REPLACE VIEW vw_executive_dashboard AS
SELECT
    COUNT(DISTINCT c.customer_unique_id) AS total_customers,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(p.payment_value) AS total_revenue,
    ROUND(
        (
            SUM(p.payment_value) /
            NULLIF(COUNT(DISTINCT o.order_id), 0)
        )::numeric,
        2
    ) AS avg_order_value,
    COUNT(DISTINCT s.seller_id) AS total_sellers
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN payments p
    ON o.order_id = p.order_id
JOIN order_items oi
    ON o.order_id = oi.order_id
JOIN sellers s
    ON oi.seller_id = s.seller_id;



	-- 2] REVENUE INTELLIGENCE VIEW

	CREATE OR REPLACE VIEW vw_revenue_intelligence AS
SELECT
    DATE_TRUNC(
        'month',
        o.order_purchase_timestamp::timestamp
    ) AS month,

    COUNT(DISTINCT o.order_id) AS orders,

    SUM(p.payment_value) AS revenue,

    ROUND(
        AVG(p.payment_value)::numeric,
        2
    ) AS avg_order_value

FROM orders o
JOIN payments p
    ON o.order_id = p.order_id

GROUP BY 1
ORDER BY 1;


	-- 3] PRODUCT INTELLIGECE VIEW
	CREATE OR REPLACE VIEW vw_product_intelligence AS
SELECT

    COALESCE(
        ct.product_category_name_english,
        pr.product_category_name
    ) AS category,

    COUNT(*) AS items_sold,

    SUM(
        p.payment_value
    ) AS revenue

FROM order_items oi

JOIN products pr
ON oi.product_id = pr.product_id

JOIN orders o
ON oi.order_id = o.order_id

JOIN payments p
ON o.order_id = p.order_id

LEFT JOIN category_translation ct
ON pr.product_category_name =
   ct.product_category_name

GROUP BY 1;



-- 4] CUSTOMER INTELLIGENCE VIEW
CREATE OR REPLACE VIEW vw_customer_intelligence AS
SELECT

    cs.customer_unique_id,

    cs.segment_name,

    ros.total_revenue,

    ros.total_orders,

    ros.avg_order_value,

    ros.customer_lifetime_days,

    ros.recency_days,

    ros.customer_value_score,

    ros.opportunity_level

FROM customer_segments cs

LEFT JOIN revenue_opportunity_scores ros
ON cs.customer_unique_id =
   ros.customer_unique_id;


   -- 5] GEOGRAPHIC INTELLIGENCE VIEW
CREATE OR REPLACE VIEW vw_geographic_intelligence AS
SELECT

    c.customer_state,

    c.customer_city,

    COUNT(
        DISTINCT c.customer_unique_id
    ) AS customers,

    SUM(
        p.payment_value
    ) AS revenue

FROM customers c

JOIN orders o
ON c.customer_id = o.customer_id

JOIN payments p
ON o.order_id = p.order_id

GROUP BY
c.customer_state,
c.customer_city;


-- 6] SALES PERFORMANCE VIEW
CREATE OR REPLACE VIEW vw_sales_performance AS
SELECT

    DATE(
        o.order_purchase_timestamp
    ) AS sales_date,

    COUNT(
        DISTINCT o.order_id
    ) AS total_orders,

    SUM(
        p.payment_value
    ) AS revenue

FROM orders o

JOIN payments p
ON o.order_id = p.order_id

GROUP BY 1

ORDER BY 1;


-- 7] ML INSIGHTS VIEW
CREATE OR REPLACE VIEW vw_ml_insights AS
SELECT
    cs.customer_unique_id,
    cs.segment_name,
    pp.purchase_probability,
    rf.actual_revenue,
    rf.predicted_revenue,

    ROUND(
        (
            rf.predicted_revenue -
            rf.actual_revenue
        )::numeric,
        2
    ) AS forecast_gap

FROM customer_segments cs

LEFT JOIN purchase_predictions pp
    ON cs.customer_unique_id =
       pp.customer_unique_id

LEFT JOIN revenue_forecasts rf
    ON cs.customer_unique_id =
       rf.customer_unique_id;


	   -- 8] OPPORTUNITY CENTER VIEW 
	   CREATE OR REPLACE VIEW vw_opportunity_center AS
SELECT

    customer_unique_id,

    segment_name,

    opportunity_level,

    total_revenue,

    total_orders,

    avg_order_value,

    purchase_probability,

    revenue_opportunity_score,

    customer_value_score,

    repeat_customer,
	recency_days,
customer_lifetime_days,
avg_review_score,
revenue_per_day,
freight_percentage

FROM revenue_opportunity_scores;



-- MASTER AI VIEW  creating this view to feed ai chatbot , recommendation engine, executive ai card and website assitant
CREATE OR REPLACE VIEW vw_ai_customer_recommendations AS
SELECT
    customer_unique_id,
    segment_name,
    opportunity_level,
    total_revenue,
    total_orders,
    avg_order_value,
    purchase_probability,
    revenue_opportunity_score,
    customer_value_score,
    recency_days,
    customer_lifetime_days,
    avg_review_score,
    revenue_per_day,
    repeat_customer
FROM revenue_opportunity_scores;



-- 	KPI SUMMARY VIEW 
CREATE OR REPLACE VIEW vw_kpi_summary AS
SELECT

COUNT(DISTINCT customer_unique_id) AS total_customers,

SUM(total_revenue) AS total_revenue,

AVG(avg_order_value) AS avg_order_value,

AVG(purchase_probability) AS avg_purchase_probability,

AVG(revenue_opportunity_score) AS avg_opportunity_score

FROM revenue_opportunity_scores;



-- CHECKING ALL THE VIEWS
SELECT
    schemaname,
    viewname
FROM pg_views
WHERE schemaname = 'public'
ORDER BY viewname;



-- CREATING NEW REVENUE GROWTH VIEW
CREATE OR REPLACE VIEW vw_revenue_growth AS
SELECT
    month,
    revenue,
    orders,
    avg_order_value,
    previous_revenue,

    ROUND(
        (
            (revenue - previous_revenue)
            / NULLIF(previous_revenue, 0)
            * 100
        )::numeric,
        2
    ) AS revenue_growth_pct

FROM (
    SELECT
        month,
        revenue,
        orders,
        avg_order_value,
        LAG(revenue) OVER (
            ORDER BY month
        ) AS previous_revenue
    FROM vw_revenue_intelligence
) t;







SELECT *
FROM vw_executive_dashboard
LIMIT 5;

SELECT *
FROM vw_kpi_summary;


SELECT COUNT(*) FROM vw_revenue_intelligence;
SELECT COUNT(*) FROM vw_ml_insights;
SELECT COUNT(*) FROM vw_opportunity_center;
SELECT COUNT(*) FROM vw_customer_intelligence;
SELECT COUNT(*) FROM vw_product_intelligence;
SELECT COUNT(*) FROM vw_geographic_intelligence;
SELECT COUNT(*) FROM vw_sales_performance;
SELECT COUNT(*) FROM vw_ai_customer_recommendations;


SELECT * FROM vw_revenue_intelligence LIMIT 1;
SELECT * FROM vw_ml_insights LIMIT 1;
SELECT * FROM vw_opportunity_center LIMIT 1;


SELECT count(*) 
FROM vw_revenue_intelligence;

SELECT
    MIN(month) AS start_month,
    MAX(month) AS end_month,
    COUNT(*) AS total_months
FROM vw_revenue_intelligence;



-- fixing the REVENUE INTELLIGENCE VIEW
CREATE OR REPLACE VIEW vw_revenue_intelligence AS
SELECT
    DATE_TRUNC('month', last_purchase) AS month,
    COUNT(customer_unique_id) AS orders,
    SUM(total_revenue) AS revenue,
    ROUND(AVG(avg_order_value)::numeric,2) AS avg_order_value
FROM revenue_opportunity_scores
GROUP BY 1
ORDER BY 1;


SELECT SUM(revenue)
FROM vw_revenue_intelligence;


-- updating executive dashboard views
DROP VIEW IF EXISTS vw_executive_dashboard;

CREATE VIEW vw_executive_dashboard AS

SELECT
    COUNT(DISTINCT customer_unique_id) AS total_customers,

    SUM(total_orders) AS total_orders,

    SUM(total_revenue) AS total_revenue,

    ROUND(
        (
            SUM(total_revenue)
            /
            NULLIF(SUM(total_orders),0)
        )::numeric,
        2
    ) AS avg_order_value,

    (
        SELECT COUNT(*)
        FROM sellers
    ) AS total_sellers

FROM revenue_opportunity_scores;



-- updating product intelligence view
DROP VIEW IF EXISTS vw_product_intelligence;

CREATE VIEW vw_product_intelligence AS

SELECT
    COALESCE(
        ct.product_category_name_english,
        pr.product_category_name
    ) AS category,

    COUNT(*) AS items_sold,

    ROUND(
        SUM(
            oi.price + oi.freight_value
        )::numeric,
        2
    ) AS revenue

FROM order_items oi

JOIN products pr
    ON oi.product_id = pr.product_id

LEFT JOIN category_translation ct
    ON pr.product_category_name =
       ct.product_category_name

GROUP BY
    COALESCE(
        ct.product_category_name_english,
        pr.product_category_name
    );


-- -- updating product performance view
DROP VIEW IF EXISTS vw_product_performance;

CREATE VIEW vw_product_performance AS

SELECT

    p.product_id,

    COALESCE(
        ct.product_category_name_english,
        p.product_category_name
    ) AS category,

    COUNT(DISTINCT oi.order_id) AS total_orders,

    COUNT(*) AS items_sold,

    ROUND(
        SUM(oi.price)::numeric,
        2
    ) AS product_revenue,

    ROUND(
        AVG(oi.price)::numeric,
        2
    ) AS avg_product_price,

    ROUND(
        SUM(oi.freight_value)::numeric,
        2
    ) AS freight_revenue

FROM products p

JOIN order_items oi
    ON p.product_id = oi.product_id

LEFT JOIN category_translation ct
    ON p.product_category_name =
       ct.product_category_name

GROUP BY
    p.product_id,
    COALESCE(
        ct.product_category_name_english,
        p.product_category_name
    );






	-- creating view for category performance of product 
	CREATE OR REPLACE VIEW vw_category_performance AS
SELECT

    pct.product_category_name_english AS category,

    COUNT(DISTINCT oi.product_id) AS total_products,

    COUNT(DISTINCT oi.order_id) AS total_orders,

    SUM(oi.price) AS total_revenue,

    AVG(oi.price) AS avg_price

FROM order_items oi

JOIN products p
ON oi.product_id = p.product_id

LEFT JOIN category_translation pct
ON p.product_category_name = pct.product_category_name

GROUP BY
    pct.product_category_name_english;


SELECT column_name
FROM information_schema.columns
WHERE table_name = 'revenue_opportunity_scores'
ORDER BY ordinal_position;
select * from revenue_opportunity_scores

-- updating ai customer recommendaiton 
DROP VIEW IF EXISTS vw_ai_customer_recommendations;

CREATE VIEW vw_ai_customer_recommendations AS
SELECT
    customer_unique_id,
    segment_name,
    opportunity_level,
    total_revenue,
    total_orders,
    avg_order_value,
    purchase_probability,
    revenue_opportunity_score,
    customer_value_score,
    last_purchase,
    customer_lifetime_days,
    recency_days,
    revenue_per_day,
    avg_review_score,
    review_category,
    repeat_customer,
    "R_score" AS r_score,
    "F_score" AS f_score,
    "M_score" AS m_score,
    "RFM_score" AS rfm_score
FROM revenue_opportunity_scores;

	

-- updating kpi summry 
DROP VIEW IF EXISTS vw_kpi_summary;

CREATE VIEW vw_kpi_summary AS
SELECT
    COUNT(DISTINCT customer_unique_id) AS total_customers,

    SUM(total_revenue) AS total_revenue,

    ROUND(
        AVG(avg_order_value)::numeric,
        2
    ) AS avg_order_value,

    ROUND(
        AVG(purchase_probability)::numeric,
        4
    ) AS avg_purchase_probability,

    ROUND(
        AVG(revenue_opportunity_score)::numeric,
        2
    ) AS avg_opportunity_score,

    MAX(revenue_opportunity_score) AS max_opportunity_score,

    MIN(revenue_opportunity_score) AS min_opportunity_score

FROM revenue_opportunity_scores;






SELECT
    SUM(payment_value) AS total_revenue
FROM payments;

SELECT
    SUM(total_revenue) AS total_revenue
FROM vw_customer_intelligence;

SELECT
    SUM(total_revenue) AS total_revenue
FROM vw_opportunity_center;

SELECT
    SUM(revenue) AS total_revenue
FROM vw_revenue_intelligence;



SELECT
    COUNT(*) AS rows_count,
    COUNT(DISTINCT customer_unique_id) AS distinct_customers
FROM vw_customer_intelligence;



SELECT definition
FROM pg_views
WHERE viewname = 'vw_customer_intelligence';

SELECT definition
FROM pg_views
WHERE viewname = 'vw_opportunity_center';



SELECT COUNT(*) FROM payments;

SELECT ROUND(SUM(payment_value)::numeric,2) FROM payments;

SELECT COUNT(*) 
FROM payments p
LEFT JOIN orders o
ON p.order_id = o.order_id
WHERE o.order_id IS NULL;

SELECT SUM(price)
FROM order_items;





SELECT
    SUM(total_revenue)
FROM vw_customer_intelligence;

SELECT COUNT(DISTINCT customer_unique_id)
FROM revenue_opportunity_scores;

SELECT
    SUM(total_revenue)
FROM revenue_opportunity_scores;

SELECT
    SUM(total_revenue)
FROM vw_customer_intelligence;


SELECT definition
FROM pg_views
WHERE viewname = 'vw_executive_dashboard';

SELECT definition
FROM pg_views
WHERE viewname = 'vw_product_intelligence';

SELECT definition
FROM pg_views
WHERE viewname = 'vw_product_performance';