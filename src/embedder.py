import openai
import dotenv
import json
from file_manager import EmbeddingsManager

class OpenAIEmbedder:
    """
    A utility class for embedding text using the OpenAI Embedding API.

    This class initializes the OpenAI API key and provides methods to embed text
    using the 'text-embedding-ada-002' model.
    """
    embeddings_memory = {}
    
    def __init__(self) -> None:
        dotenv.load_dotenv("../.env")
        env_variables = dotenv.get_key(".env", "OPENAI_API_KEY")
        openai.api_key = env_variables
        
    def embed_text(self, text: str, save_to_json: bool = True) -> dict:
        """
        Embeds the given text using the OpenAI Embedding API model 'text-embedding-ada-002'.

        Args:
            text (str): The input text to be embedded.
            save_to_json (bool, optional): Whether to save the embedding record to a JSON file. Default is True.

        Returns:
            dict: A dictionary containing the embedded text and its associated embedding.

        Raises:
            Exception: If the response from the OpenAI API is not a dictionary.

        Example:
            instance = OpenAIEmbedder()
            embeddings_record = instance.embed_text("Hello, world!")
            print(embeddings_record)
        """
        if self.embeddings_memory.__contains__(text):
            print(f"{text} already embedded.")
            return self.embeddings_memory[text]
        response = openai.Embedding.create( model="text-embedding-ada-002", input=text)
        if not isinstance(response, dict):
            print("Error: response is not a dictionary.")
            print("Response: ", response)
            raise Exception("Error: response is not a dictionary.")
        print(f"{text} successfully embedded.")
        embeddings_record: dict = {
            "text": text,
            "embeddings": list(response["data"][0]["embedding"])
        }
        self.embeddings_memory[text] = embeddings_record
        if save_to_json:
            embeddings_manager = EmbeddingsManager("src/out/embeddings.json")
            embeddings_manager.save_embeddings(embeddings_record)
        return embeddings_record
        
        
    
    def embed_text_tui(self):
        lines = []
        input_text = input("Enter text to embed ( type :exit() to exit): ")
        while True:
            if input_text == ":exit()":
                break
            lines.append(input_text)
            input_text = input("> ")
        concated_text = "\n".join(lines)
        self.embed_text(concated_text)
        
if __name__ == "__main__":
    embedder = OpenAIEmbedder()
    embedder.embed_text_tui()
        



