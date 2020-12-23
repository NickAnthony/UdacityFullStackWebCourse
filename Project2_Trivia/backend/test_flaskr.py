import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is the original name and city of the Tennessee Titans?',
            'answer': 'Houston Oilers',
            'difficulty': 8,
            'category': 6
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    '''Testing '/categories' GET endpoint '''

    def test_basic_get_categories_succeeds(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    '''Testing '/questions' GET endpoint '''

    def test_default_get_questions_succeeds(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # Assert the data exists
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])
        # Assert the data is the correct length
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['categories']), 6)
        # Assert default category is selected
        self.assertEqual(data['current_category'], 1)

    def test_get_questions_page_2_succeeds(self):
        res = self.client().get('/questions', json={'page': 2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # Assert the data exists
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])
        # Assert the data is the correct length
        self.assertEqual(len(data['questions']), 9)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['current_category'], 1)

    def test_get_questions_returns_pagenated_results(self):
        res = self.client().get('/questions', json={'page': 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # Assert the data is the correct length
        self.assertEqual(len(data['questions']), 10)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['current_category'], 1)

        page_one_results = [q['id'] for q in data['questions']]

        res = self.client().get('/questions', json={'page': 2})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # Assert the data is the correct length
        self.assertEqual(len(data['questions']), 9)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(len(data['categories']), 6)
        self.assertEqual(data['current_category'], 1)

        page_two_results = [q['id'] for q in data['questions']]

        for q1 in page_two_results:
            for q2 in page_one_results:
                self.assertNotEqual(q1, q2)

    def test_get_questions_throws_404_for_bad_page(self):
        res = self.client().get('/questions', json={'page': 1000})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource was not found')

    '''Testing '/questions/${question_id}' DELETE endpoint '''

    def test_delete_question_succeeds(self):
        # Create question to delete
        res = self.client().post('/questions/create', json={
            'question': self.new_question['question'],
            'answer': self.new_question['answer'],
            'difficulty': self.new_question['difficulty'],
            'category': self.new_question['category']
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        new_question_id = data['id']

        # Check question exists before deletion
        res = self.client().get('/categories/0/questions')
        data = json.loads(res.data)
        self.assertEqual(data['total_questions'], 20)
        question_exists = False
        for question in data['questions']:
            if question['id'] == new_question_id:
                question_exists = True
        self.assertTrue(question_exists)

        # Delete our new question with id new_question_id
        res = self.client().delete('/questions/%d' % new_question_id)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # Check question does NOT exists after deletion
        res = self.client().get('/categories/0/questions')
        data = json.loads(res.data)
        self.assertEqual(data['total_questions'], 19)
        question_exists = False
        for question in data['questions']:
            if question['id'] == new_question_id:
                question_exists = True
        self.assertFalse(question_exists)

    def test_delete_questions_throws_404_for_bad_question_id(self):
        res = self.client().delete('/categories/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource was not found')

    '''Testing '/questions/create' POST endpoint '''

    def test_create_questions_succeeds(self):
        res = self.client().post('/questions/create', json={
            'question': self.new_question['question'],
            'answer': self.new_question['answer'],
            'difficulty': self.new_question['difficulty'],
            'category': self.new_question['category']
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        # Assert the question was inserted
        self.assertEqual(data['question'], self.new_question['question'])
        self.assertEqual(data['answer'], self.new_question['answer'])
        self.assertEqual(data['difficulty'], self.new_question['difficulty'])
        self.assertEqual(data['category'], self.new_question['category'])
        new_question_id = data['id']
        res = self.client().get('/categories/0/questions')
        data = json.loads(res.data)
        question_exists = False
        for question in data['questions']:
            if question['question'] == self.new_question['question']:
                question_exists = True
        self.assertTrue(question_exists)

        # Clean up DB after creating question
        self.client().delete('/questions/%d' % new_question_id)
        data = json.loads(res.data)
        self.assertTrue(data['total_questions'], 19)

    def test_create_questions_400_for_missing_category(self):
        res = self.client().post('/questions/create', json={
            'question': self.new_question['question'],
            'answer': self.new_question['answer'],
            'difficulty': self.new_question['difficulty']
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_create_questions_404_for_bad_category_id(self):
        res = self.client().post('/questions/create', json={
            'question': self.new_question['question'],
            'answer': self.new_question['answer'],
            'difficulty': self.new_question['difficulty'],
            'category': 1000
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource was not found')

    def test_create_questions_422_for_bad_question_format(self):
        res = self.client().post('/questions/create', json={
            'question': None,
            'answer': self.new_question['answer'],
            'difficulty': self.new_question['difficulty'],
            'category': self.new_question['category']
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

        res = self.client().post('/questions/create', json={
            'question': self.new_question['question'],
            'answer': None,
            'difficulty': self.new_question['difficulty'],
            'category': self.new_question['category']
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

        res = self.client().post('/questions/create', json={
            'question': self.new_question['question'],
            'answer': self.new_question['answer'],
            'difficulty': None,
            'category': self.new_question['category']
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    '''Testing '/questions/search' POST endpoint '''

    def test_no_results_search_succeeds(self):
        res = self.client().post('/questions/search', json={
            'searchTerm': 'supercalifragilisticexpialidocious'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 0)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(data['current_category'], 1)

    def test_empty_search_returns_all_questions(self):
        res = self.client().post('/questions/search', json={
            'searchTerm': ''
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 19)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(data['current_category'], 1)

    def test_simple_search_questions_succeeds(self):
        res = self.client().post('/questions/search', json={
            'searchTerm': 'soccer'
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 2)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(data['current_category'], 1)

    def test_search_with_no_term_throws_400(self):
        res = self.client().post('/questions/search')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    '''Testing '/categories/${id}/questions' GET endpoint '''

    def test_get_questions_in_category_succeeds(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 3)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(data['current_category'], 1)

        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 4)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(data['current_category'], 2)

        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 3)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(data['current_category'], 3)

        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 2)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(data['current_category'], 6)

    def test_get_questions_in_all_categories_succeeds(self):
        res = self.client().get('/categories/0/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['questions']), 19)
        self.assertEqual(data['total_questions'], 19)
        self.assertEqual(data['current_category'], 0)

    def test_get_questions_with_bad_category_throws_404(self):
        res = self.client().get('/categories/1000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource was not found')

    '''Testing '/questions/next' POST endpoint '''

    def question_was_previously_returned(self, question, previous_questions):
        for prev_question_id in previous_questions:
            if question['id'] == prev_question_id:
                return True
        return False

    def test_get_questions_in_category_succeeds(self):
        category = {
            'type': 'Art',
            'id': 2
        }
        res = self.client().get('/categories/%d/questions' % (category['id']))
        data = json.loads(res.data)
        previous_questions = []
        num_questions_in_catgeory = len(data['questions'])
        for i in range(num_questions_in_catgeory):
            res = self.client().post('/questions/next', json={
                'previous_questions': previous_questions,
                'quiz_category': {
                    'type': category['type'],
                    'id': category['id']
                }
            })
            data = json.loads(res.data)
            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            self.assertTrue(data['question'])
            self.assertFalse(self.question_was_previously_returned(
                data['question'],
                previous_questions
            ))
            previous_questions.append(data['question']['id'])

        # Assert the next call returns no questions
        res = self.client().post('/questions/next', json={
            'previous_questions': previous_questions,
            'quiz_category': {
                'type': category['type'],
                'id': category['id']
            }
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertFalse(data['question'], 0)

    def test_get_questions_in_category_returns_all_succeeds(self):
        res = self.client().post('/questions/next', json={
            'previous_questions': [],
            'quiz_category': {
                'type': '',
                'id': 0
            }
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

    def test_play_game_throws_400_for_null_category(self):
        res = self.client().post('/questions/next', json={
            'previous_questions': [],
            'quiz_category': None
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request')

    def test_play_game_throws_404_for_bad_category(self):
        res = self.client().post('/questions/next', json={
            'previous_questions': [],
            'quiz_category': {
                'type': 'Art',
                'id': 10000
            }
        })
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource was not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
