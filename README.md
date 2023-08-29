# Vector-Based Memory System

The aim of this project was to explore and prototype a novel long-term memory solution for Language Models (LLMs). The core concept involves storing text as embedded vectors within a database, facilitating efficient text retrieval through vector search algorithms. This approach enables the storage of substantial data volumes within a compact space while ensuring rapid search capabilities.

The workflow is straightforward: users input a sentence, which is then transformed into an embedded format using a pre-trained model. This embedded representation is subsequently stored within a vector-based database. The database facilitates searches for similar sentences, returning the most closely related matches. Users can then choose the closest match and view the corresponding sentence.

To provide a practical demonstration, a sample dataset is included and can be accessed through the provided web interface.

## Technologies

- [Milvus](https://milvus.io/)
- [OpenAPI](https://swagger.io/specification/)
- [Docker](https://www.docker.com/)
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/)
- [HTMX](https://htmx.org/)
- [Tailwind CSS](https://tailwindcss.com/)

## Installation

1. Clone the repository.
2. Change into the project directory `cd vector-database`.
3. Install dependencies with `pip -r requirements.txt`.

## Usage

1. Run the [milvus server](http://localhost:8000) with `docker-compose up`.
2. Run the [web server](http://localhost:5000) with 
   1. `flask --app=src/run run` or 
   2. `python3 -m flask --app src/app.py run`.
3. Access the [web interface](http://localhost:5000) in your browser `http://localhost:5000`.

> Bonus: Import the provided dataset by clicking the 'Load presets' button

## Contributing

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make your changes and commit them with descriptive commit messages.
4. Push your changes to your fork.
5. Submit a pull request to the original repository.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).