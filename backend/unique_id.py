import json

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

# Usage
assign_unique_ids('structured_relationships_output.json', 'structured_relationships_unique_ids.json')
