#bultin
from pinecone import Pinecone, ServerlessSpec

#internal
from config import PINECONE_API_KEY

pc = Pinecone(api_key=PINECONE_API_KEY)
index = pc.Index('relationships-index') # ur creating multiple clients


def query_database(k_num:int,  relationship_embedding: list[float]) -> dict[str, any]:
    assert isinstance(k_num, int)
    assert isinstance(relationship_embedding, list)
    results = index.query(
        vector=relationship_embedding,
        top_k=  k_num,
        include_values=False,
        include_metadata=True)
    return results

