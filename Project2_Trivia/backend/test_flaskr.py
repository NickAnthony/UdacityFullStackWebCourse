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

	# def test_404_was_thrown(self):
	# 	res = self.client().post('/things', json={'foo': ''})
	# 	data = json.loads(res.data)
	#
	# 	self.assertEqual(res.status_code, 404)
	# 	self.assertEqual(data['success'], False)
	# 	self.assertEqual(data['message'], 'foo was not bar')

	'''Testing '/questions' GET endpoint '''

	def test_default_get_questions_succeeds(self):
		res = self.client().get('/questions')
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertEqual(data['success'], True)
		# Assert the data exists
		self.assertTrue(data['questions'])
		self.assertTrue(data['totalQuestions'])
		self.assertTrue(data['categories'])
		self.assertTrue(data['currentCategory'])
		# Assert the data is the correct length
		self.assertEqual(len(data['questions']), 10)
		self.assertEqual(len(data['totalQuestions']), 19)
		self.assertEqual(len(data['categories']), 6)
		# Assert the questions are the correct page
		self.assertEqual(data['questions'], data['totalQuestions'][0:10])
		# Assert default category is selected
		self.assertEqual(data['currentCategory'], 1)

	def test_get_questions_page_2_succeeds(self):
		res = self.client().get('/questions', json={'page': 2})
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertEqual(data['success'], True)
		# Assert the data exists
		self.assertTrue(data['questions'])
		self.assertTrue(data['totalQuestions'])
		self.assertTrue(data['categories'])
		self.assertTrue(data['currentCategory'])
		# Assert the data is the correct length
		self.assertEqual(len(data['questions']), 9)
		self.assertEqual(len(data['totalQuestions']), 19)
		self.assertEqual(len(data['categories']), 6)
		# Assert the questions are the correct page
		self.assertEqual(data['questions'], data['totalQuestions'][10:])
		self.assertEqual(data['currentCategory'], 1)

	# def test_404_was_thrown(self):
	# 	res = self.client().post('/things', json={'foo': ''})
	# 	data = json.loads(res.data)
	#
	# 	self.assertEqual(res.status_code, 404)
	# 	self.assertEqual(data['success'], False)
	# 	self.assertEqual(data['message'], 'foo was not bar')

	'''Testing '/questions/${question_id}' DELETE endpoint '''

	def test_delete_question_succeeds(self):
		# Check question exists before deletion
		res = self.client().get('/questions')
		data = json.loads(res.data)
		self.assertEqual(len(data['totalQuestions']), 19)
		question_exists = False
		for question in data['totalQuestions']:
			if question['id'] == 2:
				question_exists = True
		self.assertTrue(question_exists)

		# Delete question with id 2:
		# "What movie earned Tom Hanks his third straight Oscar nomination,
		# in 1996?"
		res = self.client().delete('/questions/2')
		data = json.loads(res.data)
		self.assertEqual(res.status_code, 200)
		self.assertEqual(data['success'], True)

		# Check question does NOT exists after deletion
		res = self.client().get('/questions')
		data = json.loads(res.data)
		self.assertEqual(len(data['totalQuestions']), 18)
		question_exists = False
		for question in data['totalQuestions']:
			if question['id'] == 2:
				question_exists = True
		self.assertFalse(question_exists)

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
		res = self.client().get('/questions')
		data = json.loads(res.data)
		question_exists = False
		for question in data['totalQuestions']:
			if question['question'] == self.new_question['question']:
				question_exists = True
		self.assertTrue(question_exists)

	'''Testing '/questions/search' POST endpoint '''

	def test_no_results_search_succeeds(self):
		res = self.client().post('/questions/search', json={
			'searchTerm': 'supercalifragilisticexpialidocious'
		})
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertEqual(data['success'], True)
		self.assertEqual(len(data['questions']), 0)
		self.assertEqual(len(data['totalQuestions']), 19)
		self.assertEqual(data['currentCategory'], 1)

	def test_empty_search_returns_all_questions(self):
		res = self.client().post('/questions/search', json={
			'searchTerm': ''
		})
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertEqual(data['success'], True)
		self.assertEqual(len(data['questions']), 19)
		self.assertEqual(len(data['totalQuestions']), 19)
		self.assertEqual(data['currentCategory'], 1)

	def test_simple_search_questions_succeeds(self):
		res = self.client().post('/questions/search', json={
			'searchTerm': 'soccer'
		})
		data = json.loads(res.data)

		self.assertEqual(res.status_code, 200)
		self.assertEqual(data['success'], True)
		self.assertEqual(len(data['questions']), 2)
		self.assertEqual(len(data['totalQuestions']), 19)
		self.assertEqual(data['currentCategory'], 1)

	'''Testing '/categories/${id}/questions' GET endpoint '''

	'''Testing '/questions/next' POST endpoint '''



# Make the tests conveniently executable
if __name__ == "__main__":
	unittest.main()
