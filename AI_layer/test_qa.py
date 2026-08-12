from qa_router import QARouter

router = QARouter()

while True:

    q = input("\nAsk: ")

    if q.lower() == "exit":
        break

    print("\nAnswer:")
    print(router.route(q))

router.close()