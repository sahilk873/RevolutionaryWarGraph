#builtin
from typing import Optional

#external
from openai import OpenAI

#internal
from config import OPENAI_API_KEY

OPENAI_MODEL = "gpt-4o-mini"
client = OpenAI(api_key=OPENAI_API_KEY)

def output_answer_generation(question: str, context: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant specializing in historical relationships."},
            {"role": "user", "content": question},
            {"role": "system", "content": f"Context: {context}"}
        ],
        max_tokens=150,  
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

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

def extract_relationship_type(question: str) -> Optional[str]:
    assert isinstance(question, str), "Input must be a string."
    prompt = (
        f"Given the user's question about the Revolutionary War, identify the relationship type "
        f"that a hypothetical answer would provide. The relationship type should be a concise phrase "
        f"that connects two entities involved in the question.\n\n"
        f"Question: {question}\n"
        f"Relationship Type:"
    )

    # Make a completion request to the OpenAI API
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant that identifies relationship types from user questions."
                    "Extract only the relationship type phrase that would appear in a hypothetical answer such as **was was by** or **was found in**."
                    "Return only a string with alphabetical characters"
                ),
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_tokens=10,  
        temperature=0,   # Deterministic output
        n=1,
    )

    
    relationship_type = response.choices[0].message.content.strip()
    return relationship_type
