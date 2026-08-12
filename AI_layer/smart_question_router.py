class SmartQuestionRouter:

    def __init__(self):

        self.intent_keywords = {

            "revenue": [
                "revenue",
                "growth",
                "income",
                "earning",
                "turnover",
                "profit"
            ],

            "customer": [
                "customer",
                "segment",
                "buyer",
                "loyal",
                "retention"
            ],

            "product": [
                "product",
                "category",
                "item",
                "inventory"
            ],

            "sales": [
                "sales",
                "order",
                "daily sales",
                "monthly sales"
            ],

            "geographic": [
                "state",
                "city",
                "region",
                "location",
                "geographic"
            ],

            "ml": [
                "prediction",
                "forecast",
                "probability",
                "model",
                "purchase probability"
            ],

            "opportunity": [
                "opportunity",
                "cross sell",
                "upsell",
                "high value",
                "target customer"
            ],

            "executive": [
                "overview",
                "kpi",
                "business performance",
                "executive"
            ]
        }

    def detect_intent(self, question):

        question = question.lower()

        for intent, keywords in self.intent_keywords.items():

            for keyword in keywords:

                if keyword in question:

                    return intent

        return "executive"