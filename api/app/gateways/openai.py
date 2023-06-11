from app.utils.logging import logger
import openai
import os
from dotenv import load_dotenv
load_dotenv()


class OpenAIClient:
    def __init__(self, api_key, completions_model, temperature, max_tokens, embedding_model):
        openai.api_key = api_key
        self.openai = openai
        self.completions_model = completions_model
        self.temperature = float(temperature)
        self.max_tokens = int(max_tokens)
        self.embedding_model = embedding_model

    def get_openai_embedding(self, text):
        text = text.replace(r"\s{2,}", " ")

        response = self.openai.Embedding.create(
            input=[text],
            model=self.embedding_engine)['data'][0]['embedding']

        return response

    def complete_text(self, prompt):
        try:
            response = self.openai.ChatCompletion.create(
                model=self.completions_model,
                messages=[
                    # {'role': 'system', 'content': 'You are a personal assistant'},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature)

            answer = response["choices"][0]["message"]["content"].strip()
            utf8_answer = answer.encode("utf-8").decode("utf-8")
            logger.info("Text completion successful")
            return utf8_answer
        except Exception as error:
            logger.error(f"Error completing text: {error}")


client = OpenAIClient(
    api_key=os.environ.get("OPENAI_API_KEY"),
    completions_model=os.environ.get("COMPLETIONS_MODEL", "gpt-3.5-turbo"),
    temperature=os.environ.get("COMPLETIONS_TEMPERATURE", 0.5),
    max_tokens=os.environ.get("COMPLETIONS_MAX_TOKENS", 1000),
    embedding_model=os.environ.get("EMBEDDING_MODEL", "text-embedding-ada-002")
)
