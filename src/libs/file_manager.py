import json

default_json = """{
    "embeddings": []
}
"""

class FileManager:
    """
    A base class for managing file operations.

    Attributes:
        _file_path (str): The path to the file being managed.
        _file (file): The file object used for reading and writing.
    """
    
    def __init__(self, file_path="out/file.txt"):
        self._file_path = file_path
        self._file = open(self._file_path, "r+")
                
    def __del__(self):
        self._file.close()
        
        
class EmbeddingsManager(FileManager):
    """
    A class for managing embeddings stored in a JSON file.

    Attributes:
        Inherits attributes from FileManager.

    Methods:
        initialize_embeddings(): Initialize the embeddings JSON file with default content.
        save_embeddings(embedding): Save an embedding to the JSON file.
        load_embeddings(): Load embeddings from the JSON file.
    """
    
    def __init__(self, file_path="out/embeddings.json"):
        super().__init__(file_path)
        if self._file.read() == "":
            self.initialize_embeddings()
        
    def initialize_embeddings(self):
        self._file.seek(0)
        self._file.write(default_json)
        self._file.flush()
        
    def save_embeddings(self, embedding: dict):
        embeddings = self.load_embeddings()
        embeddings.append(embedding)
        self._file.seek(0)
        self._file.write(json.dumps({"embeddings": embeddings}, indent=4))
        self._file.flush()

    def load_embeddings(self) -> list : 
        self._file.seek(0)
        contents = self._file.read()
        return json.loads(contents)['embeddings']
    