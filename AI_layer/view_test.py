from db import DatabaseManager

views = [

    "vw_ai_customer_recommendations",
    "vw_category_performance",
    "vw_customer_intelligence",
    "vw_executive_dashboard",
    "vw_geographic_intelligence",
    "vw_kpi_summary",
    "vw_ml_insights",
    "vw_opportunity_center",
    "vw_product_intelligence",
    "vw_product_performance",
    "vw_revenue_growth",
    "vw_revenue_intelligence",
    "vw_sales_performance"
]

db = DatabaseManager()

db.connect()

for view in views:

    try:

        df = db.get_view_data(view)

        print(f"\n✅ {view}")

        print(df.shape)
        print(df.columns.tolist())
        print(df.head(2))

    except Exception as e:

        print(f"\n❌ {view}")

        print(e)

db.disconnect()


print(df.columns.tolist())