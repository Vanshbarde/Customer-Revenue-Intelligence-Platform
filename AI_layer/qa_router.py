from business_qa_engine import BusinessQAEngine


class QARouter:

    def __init__(self):

        self.qa = BusinessQAEngine()

    def close(self):

        self.qa.close()

    def route(self, question):

        q = question.lower()

        # ==========================================
        # EXECUTIVE
        # ==========================================

        if "total revenue" in q:
            return self.qa.answer_total_revenue()

        if "total customer" in q:
            return self.qa.answer_total_customers()

        if "customer count" in q:
            return self.qa.answer_total_customers()

        if "total order" in q:
            return self.qa.answer_total_orders()

        if "average order value" in q:
            return (
                f"Average order value is "
                f"₹{self.qa.get_avg_order_value():.2f}."
            )

        if "seller" in q:
            return (
                f"Total sellers: "
                f"{self.qa.get_total_sellers():,}"
            )

        # ==========================================
        # CUSTOMER
        # ==========================================

        if "customer segment" in q:
            return self.qa.answer_top_customer_segment()

        if "largest segment" in q:
            return self.qa.answer_top_customer_segment()

        if "average customer revenue" in q:
            return self.qa.answer_average_customer_revenue()

        if "customer revenue" in q:
            return self.qa.answer_average_customer_revenue()

        if "average customer order" in q:
            return self.qa.answer_average_customer_orders()

        if "high value customer" in q:
            return self.qa.answer_high_value_customers()

        # ==========================================
        # PRODUCT
        # ==========================================

        if "top category" in q:
            return self.qa.answer_top_category()

        if "best category" in q:
            return self.qa.answer_top_category()

        if "items sold" in q:
            return (
                f"Total items sold: "
                f"{self.qa.get_total_items_sold():,}"
            )

        # ==========================================
        # REVENUE
        # ==========================================

        if "growth" in q:
            return (
                f"Latest revenue growth: "
                f"{self.qa.get_latest_growth():.2f}%"
            )

        if "best month" in q:
            return (
                f"Best month: "
                f"{self.qa.get_best_month()}"
            )

        if "worst month" in q:
            return (
                f"Worst month: "
                f"{self.qa.get_worst_month()}"
            )

        if "monthly revenue" in q:
            return (
                f"Average monthly revenue: "
                f"₹{self.qa.get_avg_monthly_revenue():,.2f}"
            )

        # ==========================================
        # GEOGRAPHIC
        # ==========================================

        if "top city" in q:
            return self.qa.answer_top_city()

        if "best city" in q:
            return self.qa.answer_top_city()

        if "top state" in q:
            return self.qa.answer_top_state()

        if "best state" in q:
            return self.qa.answer_top_state()

        if "city generates most revenue" in q:
            return self.qa.answer_top_city()

        if "location gives most revenue" in q:
            return self.qa.answer_top_city()

        # ==========================================
        # SALES
        # ==========================================

        if "best sales day" in q:
            return self.qa.answer_best_sales_day()

        if "average daily revenue" in q:
            return self.qa.answer_average_daily_revenue()

        if "average daily order" in q:
            return self.qa.answer_average_daily_orders()

        if "sales revenue" in q:
            return self.qa.answer_total_sales_revenue()

        if "sales days" in q:
            return self.qa.answer_total_sales_days()

        # ==========================================
        # ML
        # ==========================================

        if "purchase probability" in q:
            return self.qa.answer_purchase_probability()

        if "predicted revenue" in q:
            return (
                f"Predicted revenue is "
                f"₹{self.qa.get_predicted_revenue():,.2f}"
            )

        if "forecast gap" in q:
            return (
                f"Average forecast gap is "
                f"₹{self.qa.get_forecast_gap():.2f}"
            )

        # ==========================================
        # OPPORTUNITY
        # ==========================================

        if "opportunity score" in q:
            return self.qa.answer_opportunity_score()

        if "high opportunity customer" in q:
            return (
                f"High opportunity customers: "
                f"{self.qa.get_high_opportunity_customers():,}"
            )

        if "customer value score" in q:
            return (
                f"Average customer value score: "
                f"{self.qa.get_avg_customer_value_score():.2f}"
            )

        # ==========================================
        # RECOMMENDATIONS
        # ==========================================

        if "recommendation" in q:
            recommendations = (
                self.qa.get_all_recommendations()
            )

            return "\n".join(recommendations)

        # ==========================================
        # DEFAULT
        # ==========================================

        return (
            "Sorry, I could not understand the question. "
            "Try asking about revenue, customers, products, "
            "sales, geography, ML insights, or opportunities."
        )