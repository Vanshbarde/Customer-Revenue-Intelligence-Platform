
import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from business_qa_engine import BusinessQAEngine
from difflib import get_close_matches

class QARouter:
    # ==========================================
    # KEYWORD GROUPS
    # ==========================================

    REVENUE_WORDS = [
        "revenue",
        "sales",
        "income",
        "earnings",
        "money",
        "profit",
        "profits",
        "turnover"
    ]

    CUSTOMER_WORDS = [
        "customer",
        "customers",
        "user",
        "users",
        "buyer",
        "buyers"
    ]

    PRODUCT_WORDS = [
        "product",
        "products",
        "category",
        "categories"
    ]

    CITY_WORDS = [
        "city",
        "location",
        "region",
        "market"
    ]

    STATE_WORDS = [
        "state",
        "states"
    ]

    ORDER_WORDS = [
        "order",
        "orders"
    ]


    def __init__(self):
        self.qa = BusinessQAEngine()

    def close(self):
        self.qa.close()

    # ==========================================
    # HELPER: turn a dict/list returned by a
    # *_summary() or *_distribution() function into
    # a readable multi-line answer instead of a raw
    # Python object.
    # ==========================================

    def _format(self, data, indent=0):

        pad = "  " * indent
        lines = []

        if isinstance(data, dict):
            for key, value in data.items():
                label = key.replace("_", " ").capitalize()

                if isinstance(value, (dict, list)):
                    lines.append(f"{pad}{label}:")
                    lines.append(self._format(value, indent + 1))
                else:
                    lines.append(f"{pad}{label}: {value}")

        elif isinstance(data, list):
            for item in data:
                lines.append(self._format(item, indent))

        else:
            lines.append(f"{pad}{data}")

        return "\n".join(lines)

    def route(self, question):

        try:
            return self._route(question)

        except AttributeError as e:
            return (
                "I hit a wiring issue answering that "
                f"question ({e}). This usually means a "
                "function name in qa_router.py doesn't "
                "match one in business_qa_engine.py."
            )

        except Exception as e:
            return (
                "Sorry, I couldn't compute an answer for "
                f"that ({e}). Try rephrasing, or ask about "
                "revenue, customers, products, sales, "
                "geography, ML insights, or opportunities."
            )

    def _route(self, question):
        q = question.lower()
        intent = self.detect_intent(q)

        # ==========================================
        # SUMMARY QUERIES
        # ==========================================

        if "summary" in q and "customer" in q:
            return self._format(self.qa.get_customer_summary())

        if "summary" in q and "product" in q:
            return self._format(self.qa.get_product_summary())

        if "summary" in q and "revenue" in q:
            return self._format(self.qa.get_revenue_summary())

        # ==========================================
        # SUMMARIES (checked first - these are multi-word
        # phrases and should never be caught by a shorter
        # generic keyword check below)
        # ==========================================

        if "executive summary" in q or "business summary" in q:
            return self._format(self.qa.get_executive_summary())

        if "customer summary" in q:
            return self._format(self.qa.get_customer_summary())

        if "product summary" in q:
            return self._format(self.qa.get_product_summary())

        if "revenue summary" in q:
            return self._format(self.qa.get_revenue_summary())

        if "geographic summary" in q or "geography summary" in q:
            return self._format(self.qa.get_geographic_summary())

        if "sales summary" in q:
            return self._format(self.qa.get_sales_summary())

        if "ml summary" in q or "machine learning summary" in q:
            return self._format(self.qa.get_ml_summary())

        if "opportunity summary" in q:
            return self._format(self.qa.get_opportunity_summary())

        # ==========================================
        # DISTRIBUTIONS / TOP-5 LISTS
        # ==========================================

        if "segment distribution" in q:
            return self._format(self.qa.get_segment_distribution())

        if "opportunity distribution" in q:
            return self._format(self.qa.get_opportunity_distribution())

        if "probability distribution" in q:
            return self._format(
                self.qa.get_purchase_probability_distribution()
            )

        if "top 5 categor" in q or "top five categor" in q:
            return self._format(self.qa.get_top_5_categories())

        if "top 5 state" in q or "top five state" in q:
            return self._format(self.qa.get_top_5_states_by_revenue())

        if "top 5 cit" in q or "top five cit" in q:
            return self._format(self.qa.get_top_5_cities_by_revenue())

        # ==========================================
        # RECOMMENDATIONS (specific ones before the
        # generic "give me recommendations" catch-all)
        # ==========================================

        if "customer campaign" in q:
            return self.qa.recommend_customer_campaign()

        if "product campaign" in q:
            return self.qa.recommend_product_campaign()

        if "geographic expansion" in q or "where should we expand" in q:
            return self.qa.recommend_geographic_expansion()

        if "sales action" in q:
            return self.qa.recommend_sales_action()

        if "opportunity action" in q:
            return self.qa.recommend_opportunity_action()

        if ("action" in q and "revenue" in q) or "improve revenue" in q:
            return self.qa.recommend_revenue_action()

        if intent == "recommendation":
            return "\n".join(self.qa.get_all_recommendations())

        # ==========================================
        # EXECUTIVE
        # ==========================================

        if (
            any(word in q for word in self.REVENUE_WORDS)
            and intent == "total"
        ):
            return self.qa.answer_total_revenue()

        if (
            any(
                word in q
                for word in [
                    "customer",
                    "customers",
                    "user",
                    "users",
                    "buyer",
                    "buyers",
                ]
            )
            and intent in ["total", "count"]
            and not any(
                kw in q
                for kw in (
                    "probability",
                    "opportunity",
                    "high value",
                    "high-value",
                    "repeat",
                )
            )
        ):
            return self.qa.answer_total_customers()

        if (
            "total order" in q
            or "total number of order" in q
            or "how many order" in q
        ) and "value" not in q:
            return self.qa.answer_total_orders()

        if "average order value" in q:
            return self.qa.answer_avg_order_value()

        if "seller" in q:
            return self.qa.answer_total_sellers()

        # ==========================================
        # CUSTOMER
        # ==========================================

        if "customer segment" in q or "largest segment" in q:
            return self.qa.answer_top_customer_segment()

        if "average customer revenue" in q or (
            "customer revenue" in q and "average" not in q
        ):
            return self.qa.answer_average_customer_revenue()

        if (
            "average customer order" in q
            or "orders per customer" in q
            or "average number of orders" in q
        ):
            return self.qa.answer_average_customer_orders()

        if "high value customer" in q or "high-value customer" in q:
            return self.qa.answer_high_value_customers()

        if "customer value score" in q:
            return self.qa.answer_customer_value_score()

        # ==========================================
        # PRODUCT
        # ==========================================

        if "category" in q and ("most orders" in q or "orders" in q):
            top = self.qa.get_top_category_by_orders()
            return (
                f"{top['category']} has the most orders "
                f"with {top['orders']:,} orders."
            )

        if any(word in q for word in self.PRODUCT_WORDS) and intent == "top":
            return self.qa.answer_top_category()

        if "items sold" in q or "items have been sold" in q:
            return self.qa.answer_total_items_sold()

        # ==========================================
        # GEOGRAPHIC
        # ==========================================

        if any(word in q for word in self.CITY_WORDS) and intent == "top":
            return self.qa.answer_top_city_revenue()

        if any(word in q for word in self.STATE_WORDS) and intent == "top":
            return self.qa.answer_top_state_revenue()

        if "how many state" in q or "states are represented" in q:
            return self.qa.answer_total_states()

        if "how many cit" in q or "cities are represented" in q:
            return self.qa.answer_total_cities()

        if "total geographic revenue" in q or "geographic revenue" in q:
            revenue = self.qa.get_total_geographic_revenue()
            return f"Total geographic revenue is ₹{revenue:,.2f}."

        # ==========================================
        # REVENUE
        # ==========================================

        if "latest monthly revenue" in q or "latest month" in q:
            revenue = self.qa.get_latest_month_revenue()
            return f"Latest monthly revenue is ₹{revenue:,.2f}."

        if "growth" in q:
            return self.qa.answer_latest_growth()

        if "highest revenue" in q or "best month" in q:
            return f"Best month: {self.qa.get_best_month()}"

        if "lowest revenue" in q or "worst month" in q:
            return f"Worst month: {self.qa.get_worst_month()}"

        if "average monthly revenue" in q or "monthly revenue" in q:
            return self.qa.answer_average_monthly_revenue()

        # ==========================================
        # SALES
        # ==========================================

        if "best sales day" in q:
            return self.qa.answer_best_sales_day()

        if "average daily revenue" in q:
            return self.qa.answer_average_daily_revenue()

        if "average daily order" in q:
            return self.qa.answer_average_daily_orders()

        if "total sales revenue" in q:
            return self.qa.answer_total_sales_revenue()

        if "sales days" in q or "sales history" in q:
            return self.qa.answer_total_sales_days()

        # ==========================================
        # ML
        # ==========================================

        if "high probability customer" in q:
            return self.qa.answer_high_probability_customers()

        if "medium probability customer" in q:
            count = self.qa.get_medium_probability_customers()
            return f"Medium probability customers: {count:,}"

        if "low probability customer" in q:
            count = self.qa.get_low_probability_customers()
            return f"Low probability customers: {count:,}"

        if "purchase probability" in q:
            return self.qa.answer_purchase_probability()

        if "predicted revenue" in q:
            return self.qa.answer_predicted_revenue()

        if "forecast gap" in q:
            gap = self.qa.get_forecast_gap()
            return f"Average forecast gap is ₹{gap:,.2f}."

        # ==========================================
        # OPPORTUNITY
        # ==========================================

        if "high opportunity customer" in q:
            return self.qa.answer_high_opportunity_customers()

        if "medium opportunity customer" in q:
            count = self.qa.get_medium_opportunity_customers()
            return f"Medium opportunity customers: {count:,}"

        if "low opportunity customer" in q:
            count = self.qa.get_low_opportunity_customers()
            return f"Low opportunity customers: {count:,}"

        if "total opportunity score" in q or "opportunity score" in q:
            return self.qa.answer_total_opportunity_score()

        if "repeat customer" in q:
            return self.qa.answer_repeat_customers()

        # ==========================================
        # FALLBACK KEYWORD DETECTION
        # ==========================================

        if any(word in q for word in self.REVENUE_WORDS):
            return self.qa.answer_total_revenue()

        if any(word in q for word in self.CUSTOMER_WORDS):
            return self.qa.answer_total_customers()

        if any(word in q for word in self.PRODUCT_WORDS):
            return self.qa.answer_top_category()

        # ==========================================
        # DEFAULT
        # ==========================================

        return (
            "Sorry, I could not understand the question. "
            "Try asking about revenue, customers, products, "
            "sales, geography, ML insights, or opportunities."
        )

    def detect_intent(self, q):
        q = q.lower()

        if any(word in q for word in ["top", "highest", "best", "largest", "most"]):
            return "top"

        if any(word in q for word in ["total", "overall", "entire"]):
            return "total"

        if any(word in q for word in ["average", "avg", "mean"]):
            return "average"

        if any(word in q for word in ["count", "number", "how many"]):
            return "count"

        if "summary" in q:
            return "summary"

        if any(word in q for word in ["recommend", "recommendation", "suggest"]):
            return "recommendation"

        return "unknown"