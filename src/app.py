from flask import Flask, render_template, request
from service import AppService
from embedder import OpenAIEmbedder
from time import time
from pymilvus import SearchResult

service = AppService()
embedder = OpenAIEmbedder()
app = Flask(__name__)


@app.route("/", )
def hello_world():
    return render_template("index.html")

@app.route("/templates/search")
def search():
    return render_template("sections/search.html")

@app.route("/templates/insert")
def insert():
    return render_template("sections/insert.html")

@app.route("/templates/all-embeddings")
def all_embeddings():
    embeddings = '\n'.join([f"<p class='overflow-hidden max-h-24 hover:max-h-max even:text-zinc-400 text-justify' >{record['text']}</p>" for record in service.get_all_embeddings()])        
    return f"""
        <div class="flex gap-2 flex-col items-center">
            {embeddings}
        </div>
        """

@app.route("/api/load-presets")
def load_presets():
    service.import_embeddings()
    return "<p>Loaded</p>"

@app.route("/api/search")
def search_embeddings():
    text_param = request.args.get("text")
    if text_param == None or text_param == "":
        return "Please enter a search query"
    embeddings_dict = embedder.embed_text(text_param, False)
    
    search_params = {
        "metric_type": "L2",
        "params": {"nprobe": 10},
    }
    start_time = time()
    result = service.search_embeddings(embeddings_dict["embeddings"], search_params)
    end_time = time()
    print(f"Search latency: {round((end_time - start_time)*1000)}ms")
    
    to_return = '\n'.join([f"""<div class='even:text-zinc-400 flex items-center flex-col'><p class='overflow-hidden max-h-24 hover:max-h-max text-justify' >{record['text']}</p>
                           <p class='overflow-hidden max-h-24 hover:max-h-max text-justify' >{record['distance']}</p></div>"""
                           for record in result])
    
    return f"""<h3 class='text-center mb-2'>Search duration: {round((end_time - start_time)*1000)}ms</h3>
        <div class="flex gap-1 flex-col items-center">
            <hr class="w-[80%] mb-4"/>
            {to_return}
        </div>
        """
        
@app.route("/api/insert", methods=["POST"])
def insert_embeddings():
    text_param = request.form.get("text")
    if text_param == None or text_param == "":
        return "Please enter the text to insert"
    embedded_text = embedder.embed_text(text_param, True)
    did_succeed = service.insert_embeddings(embedded_text)
    if did_succeed:
        return f"<p class='text-justify'>{embedded_text['embeddings']}</p>"
    return f"<p class='text-justify'>Embedding for '{text_param}' already exists.</p>"