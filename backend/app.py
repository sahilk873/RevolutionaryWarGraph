# builtin
import os  

# external
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pinecone import Pinecone 

# internal
from utils import produce_context  
from query import query_database
from openai_methods import output_answer_generation, create_embedding , extract_relationship_type
from config import PINECONE_API_KEY 
from models import EntityMetadata  

pc: Pinecone = Pinecone(api_key=PINECONE_API_KEY)  
index = pc.Index('relationships-index')


app = FastAPI()

app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

class QuestionRequest(BaseModel):
    question: str
    num_matches: int = 5 
# Response model for API responses
class QuestionResponse(BaseModel):
    answer: str
    context: list[str]

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("../frontend/templates/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    user_question: str = request.question.strip()
    num_matches: int = request.num_matches

    if not user_question:
        raise HTTPException(status_code=400, detail="Please enter a valid question.")

    
    relationship_type: str = extract_relationship_type(question=user_question)
    relationship_embedding: list[float] = create_embedding(text=relationship_type)
    results = query_database(k_num=num_matches, relationship_embedding=relationship_embedding)

    
    entity_dict: dict[int, EntityMetadata] = {}

    for i, match in enumerate(results['matches']):
            entity = EntityMetadata(entity1_id=match['metadata'].get('entity1_id'), 
                                    entity2_id=match['metadata'].get('entity2_id'), 
                                    relationship=match['metadata'].get('relationship_type'))
            entity_dict[i] = entity

    context: list[str] = produce_context(entity_dict=entity_dict)
    answer: str = output_answer_generation(question=user_question, context=context)

    response = QuestionResponse(
        answer=answer,
        context=context
    )
    return response
