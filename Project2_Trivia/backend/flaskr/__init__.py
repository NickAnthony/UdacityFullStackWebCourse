import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

    '''
    @DONE: Use the after_request decorator to set Access-Control-Allow
    '''
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response


    '''
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    '''
    def get_formatted_categories():
        categories = Category.query.all()
        formatted_categories = {c.id:c.type for c in categories}
        return formatted_categories

    def get_default_category():
        categories = Category.query.all()
        default_category = categories[0].id if categories else None
        return default_category

    @app.route('/categories', methods=['GET'])
    def get_categories():
        # TODO: Implement error handling here
        formatted_categories = get_formatted_categories()
        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    '''
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    def paginate_questions(requested_page=1):
        '''Returns a pagenated list of formated books of size QUESTIONS_PER_PAGE.
        '''
        start = (requested_page - 1)*QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.all()
        formatted_questions = [q.format() for q in questions]
        return start, end, formatted_questions

    @app.route('/questions', methods=['GET'])
    def get_questions():
        # Handle cases where no json is even passed
        if not request.get_json():
            requested_page = 1
        else:
            requested_page = request.get_json().get('page', 1)
        # TODO: Implement error handling here
        start, end, formatted_questions = paginate_questions(requested_page)
        formatted_categories = get_formatted_categories()
        default_current_category = get_default_category()
        return jsonify({
            'success': True,
            'questions': formatted_questions[start:end],
            'total_questions': len(formatted_questions),
            'categories': formatted_categories,
            'current_category': default_current_category
        })

    '''
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        # TODO: Implement error handling here
        error_occured = False
        question_to_delete = Question.query.get(question_id)
        if not question_to_delete:
            error_occured = True
            ## TODO: Replace this with abort
            raise Exception("Venue with id %d not found in the DB" % venue_to_delete)
        question_to_delete.delete()
        return jsonify({
            'success': (not error_occured)
        })

    '''
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''

    @app.route('/questions/create', methods=['POST'])
    def create_question():
        error_occured = False
        request_json = request.get_json()
        # TODO: Implement ERROR handling here for incorrect/incomplete inputs
        category = Category.query.get(request_json.get('category', 1))
        if category is None:
            # TODO: Throw error
            return
        new_question = Question(
            question = request_json.get('question', ''),
            answer = request_json.get('answer', ''),
            difficulty = request_json.get('difficulty', 1),
            category = category.id
        )
        new_question.insert()
        # We can get the id because the object has been flushed.
        return jsonify({
            'success': True,
            'question': new_question.question,
            'answer': new_question.answer,
            'difficulty': new_question.difficulty,
            'category': new_question.category,
            'id': new_question.id
        })


    '''
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''
    @app.route('/questions/search', methods=['POST'])
    def search_question():
        search_term = request.get_json().get('searchTerm', '')
        # Do a SQL query using question LIKE %search_term%
        formatted_search_term = "%{}%".format(search_term)
        # Search questions for the search term.
        search_results = Question.query.filter(
            Question.question.ilike(formatted_search_term)
        ).all()
        formatted_search_results = [q.format() for q in search_results]
        total_questions = len(Question.query.all())
        default_current_category = get_default_category()
        return jsonify({
            'success': True,
            'questions': formatted_search_results,
            'total_questions': total_questions,
            'current_category': default_current_category
        })

    '''
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_for_category(category_id):
        if category_id == 0:
            # Get all questions - this is the "ALL"
            category_questions = Question.query.all()
        else:
            # Get all questions for the given category id
            category_questions = Question.query.filter(
                Question.category == category_id
            ).all()
        formatted_category_questions = [q.format() for q in category_questions]
        _, _, formatted_questions = paginate_questions()
        total_questions = len(Question.query.all())
        return jsonify({
            'success': True,
            'questions': formatted_category_questions,
            'total_questions': total_questions,
            'current_category': category_id
        })


    '''
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''
    def pick_random_question(question_list):
        if len(question_list) <= 0:
            return None
        return random.choice(question_list)

    @app.route('/questions/next', methods=['POST'])
    def get_next_question_in_game():
        # Example initial state:
        #   {'previous_questions': [], 'quiz_category': {'type': 'Science', 'id': 'id'}
        quiz_category = request.get_json().get('quiz_category', None)
        select_from_category = None
        if quiz_category is None:
            # TODO: Throw error
            print("quiz_category not provided")
            return
        if not quiz_category['type'] or not quiz_category['id']:
            # TODO: Throw error
            print("The quiz category type and category id must be provided")
            return

        previous_questions = request.get_json().get('previous_questions', [])
        potential_next_questions = Question.query.filter(
            Question.category == quiz_category['id']
        ).filter(
            Question.id.notin_(previous_questions)
        ).all()

        next_question = pick_random_question(potential_next_questions)
        # Account for a NULL next question
        next_question_formatted = next_question.format() if next_question else None

        return jsonify({
            'success': True,
            'question': next_question_formatted
        })

    '''
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    '''

    return app
