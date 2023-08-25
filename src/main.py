from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

dimentions = 1

connections.connect("default", host="localhost", port="19530")

fields = [
    FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=False, max_length=100),
    FieldSchema(name="random", dtype=DataType.VARCHAR),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dimentions)
]

schema = CollectionSchema(fields, "OpenAPI Embedding paired with text")

embeddings = Collection("Embeddings", schema, consistency_level="Strong")

