import json
from models import EntityMetadata

def load_entities(file_path):
    """Loads entities JSON data from a file."""
    with open(file_path, 'r') as file:
        return json.load(file)

def find_entity_by_id(entity_id, entities_data):
    """Searches for an entity by its ID in the list of entities data."""
    for entity in entities_data:
        if entity['id'].lower() == entity_id.lower():  # Match case-insensitively
            return entity
    return None

def build_relationship_strings(entity_dict, entities_data):
    """Constructs a relationship string for each entry in entity_dict using entities_data."""
    relationship_strings = []

    for _ , entity in entity_dict.items():
        entity1_id, entity2_id, relationship = entity.entity1_id, entity.entity2_id, entity.relationship

        # Fetch entity info from the JSON data
        entity1_info = find_entity_by_id(entity1_id, entities_data)
        entity2_info = find_entity_by_id(entity2_id, entities_data)

        relationship_string = (
                f"{entity1_info} {relationship} {entity2_info}."
            )
        relationship_strings.append(relationship_string)
     

    return relationship_strings

def produce_context(entity_dict: dict[int, EntityMetadata]) -> list[str]:

    entities_data = load_entities('structured_entities_output.json')
    relationship_strings = build_relationship_strings(entity_dict, entities_data)
    context = []
    for rel_string in relationship_strings:
        context.append(rel_string)
    return context
