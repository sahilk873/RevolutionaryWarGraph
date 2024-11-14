#internal
from config import (
    INPUT_FILE_PATH,
    ENTITIES_OUTPUT_FILE,
    RELATIONSHIPS_OUTPUT_FILE,
)
from models import FinalEntity, FinalRelationship
from processing import process_section, generate_relationship_embedding
from utils import write_json_list_start, write_json_list_end, write_json_entry
from make_sections import read_and_split_text

def main():
    sections = read_and_split_text(INPUT_FILE_PATH)

    # Initialize entity ID to name mapping
    entity_id_to_name: dict[str, str] = {}

    # Open output files
    with open(ENTITIES_OUTPUT_FILE, 'w', encoding='utf-8') as entities_outfile, \
         open(RELATIONSHIPS_OUTPUT_FILE, 'w', encoding='utf-8') as relationships_outfile:

        write_json_list_start(entities_outfile)
        write_json_list_start(relationships_outfile)

        first_entity = True
        first_relationship = True

        for i, section in enumerate(sections):
            print(f"Processing section {i+1}/{len(sections)}...")
            final_entities, final_relationships = process_section(section, entity_id_to_name)

            # Process entities
            if final_entities:
                for entity in final_entities:
                    entity_dict = entity.dict()
                    write_json_entry(entities_outfile, entity_dict, first_entity)
                    first_entity = False
            else:
                print(f"No entities extracted from section {i+1}.")

            # Process relationships
            if final_relationships:
                for relationship in final_relationships:
                    generate_relationship_embedding(relationship)
                    relationship_dict = relationship.dict()
                    write_json_entry(relationships_outfile, relationship_dict, first_relationship)
                    first_relationship = False
            else:
                print(f"No relationships extracted from section {i+1}.")

        write_json_list_end(entities_outfile)
        write_json_list_end(relationships_outfile)

    print(f"Processing complete. Entities saved to '{ENTITIES_OUTPUT_FILE}' and relationships saved to '{RELATIONSHIPS_OUTPUT_FILE}'.")

if __name__ == "__main__":
    main()
