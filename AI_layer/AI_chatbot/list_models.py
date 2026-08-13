# LIST_MODELS.PY – PURPOSE, ROLE, AND IMPORTANCE

# `list_models.py` is a utility file used to verify the connection between the project and the Gemini API. It authenticates using the Gemini API key from `config.py`, connects to Google's Gemini platform, and retrieves all AI models available for use.

# The main purpose of this file is to help developers identify valid Gemini models before integrating them into the chatbot. It is useful for debugging API-related issues such as invalid API keys, model availability problems, and SDK configuration errors.

# This file depends on `config.py` for the API key and the Google GenAI SDK for communication with Gemini. It does not interact with the database, business analytics modules, or chatbot workflow.

# The output is displayed only in the terminal as a list of available Gemini models. No files, logs, or data are stored in the project.

# This is a development and testing utility file and is not required for the normal execution of the chatbot once a working Gemini model has been selected.


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
from google import genai

client = genai.Client(
    api_key=GEMINI_API_KEY
)

try:

    models = client.models.list()

    print("\nAVAILABLE MODELS:\n")

    for model in models:
        print(model.name)

except Exception as e:
    print(e)