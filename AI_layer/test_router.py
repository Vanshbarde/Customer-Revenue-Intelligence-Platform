from smart_question_router import SmartQuestionRouter

router = SmartQuestionRouter()

while True:

    question = input("\nQuestion: ")

    if question.lower() == "exit":
        break

    intent = router.detect_intent(question)

    print(f"Intent Detected: {intent}")