# builtin
import os  

# external
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pinecone import Pinecone
from hypothetical_answer_generator import extract_relationship_type 
from embedding import create_embedding

# internal
from build_relationship_string import produce_context  
from query import query_database
from answer import output_answer_generation 
from config import PINECONE_API_KEY 
from models import EntityMetadata  # Importing Pydantic model for entity metadata

# Initialize Pinecone
pc: Pinecone = Pinecone(api_key=PINECONE_API_KEY)  # pydantic-settings
index = pc.Index('relationships-index')

# FastAPI app setup
app = FastAPI()

# Mount static files
app.mount("../frontend/static", StaticFiles(directory="static"), name="static")

# Request model for user questions
class QuestionRequest(BaseModel):
    question: str
    num_matches: int = 5  # Default to 5 if not specified

# Response model for API responses
class QuestionResponse(BaseModel):
    answer: str
    context: list[str]

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("templates/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.post("/ask", response_model=QuestionResponse)
async def ask_question(request: QuestionRequest):
    user_question: str = request.question.strip()
    num_matches: int = request.num_matches

    if not user_question:
        raise HTTPException(status_code=400, detail="Please enter a valid question.")

    # Process user question
    relationship_type: str = extract_relationship_type(question=user_question)
    relationship_embedding: list[float] = create_embedding(text=relationship_type)
    results = query_database(k_num=num_matches, relationship_embedding=relationship_embedding)

    # Parse results into Pydantic models
    entity_dict: dict[int, EntityMetadata] = {}

    for i, match in enumerate(results['matches']):
            entity = EntityMetadata(entity1_id=match['metadata'].get('entity1_id'), 
                                    entity2_id=match['metadata'].get('entity2_id'), 
                                    relationship=match['metadata'].get('relationship_type'))
            entity_dict[i] = entity


    # Generate context and answer
    context: list[str] = produce_context(entity_dict=entity_dict)
    answer: str = output_answer_generation(question=user_question, context=context)

    # Return response as a Pydantic model
    response = QuestionResponse(
        answer=answer,
        context=context
    )
    return response
