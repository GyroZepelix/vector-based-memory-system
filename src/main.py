from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

from libs.file_manager import EmbeddingsManager

dimentions = 1536

connections.connect("default", host="localhost", port="19530")

embeddings_field_schemas = [
    FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=True, max_length=100),
    FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=10000),
    FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=dimentions)
]
schema = CollectionSchema(embeddings_field_schemas, "OpenAPI Embedding paired with text")
embeddings_collection = Collection("Embeddings", schema)

index_params = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {
        "nlist": dimentions
    }
}

embeddings_collection.create_index(
  field_name="embeddings",
  index_params=index_params,
  index_name="test"
)

embeddings_manager = EmbeddingsManager("src/out/embeddings.json")
embeddings_records = embeddings_manager.load_embeddings()

data = []
for record in embeddings_records:
    data.append({
        "text": record["text"],
        "embeddings": record["embedding"]
    })

# data = [
#     {
#         "text": "This is a test",
#         "embeddings": [1, 2, 3, 4, 5]
#     },
# ]

print(embeddings_collection.insert(data))

