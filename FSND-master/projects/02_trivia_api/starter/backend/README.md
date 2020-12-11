# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 

## Tasks
1. Use Flask-CORS to enable cross-domain requests and set response headers. COMPLETE
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories. COMPLETE
3. Create an endpoint to handle GET requests for all available categories. COMPLETE 
4. Create an endpoint to DELETE question using a question ID. COMPLETE
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score. COMPLETE  
6. Create a POST endpoint to get questions based on category. COMPLETE 
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question. DONE
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. COMPLETE
9. Create error handlers for all expected errors including 400, 404, 422 and 500.  COMPLETE

## MODIFICATIONS beyond the base requirements for the backend include: 
1. Added ability to CREATE new questions
2. Added Player and Score objects to database.  Player table contains player id and name.  Score table contains id, value, player id, and category id.
3. Added endpoint to add new players (name) and get new players (id, name, scores), and to delete players and associated scores.
4. Updated Question model to include a ratings column (integer).  
5. Updated Get question and add new question endpoints to include rating.
6. trivia.psql contains updated database model and mock data.
7. 
   
## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

## API Documentation
The documentation for the Trivia App API can be found in the file: 
> [TriviaApp_API_DOC.md](./TriviaApp_API_Doc.md).