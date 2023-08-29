from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
    SearchFuture
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
        
    def insert_embeddings(self, embeddings_record):
        all_embeddings = self.collection.query(
            expr = "pk >= '0'", 
            output_fields = ["text"]
        )
        all_texts = []
        for record in all_embeddings:
            all_texts.append(record["text"])
        if embeddings_record["text"] in all_texts:
            return False            
        self.collection.insert(embeddings_record) 
        return True   
    
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
            
    def search_embeddings(self, vectors_to_search, search_params) -> list[dict]:
        result = self.collection.search(
            data=[vectors_to_search],
            param=search_params,
            anns_field="embeddings",
            limit=10,
            output_fields=["text"]
        )
        
        if isinstance(result, SearchFuture):
            result = result.result()
        
        to_return = []
        
        for entity in result[0]:
            to_return.append({
                "text": entity.entity.get("text"),
                "distance": entity.distance
            })
        
        return to_return
        
    
if __name__ == "__main__":
    print("Should not be run as this is a library.")
