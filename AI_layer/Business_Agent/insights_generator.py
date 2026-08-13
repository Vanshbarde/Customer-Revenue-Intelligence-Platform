import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from db import DatabaseManager


class InsightsGenerator:

    def __init__(self):
        self.db = DatabaseManager()
        self.db.connect()

    def close(self):
        self.db.disconnect()

    # =====================================================
    # EXECUTIVE DASHBOARD
    # =====================================================

    def generate_executive_insights(self):

        df = self.db.get_view_data("vw_executive_dashboard")
        row = df.iloc[0]

        insights = [

            f"Total revenue crossed ₹{row['total_revenue']:,.2f}.",

            f"Customer base includes {int(row['total_customers']):,} customers.",

            f"Total orders processed reached {int(row['total_orders']):,}.",

            f"Average order value is ₹{row['avg_order_value']:.2f}.",

            f"The platform currently operates with {int(row['total_sellers']):,} sellers."
        ]

        return insights

    # =====================================================
    # CUSTOMER DASHBOARD
    # =====================================================

    def generate_customer_insights(self):

        df = self.db.get_view_data("vw_customer_intelligence")

        total_customers = len(df)

        avg_revenue = df["total_revenue"].mean()

        avg_orders = df["total_orders"].mean()

        top_segment = df["segment_name"].value_counts().idxmax()

        top_segment_count = df["segment_name"].value_counts().max()

        top_opportunity = df["opportunity_level"].value_counts().idxmax()

        insights = [

            f"Customer base contains {total_customers:,} customers.",

            f"Average customer revenue is ₹{avg_revenue:.2f}.",

            f"Customers place an average of {avg_orders:.2f} orders.",

            f"Largest segment is '{top_segment}' with {top_segment_count:,} customers.",

            f"Most customers fall under the '{top_opportunity}' opportunity group."
        ]

        return insights

    # =====================================================
    # PRODUCT DASHBOARD
    # =====================================================

    def generate_product_insights(self):

        df = self.db.get_view_data("vw_product_intelligence")

        top_category = df.sort_values(
            "revenue",
            ascending=False
        ).iloc[0]

        total_revenue = df["revenue"].sum()

        total_items = df["items_sold"].sum()

        insights = [

            f"Product categories generated ₹{total_revenue:,.2f} in revenue.",

            f"Total items sold reached {int(total_items):,}.",

            f"Top category is '{top_category['category']}' generating ₹{top_category['revenue']:,.2f}.",

            f"Top category sold {int(top_category['items_sold']):,} items.",

            "Revenue concentration is driven by a small group of high-performing categories."
        ]

        return insights

    # =====================================================
    # REVENUE DASHBOARD
    # =====================================================

    def generate_revenue_insights(self):

        revenue_df = self.db.get_view_data(
            "vw_revenue_intelligence"
        )

        growth_df = self.db.get_view_data(
            "vw_revenue_growth"
        )

        total_revenue = revenue_df["revenue"].sum()

        avg_order_value = revenue_df[
            "avg_order_value"
        ].mean()

        latest_growth = growth_df[
            "revenue_growth_pct"
        ].dropna()

        latest_growth = (
            latest_growth.iloc[-1]
            if not latest_growth.empty
            else 0
        )

        insights = [

            f"Total revenue reached ₹{total_revenue:,.2f}.",

            f"Average order value stands at ₹{avg_order_value:.2f}.",

            f"Latest monthly growth is {latest_growth:.2f}%.",

            f"Monthly revenue is tracked across {len(revenue_df)} periods."
        ]

        if latest_growth > 0:

            insights.append(
                "Revenue trend remains positive."
            )

        else:

            insights.append(
                "Revenue trend requires attention."
            )

        return insights

    # =====================================================
    # GEOGRAPHIC DASHBOARD
    # =====================================================

    def generate_geographic_insights(self):

        df = self.db.get_view_data(
            "vw_geographic_intelligence"
        )

        top_state = (
            df.groupby("customer_state")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(1)
        )

        top_city = (
            df.groupby("customer_city")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(1)
        )

        insights = [

            f"Geographic revenue totals ₹{df['revenue'].sum():,.2f}.",

            f"Top state is {top_state.index[0]} generating ₹{top_state.iloc[0]:,.2f}.",

            f"Top city is {top_city.index[0]} generating ₹{top_city.iloc[0]:,.2f}.",

            f"Customer presence spans {df['customer_state'].nunique()} states.",

            f"Revenue is distributed across {df['customer_city'].nunique()} cities."
        ]

        return insights

    # =====================================================
    # SALES DASHBOARD
    # =====================================================

    def generate_sales_insights(self):

        df = self.db.get_view_data(
            "vw_sales_performance"
        )

        best_day = df.sort_values(
            "revenue",
            ascending=False
        ).iloc[0]

        insights = [

            f"Total sales revenue reached ₹{df['revenue'].sum():,.2f}.",

            f"Average daily revenue is ₹{df['revenue'].mean():,.2f}.",

            f"Best sales day generated ₹{best_day['revenue']:,.2f}.",

            f"Average daily orders stand at {df['total_orders'].mean():.2f}.",

            f"Sales history contains {len(df):,} daily records."
        ]

        return insights

    # =====================================================
    # ML DASHBOARD
    # =====================================================

    def generate_ml_insights(self):

        df = self.db.get_view_data(
            "vw_ml_insights"
        )

        avg_probability = (
            df["purchase_probability"]
            .mean()
        )

        expected_revenue = (
            df["predicted_revenue"]
            .sum()
        )

        avg_gap = (
            df["forecast_gap"]
            .mean()
        )

        high_probability = len(
            df[df["purchase_probability"] >= 0.95]
        )

        insights = [

            f"Average purchase probability is {avg_probability:.2%}.",

            f"Predicted future revenue equals ₹{expected_revenue:,.2f}.",

            f"Average forecast gap is ₹{avg_gap:.2f}.",

            f"{high_probability:,} customers show strong purchase intent.",

            "ML predictions identify future revenue opportunities."
        ]

        return insights

    # =====================================================
    # OPPORTUNITY CENTER
    # =====================================================

    def generate_opportunity_insights(self):

        df = self.db.get_view_data(
            "vw_opportunity_center"
        )

        high_opportunity = len(
            df[df["opportunity_level"] == "High"]
        )

        potential_revenue = (
            df["revenue_opportunity_score"]
            .sum()
        )

        avg_probability = (
            df["purchase_probability"]
            .mean()
        )

        insights = [

            f"{high_opportunity:,} customers are classified as high opportunity.",

            f"Combined opportunity score equals {potential_revenue:,.2f}.",

            f"Average purchase probability is {avg_probability:.2%}.",

            f"Average customer value score is {df['customer_value_score'].mean():.2f}.",

            "Opportunity scoring highlights the best customers for targeting campaigns."
        ]

        return insights

    # =====================================================
    # ROUTER
    # =====================================================

    def generate(self, dashboard_name):

        dashboard_map = {

            "executive":
                self.generate_executive_insights,

            "customer":
                self.generate_customer_insights,

            "product":
                self.generate_product_insights,

            "revenue":
                self.generate_revenue_insights,

            "geographic":
                self.generate_geographic_insights,

            "sales":
                self.generate_sales_insights,

            "ml":
                self.generate_ml_insights,

            "opportunity":
                self.generate_opportunity_insights
        }

        dashboard_name = dashboard_name.lower()

        if dashboard_name not in dashboard_map:

            return [
                f"No insights available for {dashboard_name}"
            ]

        return dashboard_map[
            dashboard_name
        ]()