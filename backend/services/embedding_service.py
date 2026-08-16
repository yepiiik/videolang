from openai import OpenAI

from config import OPENROUTER_API_KEY


client = OpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)


MODEL = "openai/text-embedding-3-small"


def create_embedding(text: str):
    response = client.embeddings.create(
        model=MODEL,
        input=text
    )

    return response.data[0].embedding


def create_embeddings(texts: list[str]):
    if not texts:
        return []

    response = client.embeddings.create(
        model=MODEL,
        input=texts
    )

    embeddings = [None] * len(texts)

    for item in response.data:
        embeddings[item.index] = item.embedding

    return embeddings