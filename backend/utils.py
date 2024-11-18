import json
from models import EntityMetadata

def write_json_list_start(file):
    file.write('[\n')

def write_json_list_end(file):
    file.write('\n]')

def write_json_entry(file, data, is_first_entry):
    if not is_first_entry:
        file.write(',\n')
    json.dump(data, file, indent=4, ensure_ascii=False)

def assign_unique_ids(input_path: str, output_path: str):
    # Load relationships from JSON file
    with open(input_path, 'r') as file:
        relationships = json.load(file)

    # Track used IDs and ensure uniqueness
    used_ids = set()
    for i, relationship in enumerate(relationships):
        original_id = relationship.get('id', f'relationship_{i}')
        unique_id = original_id
        counter = 1

        # Adjust the ID if it's already been used
        while unique_id in used_ids:
            unique_id = f"{original_id}_{counter}"
            counter += 1

        # Set the unique ID and mark it as used
        relationship['id'] = unique_id
        used_ids.add(unique_id)

    # Save updated relationships to a new JSON file
    with open(output_path, 'w') as file:
        json.dump(relationships, file, indent=2)

    print(f"Assigned unique IDs to relationships and saved to '{output_path}'.")

def read_and_split_text(file_path: str) -> list[str]:
    """
    Reads the text file and splits it into sections based on double newlines.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    sections = text.strip().split('\n\n')
    sections = [section.strip() for section in sections if section.strip()]
    return sections


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
        entity1_info = find_entity_by_id(entity_id=entity1_id, entities_data=entities_data)
        entity2_info = find_entity_by_id(entity_id=entity2_id, entities_data=entities_data)

        relationship_string = (
                f"{entity1_info} {relationship} {entity2_info}."
            )
        relationship_strings.append(relationship_string)
     

    return relationship_strings

def produce_context(entity_dict: dict[int, EntityMetadata]) -> list[str]:

    entities_data = load_entities(file_path='structured_entities_output.json')
    relationship_strings = build_relationship_strings(entity_dict=entity_dict, entities_data=entities_data)
    context = []
    for rel_string in relationship_strings:
        context.append(rel_string)
    return context