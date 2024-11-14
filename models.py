from typing import List, Union, Literal
from pydantic import BaseModel

# Metadata models for entities
class PersonMetadata(BaseModel):
    type: Literal["Person"]
    name: str
    birth_date: str
    death_date: str
    role: str
    contribution: str

class PlaceMetadata(BaseModel):
    type: Literal["Place"]
    name: str
    location: str
    significance: str

class EventMetadata(BaseModel):
    type: Literal["Event"]
    name: str
    date: str
    location: str
    outcome: str
    significance: str

# Metadata model for relationships
class RelationshipMetadata(BaseModel):
    type: Literal["Relationship"]
    relationship_type: str
    entity1_id: str
    entity2_id: str

# Relationship model used in parsing the API response
class RelationshipModel(BaseModel):
    id: str
    metadata: RelationshipMetadata
    text_snippet: str

# Final models used in your application
class FinalEntity(BaseModel):
    id: str
    metadata: Union[PersonMetadata, PlaceMetadata, EventMetadata]
    text_snippet: str

# Response model that includes both entities and relationships
class EntitiesResponseModel(BaseModel):
    entities: List[FinalEntity]
    relationships: List[RelationshipModel]

class FinalRelationship(BaseModel):
    id: str
    metadata: RelationshipMetadata
    text_snippet: str
    embedding: List[float]


class EntityMetadata(BaseModel):
    entity1_id: str
    entity2_id: str
    relationship: str

