# processing.py

# Built-in
import json
from typing import Tuple

# External
from openai import OpenAI
from pydantic import BaseModel

# Internal
from openai_methods import create_embedding
from models import (
    PersonMetadata,
    PlaceMetadata,
    EventMetadata,
    RelationshipMetadata,
    FinalEntity,
    FinalRelationship,
    EntitiesResponseModel, 
)
from config import OPENAI_API_KEY, OPENAI_MODEL

# Initialize OpenAI client
if not OPENAI_API_KEY:
    raise ValueError("Please set the OPENAI_API_KEY environment variable.")
client = OpenAI(api_key=OPENAI_API_KEY)

def process_section(
    section_text: str, entity_id_to_name: dict[str, str]
) -> Tuple[list[FinalEntity], list[FinalRelationship]]:
    assert isinstance(section_text, str), "---"
    """
    Processes a section of text to extract entities and relationships.

    Args:
        section_text (str): The text section to process.
        entity_id_to_name (Dict[str, str]): A mapping from entity IDs to their names.

    Returns:
        Tuple[List[FinalEntity], List[FinalRelationship]]: Lists of extracted entities and relationships.
    """
    # Define the JSON schema for structured outputs
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that extracts entities and relationships from text about the Revolutionary War. "
                "For each **entity**, provide its **'id'**, **'metadata'**, and **'text_snippet'** (the exact text from which the entity was extracted). "
                "For each **relationship**, provide its **'id'**, **'metadata'**, and **'text_snippet'** (the exact text from which the relationship was extracted). "
                "For relationships, the **'relationship_type'** should be the **exact phrase from the text** that connects the two entities, "
                "such as **'was won by'**, **'took place near'**, or phrases commonly used in answers like **'led by'**, **'occurred in'**, **'resulted in'**, **'fought between'**, etc. "
                "These relationships will be used to compare with **embeddings of hypothetical answers to questions** in a database, so **extract relationships in a way that they represent how such answers would phrase them**. "
                "Use the following metadata schemas for entities and relationships:\n\n"
                "Only extract entities of types **'Person'**, **'Place'**, or **'Event'** and their relationships. "
                "Do not extract chapter titles, section titles, or similar non-entity text."
            ),
        },
        {"role": "user", "content": section_text},
    ]

    response = client.beta.chat.completions.parse(
        model=OPENAI_MODEL,
        messages=messages,
        response_format=EntitiesResponseModel,  # Pass EntitiesResponseModel class
    )

    # Acces the parsed lists of entities and relationships
    entities_data = response.choices[0].message.parsed.entities # type hint
    relationships_data = response.choices[0].message.parsed.relationships

    final_entities: list[FinalEntity] = []
    final_relationships: list[FinalRelationship] = []

    # Process entities
    for entity in entities_data:
        metadata = entity.metadata.dict()
        entity_type = metadata["type"]

        if entity_type == "Person":
            metadata_obj = PersonMetadata(**metadata)
            final_entity = FinalEntity(
                id=entity.id,
                metadata=metadata_obj,
                text_snippet=entity.text_snippet,
            )
            final_entities.append(final_entity)
            entity_id_to_name[final_entity.id] = metadata_obj.name

        elif entity_type == "Place":
            metadata_obj = PlaceMetadata(**metadata)
            final_entity = FinalEntity(
                id=entity.id,
                metadata=metadata_obj,
                text_snippet=entity.text_snippet,
            )
            final_entities.append(final_entity)
            entity_id_to_name[final_entity.id] = metadata_obj.name

        elif entity_type == "Event":
            metadata_obj = EventMetadata(**metadata)
            final_entity = FinalEntity(
                id=entity.id,
                metadata=metadata_obj,
                text_snippet=entity.text_snippet,
            )
            final_entities.append(final_entity)
            entity_id_to_name[final_entity.id] = metadata_obj.name

        else:
            # Unknown entity type; skip
            continue

    # Process relationships
    for relationship in relationships_data:
        metadata = relationship.metadata.model_dump()
        metadata_obj = RelationshipMetadata(**metadata)

        final_relationship = FinalRelationship(
            id=relationship.id,
            metadata=metadata_obj,
            text_snippet=relationship.text_snippet,
            embedding=[],  # Placeholder; to be filled later
        )
        final_relationships.append(final_relationship)

    return final_entities, final_relationships

def generate_relationship_embedding(relationship: FinalRelationship) -> None:
    # Embed only the 'relationship_type' string
    embedding_vector = create_embedding(text=relationship.metadata.relationship_type)
    relationship.embedding = embedding_vector
