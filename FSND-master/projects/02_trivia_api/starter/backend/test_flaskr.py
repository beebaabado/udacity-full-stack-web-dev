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
        self.database_path = "postgresql://{}@{}/{}".format('postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

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
    def test_get_categories(self):
        """ Test GET categories endpoint"""
        res = self.client().get('/categories')
        data = json.loads(res.data)
        
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['categories']))

    def test_get_categories_questions(self):
        """ Test GET quesions for category id endpoint"""
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)
        
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['current_category'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])  

    def test_get_questions(self):
        """ Test GET questions endpoint"""
        res = self.client().get('/questions')
        data = json.loads(res.data)
        
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])
 
    def test_failed_get_questions_invalid_page_404(self):
        """ Test FAILED GET questions INVALID PAGE """
        res = self.client().get('/questions?page=100')
        data=json.loads(res.data)
        
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")       


    def test_get_new_quiz_question(self):
        """ Test Get quiz """
        previous_questions = [
            {
               "id": 5,
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
                "answer": "Maya Angelou",
                "category": 4,
                "difficulty": 2
            }, 
            {
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?",
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1
            }]

        quiz_category = {'id': 4, 
                         'type':'History'}
        res = self.client().post('/quiz', json={'previous_questions': previous_questions, 'quiz_category': quiz_category})    
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['previous_questions'])
        self.assertTrue(data['current_question'])
        
    def test_get_new_quiz_question_no_new_questions(self):
        """ Test Get quiz NO MORE QUESTIONS"""
        #test database has only 4 category 4 questions 
        previous_questions = [
            {
               "id": 5,
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
                "answer": "Maya Angelou",
                "category": 4,
                "difficulty": 2
            }, 
            {
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?",
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1
            },
            {
                "id": 12, 
                "question": "Who invented Peanut Butter?", 
                "answer": "George Washington Carver", 
                "category": 4, 
                "difficulty": 2
            },
            {
                "id": 23, 
                "question": "Which dung beetle was worshipped by the ancient Egyptians?", 
                "answer": "Scarab", 
                "category": 4, 
                "difficulty": 4
            }]

        quiz_category = {'id': 4, 
                         'type':'History'}
        res = self.client().post('/quiz', json={'previous_questions': previous_questions, 'quiz_category': quiz_category})    
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['previous_questions'])
        self.assertEqual(len(data['current_question']), 0)
        self.assertEqual(data['status_message'], "No more questions in this category.")

    def test_get_new_quiz_question_invalid_category(self):
        """ Test Get quiz invalid category"""
        previous_questions = [
            {
               "id": 5,
                "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
                "answer": "Maya Angelou",
                "category": 4,
                "difficulty": 2
            }, 
            {
                "id": 9,
                "question": "What boxer's original name is Cassius Clay?",
                "answer": "Muhammad Ali",
                "category": 4,
                "difficulty": 1
            }]

        quiz_category = {'id': 100, 
                         'type':'History'}
        res = self.client().post('/quiz', json={'previous_questions': previous_questions, 'quiz_category': quiz_category})    
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")       


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()