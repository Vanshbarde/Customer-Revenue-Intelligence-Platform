import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from qa_router import QARouter

router = QARouter()

while True:

    q = input("\nAsk: ")

    if q.lower() == "exit":
        break

    print("\nAnswer:")
    print(router.route(q))

router.close()