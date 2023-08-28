from flask import Flask, render_template, request
from service import AppService

service = AppService()
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

    #use openai to embed text
    #search for similar embeddings
    #return results
    
    return f'You entered: {text_param}'