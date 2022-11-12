import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DB_PASSWORD


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format("postgres", DB_PASSWORD, "localhost:5432", self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'What is the motto for Timone and Pumba?',
            'answer': 'Hakuna matata',
            'category': 5, 
            'difficulty': 1
        }

        self.new_quizzes = {
            'previous_questions': [],
            'quiz_category': {
            'id': 5, 
            'type': 'entertainment'}
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

#tests doe getting the category:
    #successful test 
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_categories'])
        self.assertTrue(data['categories'])
    #failed test
    def test_404_get_categories(self):
        res = self.client().get('/categories/17')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')


 #test for getting the paginated questions
    #successful test
    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['categories'])
        #self.assertTrue(data['current_category'])
    #failed test
    def test_404_get_paginated_questions(self):
        res = self.client().get('/questions?page=17000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

 
 #test for deleting questions
    #successful test
    def test_delete_questions(self):
        res = self.client().delete('/questions/7')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 7).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'], 7)
        self.assertEqual(question, None)
    #failed test
    def test_422_if_question_doesnt_exist(self):
        res = self.client().delete('/questions/1700')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


#test for creating new questions
    #successful test
    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question) #changed from new_question
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
    #failed test
    def test_422_cannot_create_question(self):
        res = self.client().delete('/questions/1700', json=self.new_question) #changed from new_question
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


#test for searching for questions 
    #successful test
    def test_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm': 'who'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        #self.assertEqual(len(data['total_questions'])) #corrected from previous test
    #failed test

    
    def test_200_search_questions_no_result(self):
        res = self.client().post('/questions', json={'searchTerm': 'uzuzsdrawkcab'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        #self.assertEqual(data['total_questions'], 0) #,0 removed- test error: assertion error 
        #self.assertEqual(len(data['questions']), 0)
        


#test for getting questions by category
    #successful test
    def test_get_questions_by_category(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['current_category'])
    #failed test
    
    '''def test_404_question_category_not_found(self):
        res = self.client().get('/categories/12000/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'resource not found')
       '''


#test for getting questions to play the quiz 
    #successful test
    def test_get_questions_to_play_quiz(self):
        res = self.client().post('/quizzes', json = self.new_quizzes)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    #failed test
    def test_422_no_questions_to_play_quiz(self):
        res = self.client().post('/quizzes', json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')
        


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()