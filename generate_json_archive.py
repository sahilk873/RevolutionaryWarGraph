#builtin
import json

#external
from pydantic import BaseModel
from typing import Optional
from openai import OpenAI

#internal
from embedding import create_embedding
from make_sections import read_and_split_text

class EntityMetadata(BaseModel):
    type: str  # e.g., Person, Place, Event, Document
    name: str
    date: Optional[str] = None
    location: Optional[str] = None
    outcome: Optional[str] = None
    significance: Optional[str] = None
    role: Optional[str] = None
    appointed_by: Optional[str] = None
    year_appointed: Optional[str] = None
    contribution: Optional[str] = None
    birth_date: Optional[str] = None
    death_date: Optional[str] = None
    adoption_date: Optional[str] = None
    adopted_by: Optional[str] = None
    purpose: Optional[str] = None

class EntityResponse(BaseModel):
    id: str
    metadata: EntityMetadata
    text_snippet: str  # Text from which the entity was extracted

class EntitiesResponse(BaseModel):
    entities: list[EntityResponse]

# Define Pydantic model for final output including embedding
class FinalEntity(BaseModel):
    id: str
    metadata: EntityMetadata
    text_snippet: str
    embedding: list[float]


# Initialize OpenAI client with your API key
api_key = "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"
client = OpenAI(api_key=api_key)



def process_section(section_text: str) -> EntitiesResponse:
    """
    Sends a section of text to the OpenAI API to extract entities in a structured format.
    """
    # Define the JSON schema for structured outputs using Pydantic models
    # Note: 'embedding' is excluded from this schema
    schema = EntitiesResponse.model_schema_json(indent=2)

    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that extracts entities from text about the Revolutionary War. "
                "For each entity, provide its 'id', 'metadata', and 'text_snippet' (the exact text from which the entity was extracted) "
                "in structured JSON format as per the provided schema. "
                "Chapter titles, section titles, and similar things are not examples of entities.\n\n"
                f"Schema:\n{schema}"
            )
        },
        {"role": "user", "content": section_text}
    ]

    response = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",  # Ensure this model supports Structured Outputs
        messages=messages,
        response_format=EntitiesResponse
    )

    # Retrieve the structured output
    output = response.choices[0].message.parsed
    return output



def main():
    file_path = 'revolution.txt' 
    sections = read_and_split_text(file_path)
    output_file = 'structured_entities_output.json'

    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write('[\n')  # Start the JSON array

        first_entity = True  # Flag to handle commas between JSON objects

        for i, section in enumerate(sections):
            print(f"Processing section {i+1}/{len(sections)}...")
            entities_response = process_section(section)

            if entities_response.entities:
                for entity_resp in entities_response.entities:
                    # Generate embedding for the text_snippet
                    embedding_vector = create_embedding(entity_resp.text_snippet)

                    # Create FinalEntity with embedding
                    final_entity = FinalEntity(
                        id=entity_resp.id,
                        metadata=entity_resp.metadata,
                        text_snippet=entity_resp.text_snippet,
                        embedding=embedding_vector
                    )

                    # Prepare the JSON entry
                    entity_dict = final_entity.model_dump()

                    # Write comma if not the first entity
                    if not first_entity:
                        outfile.write(',\n')
                    else:
                        first_entity = False

                    # Dump the entity JSON
                    json.dump(entity_dict, outfile, indent=4, ensure_ascii=False)
            else:
                print(f"No entities extracted from section {i+1}.")

        outfile.write('\n]')  # End the JSON array

    print(f"Processing complete. Output saved to '{output_file}'.")

if __name__ == "__main__":
    main()