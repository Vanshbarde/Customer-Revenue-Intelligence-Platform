from dashboard_context import DASHBOARD_CONTEXT
from insights_generator import InsightsGenerator
from recommendation_engine import RecommendationEngine
from smart_question_router import SmartQuestionRouter


class BusinessChatbot:

    def __init__(self):

        self.insights_generator = InsightsGenerator()
        self.recommendation_engine = RecommendationEngine()
        self.router = SmartQuestionRouter()

    def close(self):

        self.insights_generator.close()
        self.recommendation_engine.close()

    def answer_question(self, user_question):

        # Detect Intent
        intent = self.router.detect_intent(
            user_question
        )

        # Get Dashboard Context
        context = DASHBOARD_CONTEXT.get(
            intent,
            {}
        )

        # Get Insights
        insights = self.insights_generator.generate(
            intent
        )

        # Get Recommendations
        recommendations = self.recommendation_engine.generate(
            intent
        )

        response = []

        response.append(
            f"Detected Topic: {intent.upper()}"
        )

        response.append("")

        response.append(
            f"Question: {user_question}"
        )

        response.append("")

        if "description" in context:

            response.append(
                f"Purpose: {context['description']}"
            )

            response.append("")

        response.append(
            "Key Insights:"
        )

        for insight in insights[:5]:

            response.append(
                f"• {insight}"
            )

        response.append("")

        response.append(
            "Recommended Actions:"
        )

        for rec in recommendations[:3]:

            response.append(
                f"• {rec['title']}"
            )

            response.append(
                f"  Action: {rec['recommendation']}"
            )

        return "\n".join(response)