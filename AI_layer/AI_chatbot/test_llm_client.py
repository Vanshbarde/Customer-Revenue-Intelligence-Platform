# TEST_LLM_CLIENT.PY – PURPOSE, ROLE, AND IMPORTANCE

# `test_llm_client.py` is a testing file created to verify that the `llm_client.py` module is working correctly. Its main purpose is to send a sample prompt to Gemini through the LLM Client and check whether a valid AI response is returned.

# This file depends directly on `llm_client.py` and `config.py`. It retrieves the Gemini API key from `config.py`, creates an instance of the `LLMClient` class, sends a test prompt, and displays the generated response in the terminal. Before this file can run successfully, both the Gemini API key and the LLM Client connection must be configured properly.

# The sample question written inside this file is only for testing purposes. In the final chatbot, users will ask their own questions through the chat interface, and those questions will eventually be sent to the LLM Client automatically. The hardcoded prompt is simply used to confirm that the Gemini connection, API key, and response generation process are functioning as expected.

# The output of this file is displayed only in the terminal as a generated AI response. It does not create any files, store data, or interact with the database. This file is mainly a development and debugging utility used to validate the LLM integration before connecting it to the complete chatbot workflow.

# Once the chatbot is fully integrated and tested, this file is rarely used except for troubleshooting or verifying that the Gemini connection is still working correctly.




import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from config import GEMINI_API_KEY
from llm_client import LLMClient

client = LLMClient(
    GEMINI_API_KEY
)

response = client.generate(
    """
    Explain customer retention in simple business language.
    """
)

print(response)

