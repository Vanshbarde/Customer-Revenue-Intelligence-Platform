# LLM_CLIENT.PY – PURPOSE, ROLE, AND IMPORTANCE

# `llm_client.py` is the core communication file between the AI chatbot and the Gemini Large Language Model (LLM). Its main purpose is to send prompts to Gemini and receive AI-generated responses. This file acts as the project's gateway to the AI model and is responsible for handling all interactions with Gemini.

# The file contains the `LLMClient` class, which creates a secure connection to Gemini using the API key and provides a `generate()` function for sending prompts and retrieving responses. It also includes error handling to ensure the chatbot does not crash if there is an API or network issue.

# This file depends on the Gemini API key stored in `config.py` and the Google GenAI SDK. It is used by higher-level chatbot components such as the Prompt Builder and Chatbot Engine, which generate prompts and then pass them to the LLM Client for response generation.

# The input to this file is a prompt created by other chatbot modules, and the output is the AI-generated response returned by Gemini. It does not store any data, create files, or interact with the database. All responses are returned directly to the calling module.

# `llm_client.py` is one of the most important files in the project because it provides the actual connection between the chatbot and the Gemini AI model. Without it, the chatbot would not be able to generate intelligent responses.


from google import genai


class LLMClient:

    def __init__(self, api_key):

        self.client = genai.Client(
            api_key=api_key
        )

    def generate(self, prompt):

        try:

            response = self.client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
          )

            return response.text

        except Exception as e:

            return f"LLM Error: {str(e)}"