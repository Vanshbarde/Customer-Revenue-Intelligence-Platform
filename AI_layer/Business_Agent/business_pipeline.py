import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from smart_question_router import SmartQuestionRouter
from qa_router import QARouter
from insights_generator import InsightsGenerator
from recommendation_engine import RecommendationEngine


class BusinessPipeline:

    def __init__(self):

        self.intent_router = SmartQuestionRouter()
        self.qa_router = QARouter()
        self.insights_generator = InsightsGenerator()
        self.recommendation_engine = RecommendationEngine()

    def process_question(self, question):

        intent = self.intent_router.detect_intent(question)

        answer = self.qa_router.route(question)

        insights = self.insights_generator.generate(intent)

        recommendations = self.recommendation_engine.generate(intent)

        response = {
            "intent": intent,
            "answer": answer,
            "insights": insights,
            "recommendations": recommendations
        }

        return response

    def close(self):

        self.qa_router.close()
        self.insights_generator.close()
        self.recommendation_engine.close()


if __name__ == "__main__":

    pipeline = BusinessPipeline()

    print("\nAI Business Pipeline Ready")
    print("Type 'exit' to quit.\n")

    while True:

        question = input("You: ")

        if question.lower() == "exit":
            break

        result = pipeline.process_question(question)

        print("\n" + "=" * 80)

        print("\nINTENT:")
        print(result["intent"])

        print("\nANSWER:")
        print(result["answer"])

        print("\nINSIGHTS:")

        for item in result["insights"]:
            print(f"• {item}")

        print("\nRECOMMENDATIONS:")

        for rec in result["recommendations"]:

            print(f"\nPriority : {rec['priority']}")
            print(f"Title    : {rec['title']}")
            print(f"Action   : {rec['recommendation']}")
            print(f"Impact   : {rec['expected_impact']}")

        print("\n" + "=" * 80)

    pipeline.close()