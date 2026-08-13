# # TEST_CONTEXT_BUILDER.PY – PURPOSE AND IMPORTANCE

# The `test_context_builder.py` file is a testing and validation file created during the development phase of the AI chatbot. Its purpose is not to be used by the end user, but to help developers verify that the Context Builder is working correctly before integrating it into the final chatbot system.

# This file manually sends sample questions to the Context Builder and displays the generated context. By doing this, developers can check whether the Context Builder is correctly identifying topics, retrieving business metrics, classifying question types, and generating the expected output.

# The questions written inside this file are only test cases. They are not the actual questions that users will ask in the final application. These questions are intentionally chosen to represent different categories of queries such as revenue, customers, geography, opportunities, machine learning, and general knowledge. The goal is to ensure that the Context Builder behaves correctly for each type of question.

# For example:

# * "Why is revenue falling?" tests revenue context generation.
# * "How many customers do we have?" tests customer context generation.
# * "Which city generates the most revenue?" tests geographic context generation.
# * "What is our predicted revenue?" tests machine learning prediction context.
# * "Who are our high opportunity customers?" tests opportunity analysis context.
# * "What is machine learning?" tests general knowledge detection.

# In the actual project, users will never interact with this file. Instead, the workflow will be:

# User Question → Chat Interface → Context Builder → Prompt Builder → Gemini → Response

# The user's question can be anything related to the business or even a general knowledge query. The chatbot will automatically receive that question and pass it to the Context Builder. There is no need to manually write questions inside the code during normal operation.

# The reason this test file exists is because developers need a way to verify that the Context Builder works correctly before connecting it to the complete chatbot pipeline. It helps identify errors, missing functions, incorrect classifications, data formatting issues, and integration problems at an early stage.

# Without this testing file, debugging would become much more difficult because developers would have to run the entire chatbot system every time they wanted to check a small change in the Context Builder.

# The dependency flow for this file is:

# Business QA Engine → Context Builder → Test Context Builder

# This means the test file depends on the Context Builder, and the Context Builder itself depends on the Business QA Engine.

# In summary, `test_context_builder.py` is a development and debugging tool used to validate the functionality of the Context Builder. The sample questions inside it are only testing examples and are not part of the final user experience. In the deployed chatbot, real users will ask their own questions, and those questions will automatically follow the chatbot pipeline without requiring any manual input in the code.


import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

from context_builder import ContextBuilder

builder = ContextBuilder()

questions = [

    "Why is revenue falling?",

    "How many customers do we have?",

    "Which city generates the most revenue?",

    "What is our predicted revenue?",

    "Who are our high opportunity customers?",

    "What is machine learning?"
]

for q in questions:

    print("\n" + "=" * 60)

    print("QUESTION:")
    print(q)

    print("\nCONTEXT:")

    print(
        builder.get_context(q)
    )