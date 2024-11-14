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

