import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ.get("OPENAI_API_KEY")
completions_model = os.environ.get("COMPLETIONS_MODEL")

openai_client = openai
