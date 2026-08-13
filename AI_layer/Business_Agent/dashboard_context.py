import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

# dashboard_context.py

DASHBOARD_CONTEXT = {

    "executive": {

        "title": "Executive Overview",

        "primary_view":
            "vw_executive_dashboard",

        "supporting_views": [
            "vw_kpi_summary"
        ]
    },

    "customer": {

        "title": "Customer Intelligence",

        "primary_view":
            "vw_customer_intelligence",

        "supporting_views": [
            "vw_ai_customer_recommendations"
        ]
    },

    "product": {

        "title": "Product Intelligence",

        "primary_view":
            "vw_product_intelligence",

        "supporting_views": [
            "vw_product_performance",
            "vw_category_performance"
        ]
    },

    "revenue": {

        "title": "Revenue Intelligence",

        "primary_view":
            "vw_revenue_intelligence",

        "supporting_views": [
            "vw_revenue_growth"
        ]
    },

    "geographic": {

        "title": "Geographic Intelligence",

        "primary_view":
            "vw_geographic_intelligence",

        "supporting_views": []
    },

    "sales": {

        "title": "Sales Performance",

        "primary_view":
            "vw_sales_performance",

        "supporting_views": []
    },

    "ml": {

        "title": "ML Insights",

        "primary_view":
            "vw_ml_insights",

        "supporting_views": []
    },

    "opportunity": {

        "title": "Opportunity Center",

        "primary_view":
            "vw_opportunity_center",

        "supporting_views": []
    }
}