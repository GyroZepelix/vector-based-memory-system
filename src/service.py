from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

from file_manager import EmbeddingsManager

class AppService:
      
    def __init__(self):
        connections.connect("default", host="localhost", port="19530")
        self.dimentions = 1536
        self._create_schema()
        self.collection = Collection("Embeddings", self.schema)
        self._create_index()
        self.collection.load()
        
        
    def _create_schema(self):
        embeddings_field_schemas = [
            FieldSchema(name="pk", dtype=DataType.VARCHAR, is_primary=True, auto_id=True, max_length=100),
            FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=10000),
            FieldSchema(name="embeddings", dtype=DataType.FLOAT_VECTOR, dim=self.dimentions)
        ]
        self.schema = CollectionSchema(embeddings_field_schemas, "OpenAPI Embedding paired with text")
    
    def _create_index(self):
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "L2",
            "params": {
                "nlist": self.dimentions
            }
        }
        self.collection.create_index(
            field_name="embeddings",
            index_params=index_params,
            index_name="test"
        )
        
    def __del__(self):
        connections.disconnect("default")
        
    def get_all_embeddings(self):
        return self.collection.query(
            expr = "pk >= '0'", 
            output_fields = ["text", "embeddings"]
        )
        
    def import_embeddings(self):
        embeddings_manager = EmbeddingsManager("src/out/embeddings.json")
        embeddings_records = embeddings_manager.load_embeddings()
        all_embeddings = self.collection.query(
            expr = "pk >= '0'", 
            output_fields = ["text"]
        )
        all_texts = []
        for record in all_embeddings:
            all_texts.append(record["text"])        
        data = []
        for record in embeddings_records:
            if record["text"] in all_texts:
                continue
            data.append({
                "text": record["text"],
                "embeddings": record["embedding"]
            })
        if len(data) > 0:
            self.collection.insert(data)
        else:
            print("No new embeddings to import.")
