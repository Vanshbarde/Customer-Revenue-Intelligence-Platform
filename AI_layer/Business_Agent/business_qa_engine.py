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


class BusinessQAEngine:

    def __init__(self):
        self.db = DatabaseManager()
        self.db.connect()

    def close(self):
        self.db.disconnect()

     # ==========================================
    # EXECUTIVE DASHBOARD FUNCTIONS
    # ==========================================
    
    def get_executive_data(self):
    
        df = self.db.get_view_data(
            "vw_executive_dashboard"
        )
    
        return df.iloc[0]
    
    
    def get_total_revenue(self):
    
        row = self.get_executive_data()
    
        return float(
            row["total_revenue"]
        )
    
    
    def get_total_customers(self):
    
        row = self.get_executive_data()
    
        return int(
            row["total_customers"]
        )
    
    
    def get_total_orders(self):
    
        row = self.get_executive_data()
    
        return int(
            row["total_orders"]
        )
    
    
    def get_avg_order_value(self):
    
        row = self.get_executive_data()
    
        return round(
            float(row["avg_order_value"]),
            2
        )
    
    
    def get_total_sellers(self):
    
        row = self.get_executive_data()
    
        return int(
            row["total_sellers"]
        )
    
    
    def get_customer_order_ratio(self):
    
        row = self.get_executive_data()
    
        customers = float(
            row["total_customers"]
        )
    
        orders = float(
            row["total_orders"]
        )
    
        if customers == 0:
            return 0
    
        return round(
            orders / customers,
            2
        )
    
    
    def get_revenue_per_customer(self):
    
        row = self.get_executive_data()
    
        customers = float(
            row["total_customers"]
        )
    
        revenue = float(
            row["total_revenue"]
        )
    
        if customers == 0:
            return 0
    
        return round(
            revenue / customers,
            2
        )
    
    
    def get_revenue_per_seller(self):
    
        row = self.get_executive_data()
    
        sellers = float(
            row["total_sellers"]
        )
    
        revenue = float(
            row["total_revenue"]
        )
    
        if sellers == 0:
            return 0
    
        return round(
            revenue / sellers,
            2
        )
    
    
    def get_orders_per_seller(self):
    
        row = self.get_executive_data()
    
        sellers = float(
            row["total_sellers"]
        )
    
        orders = float(
            row["total_orders"]
        )
    
        if sellers == 0:
            return 0
    
        return round(
            orders / sellers,
            2
        )
    
    
    def get_executive_summary(self):
    
        return {
    
            "total_revenue":
                self.get_total_revenue(),
    
            "total_customers":
                self.get_total_customers(),
    
            "total_orders":
                self.get_total_orders(),
    
            "avg_order_value":
                self.get_avg_order_value(),
    
            "total_sellers":
                self.get_total_sellers(),
    
            "customer_order_ratio":
                self.get_customer_order_ratio(),
    
            "revenue_per_customer":
                self.get_revenue_per_customer(),
    
            "revenue_per_seller":
                self.get_revenue_per_seller(),
    
            "orders_per_seller":
                self.get_orders_per_seller()
        }
    
    
    def answer_total_revenue(self):
    
        revenue = self.get_total_revenue()
    
        return (
            f"Total revenue is "
            f"₹{revenue:,.2f}"
        )
    
    
    def answer_total_customers(self):
    
        customers = self.get_total_customers()
    
        return (
            f"Total customers are "
            f"{customers:,}"
        )
    
    
    def answer_total_orders(self):
    
        orders = self.get_total_orders()
    
        return (
            f"Total orders are "
            f"{orders:,}"
        )
    
    
    def answer_avg_order_value(self):
    
        aov = self.get_avg_order_value()
    
        return (
            f"Average order value is "
            f"₹{aov:,.2f}"
        )
    
    
    def answer_total_sellers(self):
    
        sellers = self.get_total_sellers()
    
        return (
            f"Total sellers are "
            f"{sellers:,}"
        )   
    
    
    # ==========================================
    # CUSTOMER INTELLIGENCE FUNCTIONS
    # ==========================================
    
    def get_customer_data(self):
    
        return self.db.get_view_data(
            "vw_customer_intelligence"
        )
    
    
    def get_customer_count(self):
    
        df = self.get_customer_data()
    
        return len(df)
    
    
    def get_avg_customer_revenue(self):
    
        df = self.get_customer_data()
    
        return round(
            df["total_revenue"].mean(),
            2
        )
    
    
    def get_avg_customer_orders(self):
    
        df = self.get_customer_data()
    
        return round(
            df["total_orders"].mean(),
            2
        )
    
    
    def get_avg_customer_value_score(self):
    
        df = self.get_customer_data()
    
        return round(
            df["customer_value_score"].mean(),
            2
        )
    
    
    def get_avg_customer_lifetime(self):
    
        df = self.get_customer_data()
    
        return round(
            df["customer_lifetime_days"].mean(),
            2
        )
    
    
    def get_avg_customer_recency(self):
    
        df = self.get_customer_data()
    
        return round(
            df["recency_days"].mean(),
            2
        )
    
    
    def get_top_segment(self):
    
        df = self.get_customer_data()
    
        segment = (
            df["segment_name"]
            .value_counts()
            .idxmax()
        )
    
        count = (
            df["segment_name"]
            .value_counts()
            .max()
        )
    
        return {
            "segment": segment,
            "customers": int(count)
        }
    
    
    def get_segment_distribution(self):
    
        df = self.get_customer_data()
    
        return (
            df["segment_name"]
            .value_counts()
            .to_dict()
        )
    
    
    def get_top_opportunity_level(self):
    
        df = self.get_customer_data()
    
        level = (
            df["opportunity_level"]
            .value_counts()
            .idxmax()
        )
    
        count = (
            df["opportunity_level"]
            .value_counts()
            .max()
        )
    
        return {
            "level": level,
            "customers": int(count)
        }
    
    
    def get_opportunity_distribution(self):
    
        df = self.get_customer_data()
    
        return (
            df["opportunity_level"]
            .value_counts()
            .to_dict()
        )
    
    
    def get_high_value_customers(self):
    
        df = self.get_customer_data()
    
        avg_score = (
            df["customer_value_score"]
            .mean()
        )
    
        count = len(
            df[
                df["customer_value_score"]
                > avg_score
            ]
        )
    
        return count
    
    
    def get_top_customer_by_revenue(self):
    
        df = self.get_customer_data()
    
        top = df.loc[
            df["total_revenue"].idxmax()
        ]
    
        return {
            "customer_id":
                top["customer_unique_id"],
    
            "revenue":
                round(
                    top["total_revenue"],
                    2
                )
        }
    
    
    def get_top_customer_by_orders(self):
    
        df = self.get_customer_data()
    
        top = df.loc[
            df["total_orders"].idxmax()
        ]
    
        return {
            "customer_id":
                top["customer_unique_id"],
    
            "orders":
                int(
                    top["total_orders"]
                )
        }
    
    
    def get_customer_summary(self):
    
        return {
    
            "customer_count":
                self.get_customer_count(),
    
            "avg_customer_revenue":
                self.get_avg_customer_revenue(),
    
            "avg_customer_orders":
                self.get_avg_customer_orders(),
    
            "avg_customer_value_score":
                self.get_avg_customer_value_score(),
    
            "avg_customer_lifetime":
                self.get_avg_customer_lifetime(),
    
            "avg_customer_recency":
                self.get_avg_customer_recency(),
    
            "top_segment":
                self.get_top_segment(),
    
            "top_opportunity":
                self.get_top_opportunity_level(),
    
            "high_value_customers":
                self.get_high_value_customers(),
    
            "top_customer_revenue":
                self.get_top_customer_by_revenue(),
    
            "top_customer_orders":
                self.get_top_customer_by_orders()
        }
    
    
    # ==========================================
    # CUSTOMER CHATBOT ANSWERS
    # ==========================================
    
    def answer_customer_count(self):
    
        return (
            f"Total customers are "
            f"{self.get_customer_count():,}."
        )
    
    
    def answer_top_segment(self):
    
        data = self.get_top_segment()
    
        return (
            f"Largest customer segment is "
            f"{data['segment']} with "
            f"{data['customers']:,} customers."
        )
    
    
    def answer_avg_customer_revenue(self):
    
        revenue = (
            self.get_avg_customer_revenue()
        )
    
        return (
            f"Average customer revenue is "
            f"₹{revenue:,.2f}."
        )
    
    
    def answer_top_opportunity(self):
    
        data = (
            self.get_top_opportunity_level()
        )
    
        return (
            f"Most customers belong to "
            f"{data['level']} opportunity group "
            f"with {data['customers']:,} customers."
        )
    
    
    def answer_high_value_customers(self):
    
        count = (
            self.get_high_value_customers()
        )
    
        return (
            f"There are {count:,} "
            f"high-value customers."
        )
    
    
    
    
    
    # ==========================================
    # PRODUCT INTELLIGENCE FUNCTIONS
    # ==========================================
    
    def get_product_data(self):
    
        return self.db.get_view_data(
            "vw_product_intelligence"
        )
    
    
    def get_product_performance_data(self):
    
        return self.db.get_view_data(
            "vw_product_performance"
        )
    
    
    def get_category_performance_data(self):
    
        return self.db.get_view_data(
            "vw_category_performance"
        )
    
    
    def get_total_product_revenue(self):
    
        df = self.get_product_data()
    
        return round(
            df["revenue"].sum(),
            2
        )
    
    
    def get_total_items_sold(self):
    
        df = self.get_product_data()
    
        return int(
            df["items_sold"].sum()
        )
    
    
    def get_total_categories(self):
    
        df = self.get_product_data()
    
        return int(
            df["category"].nunique()
        )
    
    
    def get_top_category(self):
    
        df = self.get_product_data()
    
        top = df.loc[
            df["revenue"].idxmax()
        ]
    
        return {
            "category": top["category"],
            "revenue": round(
                top["revenue"], 2
            ),
            "items_sold": int(
                top["items_sold"]
            )
        }
    
    
    def get_top_5_categories(self):
    
        df = self.get_product_data()
    
        top = (
            df.sort_values(
                "revenue",
                ascending=False
            )
            .head(5)
        )
    
        return top[
            ["category", "revenue"]
        ].to_dict(
            orient="records"
        )
    
    
    def get_best_selling_category(self):
    
        df = self.get_product_data()
    
        top = df.loc[
            df["items_sold"].idxmax()
        ]
    
        return {
            "category": top["category"],
            "items_sold": int(
                top["items_sold"]
            )
        }
    
    
    def get_avg_category_revenue(self):
    
        df = self.get_product_data()
    
        return round(
            df["revenue"].mean(),
            2
        )
    
    
    def get_avg_category_sales(self):
    
        df = self.get_product_data()
    
        return round(
            df["items_sold"].mean(),
            2
        )
    
    
    def get_top_product(self):
    
        df = self.get_product_performance_data()
    
        top = df.loc[
            df["product_revenue"].idxmax()
        ]
    
        return {
            "product_id":
                top["product_id"],
    
            "category":
                top["category"],
    
            "revenue":
                round(
                    top["product_revenue"],
                    2
                )
        }
    
    
    def get_most_ordered_product(self):
    
        df = self.get_product_performance_data()
    
        top = df.loc[
            df["total_orders"].idxmax()
        ]
    
        return {
            "product_id":
                top["product_id"],
    
            "orders":
                int(
                    top["total_orders"]
                )
        }
    
    
    def get_avg_product_price(self):
    
        df = self.get_product_performance_data()
    
        return round(
            df["avg_product_price"].mean(),
            2
        )
    
    
    def get_total_freight_revenue(self):
    
        df = self.get_product_performance_data()
    
        return round(
            df["freight_revenue"].sum(),
            2
        )
    
    
    def get_high_revenue_categories(self):
    
        df = self.get_category_performance_data()
    
        avg_revenue = (
            df["total_revenue"].mean()
        )
    
        return len(
            df[
                df["total_revenue"]
                > avg_revenue
            ]
        )
    
    
    def get_product_summary(self):
    
        return {
    
            "total_product_revenue":
                self.get_total_product_revenue(),
    
            "total_items_sold":
                self.get_total_items_sold(),
    
            "total_categories":
                self.get_total_categories(),
    
            "top_category":
                self.get_top_category(),
    
            "top_5_categories":
                self.get_top_5_categories(),
    
            "best_selling_category":
                self.get_best_selling_category(),
    
            "avg_category_revenue":
                self.get_avg_category_revenue(),
    
            "avg_category_sales":
                self.get_avg_category_sales(),
    
            "top_product":
                self.get_top_product(),
    
            "most_ordered_product":
                self.get_most_ordered_product(),
    
            "avg_product_price":
                self.get_avg_product_price(),
    
            "freight_revenue":
                self.get_total_freight_revenue(),
    
            "high_revenue_categories":
                self.get_high_revenue_categories()
        }
    
    
    # ==========================================
    # PRODUCT CHATBOT ANSWERS
    # ==========================================
    
    def answer_top_category(self):
    
        data = self.get_top_category()
    
        return (
            f"Top category is "
            f"{data['category']} "
            f"with revenue of "
            f"₹{data['revenue']:,.2f}."
        )
    
    
    def answer_total_items_sold(self):
    
        return (
            f"Total items sold are "
            f"{self.get_total_items_sold():,}."
        )
    
    
    def answer_total_categories(self):
    
        return (
            f"There are "
            f"{self.get_total_categories()} "
            f"product categories."
        )
    
    
    def answer_top_product(self):
    
        data = self.get_top_product()
    
        return (
            f"Top product is "
            f"{data['product_id']} "
            f"from category "
            f"{data['category']} "
            f"with revenue of "
            f"₹{data['revenue']:,.2f}."
        )
    
    
    def answer_avg_product_price(self):
    
        price = self.get_avg_product_price()
    
        return (
            f"Average product price is "
            f"₹{price:,.2f}."
        )
    
    
    
    
    # ==========================================
    # REVENUE INTELLIGENCE FUNCTIONS
    # ==========================================
    
    def get_revenue_data(self):
    
        return self.db.get_view_data(
            "vw_revenue_intelligence"
        )
    
    
    def get_revenue_growth_data(self):
    
        return self.db.get_view_data(
            "vw_revenue_growth"
        )
    
    
    def get_total_orders_revenue_dashboard(self):
    
        df = self.get_revenue_data()
    
        return int(
            df["orders"].sum()
        )
    
    
    def get_average_monthly_revenue(self):
    
        df = self.get_revenue_data()
    
        return round(
            df["revenue"].mean(),
            2
        )
    
    
    def get_average_order_value_revenue(self):
    
        df = self.get_revenue_data()
    
        return round(
            df["avg_order_value"].mean(),
            2
        )
    
    
    def get_best_revenue_month(self):
    
        df = self.get_revenue_data()
    
        top = df.loc[
            df["revenue"].idxmax()
        ]
    
        return {
            "month": str(top["month"]),
            "revenue": round(
                top["revenue"],
                2
            )
        }
    
    
    def get_worst_revenue_month(self):
    
        df = self.get_revenue_data()
    
        low = df.loc[
            df["revenue"].idxmin()
        ]
    
        return {
            "month": str(low["month"]),
            "revenue": round(
                low["revenue"],
                2
            )
        }
    
    
    def get_latest_growth_rate(self):
    
        df = self.get_revenue_growth_data()
    
        growth = (
            df["revenue_growth_pct"]
            .dropna()
        )
    
        if growth.empty:
            return 0
    
        return round(
            growth.iloc[-1],
            2
        )
    
    
    def get_average_growth_rate(self):
    
        df = self.get_revenue_growth_data()
    
        growth = (
            df["revenue_growth_pct"]
            .dropna()
        )
    
        if growth.empty:
            return 0
    
        return round(
            growth.mean(),
            2
        )
    
    
    def get_highest_growth_month(self):
    
        df = self.get_revenue_growth_data()
    
        growth = df.dropna(
            subset=[
                "revenue_growth_pct"
            ]
        )
    
        top = growth.loc[
            growth[
                "revenue_growth_pct"
            ].idxmax()
        ]
    
        return {
            "month": str(top["month"]),
            "growth": round(
                top[
                    "revenue_growth_pct"
                ],
                2
            )
        }
    
    
    def get_lowest_growth_month(self):
    
        df = self.get_revenue_growth_data()
    
        growth = df.dropna(
            subset=[
                "revenue_growth_pct"
            ]
        )
    
        low = growth.loc[
            growth[
                "revenue_growth_pct"
            ].idxmin()
        ]
    
        return {
            "month": str(low["month"]),
            "growth": round(
                low[
                    "revenue_growth_pct"
                ],
                2
            )
        }
    
    
    def get_revenue_trend(self):
    
        latest_growth = (
            self.get_latest_growth_rate()
        )
    
        if latest_growth > 0:
            return "Growing"
    
        elif latest_growth < 0:
            return "Declining"
    
        else:
            return "Stable"
    
    
    def get_month_count(self):
    
        df = self.get_revenue_data()
    
        return len(df)
    
    
    def get_revenue_summary(self):
    
        return {
    
            "total_revenue":
                self.get_total_revenue(),
    
            "total_orders":
                self.get_total_orders_revenue_dashboard(),
    
            "average_monthly_revenue":
                self.get_average_monthly_revenue(),
    
            "average_order_value":
                self.get_average_order_value_revenue(),
    
            "best_month":
                self.get_best_revenue_month(),
    
            "worst_month":
                self.get_worst_revenue_month(),
    
            "latest_growth":
                self.get_latest_growth_rate(),
    
            "average_growth":
                self.get_average_growth_rate(),
    
            "highest_growth_month":
                self.get_highest_growth_month(),
    
            "lowest_growth_month":
                self.get_lowest_growth_month(),
    
            "trend":
                self.get_revenue_trend(),
    
            "month_count":
                self.get_month_count()
        }
    
    
    # ==========================================
    # REVENUE CHATBOT ANSWERS
    # ==========================================
    
    def answer_total_revenue_dashboard(self):
    
        revenue = (
            self.get_total_revenue()
        )
    
        return (
            f"Total revenue is "
            f"₹{revenue:,.2f}."
        )
    
    
    def answer_best_revenue_month(self):
    
        data = (
            self.get_best_revenue_month()
        )
    
        return (
            f"Best revenue month was "
            f"{data['month']} "
            f"with revenue of "
            f"₹{data['revenue']:,.2f}."
        )
    
    
    def answer_latest_growth(self):
    
        growth = (
            self.get_latest_growth_rate()
        )
    
        return (
            f"Latest revenue growth "
            f"is {growth:.2f}%."
        )
    
    
    def answer_revenue_trend(self):
    
        trend = (
            self.get_revenue_trend()
        )
    
        return (
            f"Current revenue trend "
            f"is {trend}."
        )
    
    
    def answer_average_monthly_revenue(self):
    
        revenue = (
            self.get_average_monthly_revenue()
        )
    
        return (
            f"Average monthly revenue "
            f"is ₹{revenue:,.2f}."
        )
    
    
    
    
    # ==========================================
    # GEOGRAPHIC INTELLIGENCE FUNCTIONS
    # ==========================================
    
    def get_geographic_data(self):
    
        return self.db.get_view_data(
            "vw_geographic_intelligence"
        )
    
    
    def get_total_geographic_revenue(self):
    
        df = self.get_geographic_data()
    
        return round(
            df["revenue"].sum(),
            2
        )
    
    
    def get_total_states(self):
    
        df = self.get_geographic_data()
    
        return int(
            df["customer_state"]
            .nunique()
        )
    
    
    def get_total_cities(self):
    
        df = self.get_geographic_data()
    
        return int(
            df["customer_city"]
            .nunique()
        )
    
    
    def get_total_customers_geo(self):
    
        df = self.get_geographic_data()
    
        return int(
            df["customers"].sum()
        )
    
    
    def get_top_state_by_revenue(self):
    
        df = self.get_geographic_data()
    
        state_df = (
            df.groupby(
                "customer_state"
            )["revenue"]
            .sum()
            .reset_index()
        )
    
        top = state_df.loc[
            state_df["revenue"].idxmax()
        ]
    
        return {
            "state":
                top["customer_state"],
    
            "revenue":
                round(
                    top["revenue"],
                    2
                )
        }
    
    
    def get_top_city_by_revenue(self):
    
        df = self.get_geographic_data()
    
        top = df.loc[
            df["revenue"].idxmax()
        ]
    
        return {
            "city":
                top["customer_city"],
    
            "state":
                top["customer_state"],
    
            "revenue":
                round(
                    top["revenue"],
                    2
                )
        }
    
    
    def get_top_state_by_customers(self):
    
        df = self.get_geographic_data()
    
        state_df = (
            df.groupby(
                "customer_state"
            )["customers"]
            .sum()
            .reset_index()
        )
    
        top = state_df.loc[
            state_df["customers"].idxmax()
        ]
    
        return {
            "state":
                top["customer_state"],
    
            "customers":
                int(
                    top["customers"]
                )
        }
    
    
    def get_top_city_by_customers(self):
    
        df = self.get_geographic_data()
    
        top = df.loc[
            df["customers"].idxmax()
        ]
    
        return {
            "city":
                top["customer_city"],
    
            "state":
                top["customer_state"],
    
            "customers":
                int(
                    top["customers"]
                )
        }
    
    
    def get_average_state_revenue(self):
    
        df = self.get_geographic_data()
    
        state_df = (
            df.groupby(
                "customer_state"
            )["revenue"]
            .sum()
        )
    
        return round(
            state_df.mean(),
            2
        )
    
    
    def get_average_city_revenue(self):
    
        df = self.get_geographic_data()
    
        return round(
            df["revenue"].mean(),
            2
        )
    
    
    def get_top_5_states_by_revenue(self):
    
        df = self.get_geographic_data()
    
        state_df = (
            df.groupby(
                "customer_state"
            )["revenue"]
            .sum()
            .sort_values(
                ascending=False
            )
            .head(5)
        )
    
        return state_df.to_dict()
    
    
    def get_top_5_cities_by_revenue(self):
    
        df = self.get_geographic_data()
    
        top = (
            df.sort_values(
                "revenue",
                ascending=False
            )
            .head(5)
        )
    
        return top[
            [
                "customer_city",
                "revenue"
            ]
        ].to_dict(
            orient="records"
        )
    
    
    def get_geographic_summary(self):
    
        return {
    
            "total_revenue":
                self.get_total_geographic_revenue(),
    
            "total_customers":
                self.get_total_customers_geo(),
    
            "states":
                self.get_total_states(),
    
            "cities":
                self.get_total_cities(),
    
            "top_state_revenue":
                self.get_top_state_by_revenue(),
    
            "top_city_revenue":
                self.get_top_city_by_revenue(),
    
            "top_state_customers":
                self.get_top_state_by_customers(),
    
            "top_city_customers":
                self.get_top_city_by_customers(),
    
            "avg_state_revenue":
                self.get_average_state_revenue(),
    
            "avg_city_revenue":
                self.get_average_city_revenue(),
    
            "top_5_states":
                self.get_top_5_states_by_revenue(),
    
            "top_5_cities":
                self.get_top_5_cities_by_revenue()
        }
    
    
    # ==========================================
    # GEOGRAPHIC CHATBOT ANSWERS
    # ==========================================
    
    def answer_top_state_revenue(self):
    
        data = (
            self.get_top_state_by_revenue()
        )
    
        return (
            f"Top revenue state is "
            f"{data['state']} with "
            f"₹{data['revenue']:,.2f}."
        )
    
    
    def answer_top_city_revenue(self):
    
        data = (
            self.get_top_city_by_revenue()
        )
    
        return (
            f"Top revenue city is "
            f"{data['city']} "
            f"({data['state']}) with "
            f"₹{data['revenue']:,.2f}."
        )
    
    
    def answer_top_state_customers(self):
    
        data = (
            self.get_top_state_by_customers()
        )
    
        return (
            f"State with most customers is "
            f"{data['state']} with "
            f"{data['customers']:,} customers."
        )
    
    
    def answer_total_states(self):
    
        return (
            f"Business operates in "
            f"{self.get_total_states()} states."
        )
    
    
    def answer_total_cities(self):
    
        return (
            f"Business operates in "
            f"{self.get_total_cities()} cities."
        )
    
    
    
    
    # ==========================================
    # ML INTELLIGENCE FUNCTIONS
    # ==========================================
    
    def get_ml_data(self):
    
        return self.db.get_view_data(
            "vw_ml_insights"
        )
    
    
    def get_total_predicted_revenue(self):
    
        df = self.get_ml_data()
    
        return round(
            df["predicted_revenue"].sum(),
            2
        )
    
    
    def get_total_actual_revenue(self):
    
        df = self.get_ml_data()
    
        return round(
            df["actual_revenue"].sum(),
            2
        )
    
    
    def get_average_purchase_probability(self):
    
        df = self.get_ml_data()
    
        return round(
            df["purchase_probability"].mean() * 100,
            2
        )
    
    
    def get_average_forecast_gap(self):
    
        df = self.get_ml_data()
    
        return round(
            df["forecast_gap"].mean(),
            2
        )
    
    
    def get_high_probability_customers(self):
    
        df = self.get_ml_data()
    
        return len(
            df[
                df["purchase_probability"]
                >= 0.95
            ]
        )
    
    
    def get_medium_probability_customers(self):
    
        df = self.get_ml_data()
    
        return len(
            df[
                (
                    df["purchase_probability"]
                    >= 0.80
                )
                &
                (
                    df["purchase_probability"]
                    < 0.95
                )
            ]
        )
    
    
    def get_low_probability_customers(self):
    
        df = self.get_ml_data()
    
        return len(
            df[
                df["purchase_probability"]
                < 0.80
            ]
        )
    
    
    def get_purchase_probability_distribution(self):
    
        return {
    
            "high":
                self.get_high_probability_customers(),
    
            "medium":
                self.get_medium_probability_customers(),
    
            "low":
                self.get_low_probability_customers()
        }
    
    
    def get_top_segment_prediction(self):
    
        df = self.get_ml_data()
    
        segment_df = (
            df.groupby(
                "segment_name"
            )["purchase_probability"]
            .mean()
            .reset_index()
        )
    
        top = segment_df.loc[
            segment_df[
                "purchase_probability"
            ].idxmax()
        ]
    
        return {
    
            "segment":
                top["segment_name"],
    
            "probability":
                round(
                    top[
                        "purchase_probability"
                    ] * 100,
                    2
                )
        }
    
    
    def get_highest_predicted_customer(self):
    
        df = self.get_ml_data()
    
        top = df.loc[
            df[
                "predicted_revenue"
            ].idxmax()
        ]
    
        return {
    
            "customer":
                top[
                    "customer_unique_id"
                ],
    
            "predicted_revenue":
                round(
                    top[
                        "predicted_revenue"
                    ],
                    2
                )
        }
    
    
    def get_total_forecast_gap(self):
    
        df = self.get_ml_data()
    
        return round(
            df["forecast_gap"].sum(),
            2
        )
    
    
    def get_forecast_accuracy_indicator(self):
    
        gap = abs(
            self.get_average_forecast_gap()
        )
    
        if gap < 5:
    
            return "Excellent"
    
        elif gap < 15:
    
            return "Good"
    
        else:
    
            return "Needs Improvement"
    
    
    def get_ml_summary(self):
    
        return {
    
            "predicted_revenue":
                self.get_total_predicted_revenue(),
    
            "actual_revenue":
                self.get_total_actual_revenue(),
    
            "avg_probability":
                self.get_average_purchase_probability(),
    
            "avg_forecast_gap":
                self.get_average_forecast_gap(),
    
            "forecast_accuracy":
                self.get_forecast_accuracy_indicator(),
    
            "high_probability":
                self.get_high_probability_customers(),
    
            "medium_probability":
                self.get_medium_probability_customers(),
    
            "low_probability":
                self.get_low_probability_customers(),
    
            "top_segment":
                self.get_top_segment_prediction(),
    
            "highest_customer":
                self.get_highest_predicted_customer(),
    
            "total_gap":
                self.get_total_forecast_gap()
        }
    # ==========================================
    # ML CHATBOT ANSWERS
    # ==========================================
    
    def answer_average_purchase_probability(self):
    
        prob = (
            self.get_average_purchase_probability()
        )
    
        return (
            f"Average purchase probability "
            f"is {prob:.2f}%."
        )
    
    
    def answer_predicted_revenue(self):
    
        revenue = (
            self.get_total_predicted_revenue()
        )
    
        return (
            f"Predicted future revenue is "
            f"₹{revenue:,.2f}."
        )
    
    
    def answer_forecast_accuracy(self):
    
        accuracy = (
            self.get_forecast_accuracy_indicator()
        )
    
        gap = (
            self.get_average_forecast_gap()
        )
    
        return (
            f"Forecast accuracy is "
            f"rated '{accuracy}' "
            f"with average gap of "
            f"{gap:.2f}."
        )
    
    
    def answer_high_probability_customers(self):
    
        count = (
            self.get_high_probability_customers()
        )
    
        return (
            f"{count:,} customers have "
            f"high purchase probability."
        )
    
    
    def answer_top_prediction_segment(self):
    
        data = (
            self.get_top_segment_prediction()
        )
    
        return (
            f"Top predicted segment is "
            f"{data['segment']} with "
            f"{data['probability']:.2f}% "
            f"average purchase probability."
        )
    
    
    
    
    
    # ==========================================
    # OPPORTUNITY CENTER FUNCTIONS
    # ==========================================
    
    def get_opportunity_data(self):
    
        return self.db.get_view_data(
            "vw_opportunity_center"
        )
    
    
    def get_high_opportunity_customers(self):
    
        df = self.get_opportunity_data()
    
        return len(
            df[
                df["opportunity_level"]
                == "High"
            ]
        )
    
    
    def get_medium_opportunity_customers(self):
    
        df = self.get_opportunity_data()
    
        return len(
            df[
                df["opportunity_level"]
                == "Medium"
            ]
        )
    
    
    def get_low_opportunity_customers(self):
    
        df = self.get_opportunity_data()
    
        return len(
            df[
                df["opportunity_level"]
                == "Low"
            ]
        )
    
    
    def get_total_opportunity_score(self):
    
        df = self.get_opportunity_data()
    
        return round(
            df[
                "revenue_opportunity_score"
            ].sum(),
            2
        )
    
    
    def get_average_opportunity_score(self):
    
        df = self.get_opportunity_data()
    
        return round(
            df[
                "revenue_opportunity_score"
            ].mean(),
            2
        )
    
    
    def get_average_customer_value_score(self):
    
        df = self.get_opportunity_data()
    
        return round(
            df[
                "customer_value_score"
            ].mean(),
            2
        )
    
    
    def get_highest_opportunity_customer(self):
    
        df = self.get_opportunity_data()
    
        top = df.loc[
            df[
                "revenue_opportunity_score"
            ].idxmax()
        ]
    
        return {
    
            "customer":
                top[
                    "customer_unique_id"
                ],
    
            "score":
                round(
                    top[
                        "revenue_opportunity_score"
                    ],
                    2
                )
        }
    
    
    def get_repeat_customers_count(self):
    
        df = self.get_opportunity_data()
    
        return len(
            df[
                df[
                    "repeat_customer"
                ] == 1
            ]
        )
    
    
    def get_non_repeat_customers_count(self):
    
        df = self.get_opportunity_data()
    
        return len(
            df[
                df[
                    "repeat_customer"
                ] == 0
            ]
        )
    
    
    def get_average_purchase_probability_opportunity(self):
    
        df = self.get_opportunity_data()
    
        return round(
            df[
                "purchase_probability"
            ].mean() * 100,
            2
        )
    
    
    def get_top_segment_opportunity(self):
    
        df = self.get_opportunity_data()
    
        segment_df = (
            df.groupby(
                "segment_name"
            )[
                "revenue_opportunity_score"
            ]
            .mean()
            .reset_index()
        )
    
        top = segment_df.loc[
            segment_df[
                "revenue_opportunity_score"
            ].idxmax()
        ]
    
        return {
    
            "segment":
                top["segment_name"],
    
            "score":
                round(
                    top[
                        "revenue_opportunity_score"
                    ],
                    2
                )
        }
    
    
    def get_average_review_score(self):
    
        df = self.get_opportunity_data()
    
        return round(
            df[
                "avg_review_score"
            ].mean(),
            2
        )
    
    
    def get_average_customer_lifetime(self):
    
        df = self.get_opportunity_data()
    
        return round(
            df[
                "customer_lifetime_days"
            ].mean(),
            2
        )
    
    
    def get_average_recency_days(self):
    
        df = self.get_opportunity_data()
    
        return round(
            df[
                "recency_days"
            ].mean(),
            2
        )
    
    
    def get_opportunity_summary(self):
    
        return {
    
            "high_opportunity":
                self.get_high_opportunity_customers(),
    
            "medium_opportunity":
                self.get_medium_opportunity_customers(),
    
            "low_opportunity":
                self.get_low_opportunity_customers(),
    
            "total_score":
                self.get_total_opportunity_score(),
    
            "average_score":
                self.get_average_opportunity_score(),
    
            "customer_value":
                self.get_average_customer_value_score(),
    
            "repeat_customers":
                self.get_repeat_customers_count(),
    
            "non_repeat_customers":
                self.get_non_repeat_customers_count(),
    
            "purchase_probability":
                self.get_average_purchase_probability_opportunity(),
    
            "top_segment":
                self.get_top_segment_opportunity(),
    
            "highest_customer":
                self.get_highest_opportunity_customer(),
    
            "avg_review":
                self.get_average_review_score(),
    
            "avg_lifetime":
                self.get_average_customer_lifetime(),
    
            "avg_recency":
                self.get_average_recency_days()
        }
    
    # ==========================================
    # OPPORTUNITY CHATBOT ANSWERS
    # ==========================================
    
    def answer_high_opportunity_customers(self):
    
        count = (
            self.get_high_opportunity_customers()
        )
    
        return (
            f"{count:,} customers are "
            f"classified as high opportunity."
        )
    
    
    def answer_total_opportunity_score(self):
    
        score = (
            self.get_total_opportunity_score()
        )
    
        return (
            f"Total opportunity score "
            f"is {score:,.2f}."
        )
    
    
    def answer_top_opportunity_segment(self):
    
        data = (
            self.get_top_segment_opportunity()
        )
    
        return (
            f"Top opportunity segment is "
            f"{data['segment']} "
            f"with average score "
            f"of {data['score']:.2f}."
        )
    
    
    def answer_repeat_customers(self):
    
        count = (
            self.get_repeat_customers_count()
        )
    
        return (
            f"{count:,} customers are "
            f"repeat buyers."
        )
    
    
    def answer_customer_value_score(self):
    
        score = (
            self.get_average_customer_value_score()
        )
    
        return (
            f"Average customer value "
            f"score is {score:.2f}."
        )
    
    
    
    # ==========================================
    # SALES PERFORMANCE FUNCTIONS
    # ==========================================
    
    def get_sales_data(self):
    
        return self.db.get_view_data(
            "vw_sales_performance"
        )
    
    
    def get_total_sales_revenue(self):
    
        df = self.get_sales_data()
    
        return round(
            df["revenue"].sum(),
            2
        )
    
    
    def get_avg_daily_revenue(self):
    
        df = self.get_sales_data()
    
        return round(
            df["revenue"].mean(),
            2
        )
    
    
    def get_avg_daily_orders(self):
    
        df = self.get_sales_data()
    
        return round(
            df["total_orders"].mean(),
            2
        )
    
    
    def get_total_sales_days(self):
    
        df = self.get_sales_data()
    
        return len(df)
    
    
    def get_best_sales_day(self):
    
        df = self.get_sales_data()
    
        top = df.loc[
            df["revenue"].idxmax()
        ]
    
        return {
            "date": str(top["sales_date"]),
            "revenue": round(
                top["revenue"],
                2
            )
        }
    
    
    def get_sales_summary(self):
    
        return {
    
            "total_sales_revenue":
                self.get_total_sales_revenue(),
    
            "avg_daily_revenue":
                self.get_avg_daily_revenue(),
    
            "avg_daily_orders":
                self.get_avg_daily_orders(),
    
            "total_sales_days":
                self.get_total_sales_days(),
    
            "best_sales_day":
                self.get_best_sales_day()
        }
    
    
    
    # ==========================================
    # ROUTER / CHATBOT COMPATIBILITY ALIASES
    # ==========================================
    # These give short, chatbot-friendly names to
    # functions that already exist above, so
    # qa_router.py always finds what it expects.
    
    def get_avg_monthly_revenue(self):
    
        return self.get_average_monthly_revenue()
    
    
    def get_latest_growth(self):
    
        return self.get_latest_growth_rate()
    
    
    def get_best_month(self):
    
        data = self.get_best_revenue_month()
    
        return (
            f"{data['month']} with "
            f"₹{data['revenue']:,.2f} revenue"
        )
    
    
    def get_worst_month(self):
    
        data = self.get_worst_revenue_month()
    
        return (
            f"{data['month']} with "
            f"₹{data['revenue']:,.2f} revenue"
        )
    
    
    def get_latest_month_revenue(self):
    
        df = self.get_revenue_data()
    
        latest = df.sort_values("month").iloc[-1]
    
        return round(
            latest["revenue"],
            2
        )
    
    
    def get_top_category_by_orders(self):
    
        df = self.get_category_performance_data()
    
        top = df.loc[
            df["total_orders"].idxmax()
        ]
    
        return {
            "category": top["category"],
            "orders": int(top["total_orders"])
        }
    
    
    def get_predicted_revenue(self):
    
        return self.get_total_predicted_revenue()
    
    
    def get_forecast_gap(self):
    
        return self.get_average_forecast_gap()
    
    
    
    # ==========================================
    # AI RECOMMENDATION FUNCTIONS
    # ==========================================
    
    def recommend_customer_campaign(self):
    
        segment = self.get_top_segment()["segment"]
    
        return (
            f"Focus marketing campaigns on "
            f"'{segment}' customers to improve retention."
        )
    
    
    def recommend_product_campaign(self):
    
        category = self.get_top_category()["category"]
    
        return (
            f"Promote '{category}' products through "
            f"cross-sell and upsell campaigns."
        )
    
    
    def recommend_revenue_action(self):
    
        growth = self.get_latest_growth_rate()
    
        if growth < 0:
    
            return (
                "Revenue is declining. Launch customer "
                "retention and reactivation campaigns."
            )
    
        return (
            "Revenue is growing. Increase acquisition "
            "campaigns to accelerate growth."
        )
    
    
    def recommend_geographic_expansion(self):
    
        state = self.get_top_state_by_revenue()
    
        return (
            f"Expand operations in {state['state']} "
            f"where revenue performance is strongest."
        )
    
    
    def recommend_sales_action(self):
    
        avg_orders = self.get_avg_daily_orders()
    
        if avg_orders < 200:
    
            return (
                "Increase sales through seasonal offers "
                "and promotional campaigns."
            )
    
        return (
            "Current sales volume is healthy. Focus on "
            "increasing average order value."
        )
    
    
    def recommend_opportunity_action(self):
    
        high = self.get_high_opportunity_customers()
    
        return (
            f"Target {high:,} high-opportunity customers "
            f"with premium offers and loyalty programs."
        )
    
    
    def answer_top_city(self):
    
        city = self.get_top_city_by_revenue()
    
        return (
            f"{city['city']} generated "
            f"₹{city['revenue']:,.2f} revenue."
        )
    
    
    def answer_top_state(self):
    
        state = self.get_top_state_by_revenue()
    
        return (
            f"{state['state']} generated "
            f"₹{state['revenue']:,.2f} revenue."
        )
    
    
    def answer_purchase_probability(self):
    
        prob = (
            self.get_average_purchase_probability()
        )
    
        return (
            f"Average purchase probability "
            f"is {prob:.2f}%."
        )
    
    
    def answer_opportunity_score(self):
    
        score = (
            self.get_total_opportunity_score()
        )
    
        return (
            f"Total opportunity score is "
            f"{score:,.2f}."
        )
    
    
    def answer_best_sales_day(self):
    
        day = self.get_best_sales_day()
    
        return (
            f"Best sales day was "
            f"{day['date']} with revenue "
            f"₹{day['revenue']:,.2f}."
        )
    
    
    def answer_top_customer_segment(self):
    
        data = self.get_top_segment()
    
        return (
            f"The largest customer segment is "
            f"{data['segment']} with "
            f"{data['customers']:,} customers."
        )
    
    
    def answer_average_customer_revenue(self):
    
        revenue = self.get_avg_customer_revenue()
    
        return (
            f"Average customer revenue is "
            f"₹{revenue:.2f}."
        )
    
    
    def answer_average_customer_orders(self):
    
        orders = self.get_avg_customer_orders()
    
        return (
            f"Customers place an average of "
            f"{orders:.2f} orders."
        )
    
    
    def answer_total_sales_revenue(self):
    
        revenue = self.get_total_sales_revenue()
    
        return (
            f"Total sales revenue is "
            f"₹{revenue:,.2f}."
        )
    
    
    def answer_average_daily_revenue(self):
    
        revenue = self.get_avg_daily_revenue()
    
        return (
            f"Average daily revenue is "
            f"₹{revenue:,.2f}."
        )
    
    
    def answer_average_daily_orders(self):
    
        orders = self.get_avg_daily_orders()
    
        return (
            f"Average daily orders are "
            f"{orders:.2f}."
        )
    
    
    def answer_total_sales_days(self):
    
        days = self.get_total_sales_days()
    
        return (
            f"Sales history contains "
            f"{days:,} days."
        )    
    
    
    
    # ==========================================
    # ALL RECOMMENDATIONS
    # ==========================================
    
    def get_all_recommendations(self):
    
        recommendations = []
    
        recommendations.append(
            self.recommend_customer_campaign()
        )
    
        recommendations.append(
            self.recommend_product_campaign()
        )
    
        recommendations.append(
            self.recommend_revenue_action()
        )
    
        recommendations.append(
            self.recommend_opportunity_action()
        )
    
        recommendations.append(
            self.recommend_geographic_expansion()
        )
    
        recommendations.append(
            self.recommend_sales_action()
        )
    
        return recommendations