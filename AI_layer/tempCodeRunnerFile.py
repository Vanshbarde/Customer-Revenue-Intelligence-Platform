import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}




# GENINI API KEY

from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)