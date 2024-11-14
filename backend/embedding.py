#external
from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def create_embedding(text: str) -> list[float]:
    assert isinstance(text, str), "Input must be a string."
    """
    Generates an embedding vector for the given text using OpenAI's embedding model.
    """
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"
    )
    return response.data[0].embedding