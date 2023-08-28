import openai
import dotenv
import json
from file_manager import EmbeddingsManager

dotenv.load_dotenv("../.env")
env_variables = dotenv.get_key(".env", "OPENAI_API_KEY")

openai.api_key = env_variables
    
embeddings_manager = EmbeddingsManager("libs/out/embeddings.json")
lines = []
input_text = input("Enter text to embed ( type :exit() to exit): ")
while True:
    if input_text == ":exit()":
        break
    lines.append(input_text)
    input_text = input("> ")

concated_text = "\n".join(lines)

response = openai.Embedding.create( model="text-embedding-ada-002", input=concated_text)

print(response)
if not isinstance(response, dict):
    print("Error: response is not a dictionary.")
    print("Response: ", response)
    exit(1)

file = open("libs/out/last_embedder_output.json", "w")
file.write(json.dumps(response, indent=4))
file.close()

embeddings_record: dict = {
    "text": concated_text,
    "embedding": list(response["data"][0]["embedding"])
}

embeddings_manager.save_embeddings(embeddings_record)






