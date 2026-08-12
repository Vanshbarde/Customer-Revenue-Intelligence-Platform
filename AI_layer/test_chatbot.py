from business_chatbot import BusinessChatbot

chatbot = BusinessChatbot()

print("\nAI Business Chatbot Ready")
print("Type 'exit' to quit.\n")

while True:

    question = input("You: ")

    if question.lower() == "exit":
        break

    answer = chatbot.answer_question(
        question
    )

    print("\nBot:")
    print(answer)

    print("\n" + "=" * 80 + "\n")

chatbot.close()