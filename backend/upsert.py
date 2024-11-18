#builtin
import json

#external
import pinecone
from pinecone import Pinecone, ServerlessSpec

#internal
from config import INDEX_NAME, EMBEDDING_DIMENSION, PINECONE_API_KEY

# Initialize Pinecone client
pc: Pinecone = Pinecone(api_key=PINECONE_API_KEY)

def create_or_connect_index() -> pinecone.Index:
    try:
        pc.create_index(
            name=INDEX_NAME,
            dimension=EMBEDDING_DIMENSION,
            metric="cosine", 
            spec=ServerlessSpec(
                cloud="aws",
                region="us-east-1"
            )
        )
    except pinecone.core.openapi.shared.exceptions.PineconeApiException as e:
        if "ALREADY_EXISTS" in str(e):
            print(f"Index '{INDEX_NAME}' already exists. Connecting to it.")
        else:
            raise e

    return pc.Index(INDEX_NAME)

def sanitize_id(vector_id: str) -> str:
    return vector_id.encode('ascii', errors='ignore').decode()

def upsert_relationships(index: pinecone.Index, relationships: list[dict], batch_size: int = 25) -> None:
    vectors: list[dict] = []
    for relationship in relationships:
        vector: dict = {
            'id': sanitize_id(vector_id=relationship['id']),
            'values': relationship['embedding'],
            'metadata': relationship['metadata']
        }
        vectors.append(vector)

    # Upsert in batches
    for i in range(0, len(vectors), batch_size):
        batch: list[dict] = vectors[i:i + batch_size]
        index.upsert(vectors=batch)
        print(f"Upserted batch {i // batch_size + 1} with {len(batch)} vectors.")

    print(f"Successfully upserted {len(vectors)} relationships into Pinecone index '{INDEX_NAME}'.")

def load_relationships(json_path: str) -> list[dict]:
    with open(json_path, 'r') as file:
        relationships: list[dict] = json.load(file)
    print(f"Loaded {len(relationships)} relationships from '{json_path}'.")
    return relationships

def main() -> None:
    index: pinecone.Index = create_or_connect_index()
    relationships: list[dict] = load_relationships(json_path='structured_relationships_unique_ids.json')  
    upsert_relationships(index=index, relationships=relationships)
    index = pc.Index(INDEX_NAME)
    print(index.describe_index_stats())

if __name__ == "__main__":
    main()
