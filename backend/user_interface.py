# builtin
import os  

# external
from pinecone import Pinecone, ServerlessSpec
from hypothetical_answer_generator import extract_relationship_type 
from embedding import create_embedding
from pydantic import BaseModel

#internal
from build_relationship_string import produce_context  
from query import query_database
from answer import output_answer_generation 
from config import PINECONE_API_KEY 
from models import EntityMetadata

pc: Pinecone = Pinecone(api_key=PINECONE_API_KEY) # pydantic-settings
index = pc.Index('relationships-index')

def main() -> None:
    print("=== Revolutionary War Relationship Type Generator ===\n")
    print("Enter your questions related to the Revolutionary War. Type 'exit' to quit.\n")

    while True:
        user_question: str = input("Your Question: ").strip()

        if user_question.lower() in ['exit', 'quit']:
            print("Exiting the Revolutionary War Chatbot!")
            break

        if not user_question:
            print("Please enter a valid question.\n")
            continue

        relationship_type: str = extract_relationship_type(user_question) # name ur args

        relationship_embedding: list[float] = create_embedding(relationship_type)

        results: dict[str, any] = query_database(3, relationship_embedding)

        entity_dict: dict[int, EntityMetadata] = {}

        for i, match in enumerate(results['matches']):
            entity = EntityMetadata(entity1_id=match['metadata'].get('entity1_id'), 
                                    entity2_id=match['metadata'].get('entity2_id'), 
                                    relationship=match['metadata'].get('relationship_type'))
            entity_dict[i] = entity

        context: list[str] = produce_context(entity_dict)
        
        answer: str = output_answer_generation(user_question, context)

        print(answer)


if __name__ == "__main__":
    main()

'''schema = {
        "type": "object",
        "properties": {
            "entities": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "metadata": {
                            "oneOf": [
                                {"$ref": "#/definitions/PersonMetadata"},
                                {"$ref": "#/definitions/PlaceMetadata"},
                                {"$ref": "#/definitions/EventMetadata"},
                            ]
                        },
                        "text_snippet": {"type": "string"},
                    },
                    "required": ["id", "metadata", "text_snippet"],
                },
            },
            "relationships": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "string"},
                        "metadata": {"$ref": "#/definitions/RelationshipMetadata"},
                        "text_snippet": {"type": "string"},
                    },
                    "required": ["id", "metadata", "text_snippet"],
                },
            },
        },
        "required": ["entities", "relationships"],
        "definitions": {
            "PersonMetadata": {
                "type": "object",
                "properties": {
                    "type": {"enum": ["Person"]},
                    "name": {"type": "string"},
                    "birth_date": {"type": "string"},
                    "death_date": {"type": "string"},
                    "role": {"type": "string"},
                    "contribution": {"type": "string"},
                },
                "required": [
                    "type",
                    "name",
                    "birth_date",
                    "death_date",
                    "role",
                    "contribution",
                ],
            },
            "PlaceMetadata": {
                "type": "object",
                "properties": {
                    "type": {"enum": ["Place"]},
                    "name": {"type": "string"},
                    "location": {"type": "string"},
                    "significance": {"type": "string"},
                },
                "required": ["type", "name", "location", "significance"],
            },
            "EventMetadata": {
                "type": "object",
                "properties": {
                    "type": {"enum": ["Event"]},
                    "name": {"type": "string"},
                    "date": {"type": "string"},
                    "location": {"type": "string"},
                    "outcome": {"type": "string"},
                    "significance": {"type": "string"},
                },
                "required": [
                    "type",
                    "name",
                    "date",
                    "location",
                    "outcome",
                    "significance",
                ],
            },
            "RelationshipMetadata": {
                "type": "object",
                "properties": {
                    "type": {"enum": ["Relationship"]},
                    "relationship_type": {"type": "string"},
                    "entity1_id": {"type": "string"},
                    "entity2_id": {"type": "string"},
                },
                "required": [
                    "type",
                    "relationship_type",
                    "entity1_id",
                    "entity2_id",
                ],
            },
        },
    }
'''