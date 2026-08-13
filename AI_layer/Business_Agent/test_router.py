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

router = SmartQuestionRouter()

while True:

    question = input("\nQuestion: ")

    if question.lower() == "exit":
        break

    intent = router.detect_intent(question)

    print(f"Intent Detected: {intent}")