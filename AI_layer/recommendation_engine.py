from db import DatabaseManager


class RecommendationEngine:

    def __init__(self):
        self.db = DatabaseManager()
        self.db.connect()

    def close(self):
        self.db.disconnect()

    # =====================================================
    # EXECUTIVE DASHBOARD
    # =====================================================

    def generate_executive_recommendations(self):

        df = self.db.get_view_data(
            "vw_executive_dashboard"
        )

        row = df.iloc[0]

        recommendations = []

        if row["avg_order_value"] < 250:

            recommendations.append({
                "priority": "High",
                "title": "Increase Average Order Value",
                "recommendation": "Launch bundle offers and upselling campaigns.",
                "expected_impact": "Higher revenue per order."
            })

        recommendations.append({
            "priority": "Medium",
            "title": "Seller Expansion",
            "recommendation": "Recruit additional sellers in top-performing categories.",
            "expected_impact": "Broader product selection and revenue growth."
        })

        return recommendations

    # =====================================================
    # CUSTOMER DASHBOARD
    # =====================================================

    def generate_customer_recommendations(self):

        df = self.db.get_view_data(
            "vw_customer_intelligence"
        )

        top_segment = (
            df["segment_name"]
            .value_counts()
            .idxmax()
        )

        recommendations = [

            {
                "priority": "High",
                "title": "Target Largest Customer Segment",
                "recommendation": f"Create campaigns for '{top_segment}' customers.",
                "expected_impact": "Improved retention and repeat purchases."
            },

            {
                "priority": "Medium",
                "title": "Customer Loyalty Program",
                "recommendation": "Reward repeat customers with exclusive benefits.",
                "expected_impact": "Higher customer lifetime value."
            }

        ]

        return recommendations

    # =====================================================
    # PRODUCT DASHBOARD
    # =====================================================

    def generate_product_recommendations(self):

        df = self.db.get_view_data(
            "vw_product_intelligence"
        )

        top_category = (
            df.sort_values(
                "revenue",
                ascending=False
            )
            .iloc[0]["category"]
        )

        recommendations = [

            {
                "priority": "High",
                "title": "Promote Top Category",
                "recommendation": f"Increase marketing for '{top_category}'.",
                "expected_impact": "Revenue growth from proven products."
            },

            {
                "priority": "Medium",
                "title": "Optimize Low Performing Categories",
                "recommendation": "Review pricing and visibility of weak categories.",
                "expected_impact": "Improved category contribution."
            }

        ]

        return recommendations

    # =====================================================
    # REVENUE DASHBOARD
    # =====================================================

    def generate_revenue_recommendations(self):

        growth_df = self.db.get_view_data(
            "vw_revenue_growth"
        )

        latest_growth = (
            growth_df["revenue_growth_pct"]
            .dropna()
        )

        latest_growth = (
            latest_growth.iloc[-1]
            if not latest_growth.empty
            else 0
        )

        recommendations = []

        if latest_growth < 0:

            recommendations.append({

                "priority": "High",

                "title": "Revenue Decline Detected",

                "recommendation":
                    "Launch customer retention and reactivation campaigns.",

                "expected_impact":
                    "Reduce revenue loss and improve repeat purchases."
            })

        else:

            recommendations.append({

                "priority": "Medium",

                "title": "Scale Growth",

                "recommendation":
                    "Increase investment in high-performing channels.",

                "expected_impact":
                    "Accelerate revenue growth."
            })

        return recommendations

    # =====================================================
    # GEOGRAPHIC DASHBOARD
    # =====================================================

    def generate_geographic_recommendations(self):

        df = self.db.get_view_data(
            "vw_geographic_intelligence"
        )

        top_state = (
            df.groupby("customer_state")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .idxmax()
        )

        recommendations = [

            {
                "priority": "High",
                "title": "Expand in Top Region",
                "recommendation": f"Increase marketing efforts in {top_state}.",
                "expected_impact": "Higher regional revenue."
            },

            {
                "priority": "Medium",
                "title": "Regional Expansion",
                "recommendation": "Identify underpenetrated states.",
                "expected_impact": "New customer acquisition."
            }

        ]

        return recommendations

    # =====================================================
    # SALES DASHBOARD
    # =====================================================

    def generate_sales_recommendations(self):

        recommendations = [

            {
                "priority": "High",
                "title": "Sales Seasonality Planning",
                "recommendation": "Increase inventory before peak periods.",
                "expected_impact": "Avoid stockouts and lost revenue."
            },

            {
                "priority": "Medium",
                "title": "Low Sales Day Promotions",
                "recommendation": "Run targeted offers during weak periods.",
                "expected_impact": "Improve daily sales consistency."
            }

        ]

        return recommendations

    # =====================================================
    # ML DASHBOARD
    # =====================================================

    def generate_ml_recommendations(self):

        df = self.db.get_view_data(
            "vw_ml_insights"
        )

        high_probability = len(
            df[df["purchase_probability"] >= 0.95]
        )

        recommendations = [

            {
                "priority": "High",
                "title": "Target High Intent Customers",
                "recommendation":
                    f"Focus campaigns on {high_probability:,} high-intent customers.",
                "expected_impact":
                    "Increase conversion and revenue."
            },

            {
                "priority": "Medium",
                "title": "Model Monitoring",
                "recommendation":
                    "Track prediction accuracy regularly.",
                "expected_impact":
                    "Improve forecasting reliability."
            }

        ]

        return recommendations

    # =====================================================
    # OPPORTUNITY CENTER
    # =====================================================

    def generate_opportunity_recommendations(self):

        df = self.db.get_view_data(
            "vw_opportunity_center"
        )

        high_opportunity = len(
            df[df["opportunity_level"] == "High"]
        )

        recommendations = [

            {
                "priority": "High",
                "title": "Immediate Revenue Opportunity",
                "recommendation":
                    f"Target {high_opportunity:,} high-opportunity customers.",
                "expected_impact":
                    "Maximize near-term revenue growth."
            },

            {
                "priority": "High",
                "title": "Cross Sell Campaign",
                "recommendation":
                    "Recommend complementary products to repeat customers.",
                "expected_impact":
                    "Increase basket size and revenue."
            }

        ]

        return recommendations

    # =====================================================
    # ROUTER
    # =====================================================

    def generate(self, dashboard_name):

        dashboard_map = {

            "executive":
                self.generate_executive_recommendations,

            "customer":
                self.generate_customer_recommendations,

            "product":
                self.generate_product_recommendations,

            "revenue":
                self.generate_revenue_recommendations,

            "geographic":
                self.generate_geographic_recommendations,

            "sales":
                self.generate_sales_recommendations,

            "ml":
                self.generate_ml_recommendations,

            "opportunity":
                self.generate_opportunity_recommendations
        }

        dashboard_name = dashboard_name.lower()

        if dashboard_name not in dashboard_map:

            return [

                {
                    "priority": "Info",
                    "title": "No Recommendation",
                    "recommendation":
                        f"No recommendation available for {dashboard_name}",
                    "expected_impact":
                        "-"
                }

            ]

        return dashboard_map[dashboard_name]()