# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by navigating to the `/backend` directory and running:

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

One note before you delve into your tasks: for each endpoint you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle GET requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle GET requests for all available categories.
4. Create an endpoint to DELETE question using a question ID.
5. Create an endpoint to POST a new question, which will require the question and answer text, category, and difficulty score.
6. Create a POST endpoint to get questions based on category.
7. Create a POST endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a POST endpoint to get questions to play the quiz. This endpoint should take category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422 and 500.

## Endpoints

GET '/categories'
GET '/questions'
GET '/categories/<int:category_id>/questions'
POST '/questions/create'
POST '/questions/search'
POST '/questions/next'
DELETE '/questions/<int:question_id>'

### GET '/categories'

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs.
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```

### GET '/questions'

- Fetches a pagenated list of questions, reguardless from all categories.
  Questions are returned in pages of 10, as configured by `QUESTIONS_PER_PAGE`.
  The default is page 1 and the endpoint will throw a 404 is fails to find any
  questions in the database.
- Request Arguments:
  - `page`: An optional `page` argument that is an int.  This represents the
    page number of questions to be returned.  No argument will default to page
    one.
- Returns:
  - `questions`: A list of question objects for the requested page, of the form:
    ```
    [
      {
        'id': <int_id>,
        'question': <str_question>,
        'answer': <str_answer>,
        'category': <int_category_id>,
        'difficulty': <int_difficulty>
      }
    ]
    ```
  - `total_questions`: The total number of questions available in the database.
  - `categories`: An object with a single key, categories, that contains a
     object of id: category_string key:value pairs.
    ```
    {'id' : 'category_type'}
    ```
  - `current_category`: The current category id.  Defaults to None.

### GET '/categories/<int:category_id>/questions'

- Fetches all questions with the provided `category_id`.  This endpoint returns
  all questions and do not pagenate results.  A `category_id` of 0 can be used
  to return all questions.  It will throw a 404 for unknown categories other
  than 0 and for categories with no questions.
- Request Arguments: None
- Returns:
  - `questions`: A list of question objects in the requested category, of the
    form:
    ```
    [
      {
        'id': <int_id>,
        'question': <str_question>,
        'answer': <str_answer>,
        'category': <int_category_id>,
        'difficulty': <int_difficulty>
      }
    ]
    ```
  - `total_questions`: The total number of questions available in the database.
  - `current_category`: The current category id that was provided as
    `category_id`.

### POST '/questions/create'

- With the provided set of parameters, it creates a new question in the
  database.  It will throw a 400 if any of the request arguments are not
  provided.  It will throw a 404 if that category id does not exist.
- Request Arguments:
  - `category`: An int presenting the id of an existing category.
  - `question`: A string that is the question to be asked.
  - `answer`: A string that is the answer to the question.
  - `difficulty`: An int representing the difficulty of the question, from 1
    to 5.
- Returns:
  - `question`: A string that is the actual question of the new question
    (should equal the one sent in the request).
  - `answer`: A string that is the answer to the new question (should equal
    the one sent in the request).
  - `difficulty`: An int representing the difficulty of the new question
    (should equal the one sent in the request).
  - `category`: An int representing the category id of the new question
    (should equal the one sent in the request).
  - `id`: An int representing the id of the new question.

### POST '/questions/search'

- Fetches a list of questions based on the search term provided.  It will
  return any question for whom the search term is a substring of the question.
  An empty string will return all questions.  This endpoint is not pagenated.
- Request Arguments:
  - `searchTerm`: A string that is the search term to search for.
- Returns:
  - `questions`: A list of questions from all categories that contain the
    search term as a substring.  The list is of the form:
    ```
    [
      {
        'id': <int_id>,
        'question': <str_question>,
        'answer': <str_answer>,
        'category': <int_category_id>,
        'difficulty': <int_difficulty>
      }
    ]
    ```
  - `total_questions`: The total number of questions available in the database.
  - `current_category`: The current category.  Defaults to None.

### POST '/questions/next'

- This is how quizzes are played.  Given there is no quiz object in the
  database, each question is received in succession.
  This endpoints takes a category and a list of questions that were previously
  returned.  This endpoint will return a random question from the remaining
  unanswered questions in the given category.  When there are no more
  questions left, it will return None.
  A category ID of 0 can be used to return all questions.
- Request Arguments:
  - `previous_questions`: An list of question ids (ints) that have already been
    presented in the quiz.
  - `quiz_category`: An object that represents the quiz category.  It has the
    form:
    ```
    'quiz_category': {'type': '<str_category_type>', 'id': '<int_category_id>'}
    ```
    It will throw a 404 if the `int_category_id` is not 0 or a known category
    id.
- Returns:
  - `question`: A single question object that represents the next question. It
    is of the form:
    ```
    {
      'id': <int_id>,
      'question': <str_question>,
      'answer': <str_answer>,
      'category': <int_category_id>,
      'difficulty': <int_difficulty>
    }
    ```

### DELETE '/questions/<int:question_id>'

- Deletes the question with the given question_id.  Throws a 404 if that
  question does not exist.
- Request Arguments: None
- Returns: Only the `success` value for a successful delete.


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
