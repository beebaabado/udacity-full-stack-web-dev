# filename: test_flask.py
# author:  modified by Connie Compos
# date: 11/10/2020 
# version number: n/a
# Full Stack Web Developer Nanodegree Trivia API Backend unittests
# for testing trivia API used by Udacity triva app - project 2

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
    
        # default data
        # get last question in question table for deletion as default
        # could be different question (see test for addd question)
        self.question_to_delete_id = 0
        question = Question.query.order_by(Question.id.desc()).first()  
        if question:
            self.question_to_delete_id = question.id

        self.quiz_category = {'id': 4, 
                            'type':'History'}

        self.invalid_quiz_category = {'id': 100, 
                            'type':'History'}

        self.new_question = Question (
            question = "Who is widely considered to be the world's first computer programmer?",
            answer = "Ada Lovelace",
            difficulty = 3,
            category = 4
        )
        self.new_question = self.new_question.format()


        self.invalid_new_question = Question (
            question = "Who is widely considered to be the world's first computer programmer?",
            answer = "Ada Lovelace",
            difficulty = 3,
            category = self.quiz_category
        )
        self.invalid_new_question = self.invalid_new_question.format()

        self.previous_questions = [
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

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    # NOTE TO SELF:  tests are run in order of function name...
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
        res = self.client().get('/questions?page=2')
        data = json.loads(res.data)
        
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['categories'])
        self.assertTrue(data['current_category'])
 
    def test_get_questions_invalid_page_404(self):
        """ Test FAILED GET questions INVALID PAGE """
        res = self.client().get('/questions?page=100')
        data=json.loads(res.data)
        
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")       
 
    def test_get_new_quiz_question(self):
        """ Test Get quiz """
        #use only first two questions in test data array
        res = self.client().post('/quizzes', json={'previous_questions': self.previous_questions[0:2], 'quiz_category': self.quiz_category})    
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])
        
    def test_get_new_quiz_question_no_new_questions(self):
        """ Test Get quiz NO MORE QUESTIONS"""
        # prev len = 4  db questions = 4        
        res = self.client().post('/quizzes', json={'previous_questions': self.previous_questions, 'quiz_category': self.quiz_category})    
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])     

    def test_get_new_quiz_question_invalid_category(self):
        """ Test Get quiz invalid category"""
        res = self.client().post('/quizzes', json={'previous_questions': self.previous_questions[0:2], 'quiz_category': self.invalid_quiz_category})    
        data = json.loads(res.data)
        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "resource not found")       

    def test_add_new_question_POST(self):
        """ Test ADD/POST New question """
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        question = Question.query.filter(Question.id==data["created"]).one_or_none()
        if question:
            self.question_to_delete_id = question.id
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)

    def test_add_new_questions_no_data_POST(self):
        """ Test FAIL ADD/POST New question """
        res = self.client().post('/questions')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['error'], 400)
        self.assertEqual(data['message'], "bad request") 

    def test_delete_question_DELETE(self):
        """ Test DELETE  question """
        delete_path = "/questions/" + str(self.question_to_delete_id)
        res = self.client().delete(delete_path)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['deleted'], self.question_to_delete_id)
    
    def test_delete_question_invalid_id_DELETE(self):
        """ Test FAIL DELETE question with invalid id"""
        res = self.client().delete('/questions/5000')
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], "unprocessable")
    
    def test_search_questions(self):
        res = self.client().post('/questions', json={'searchTerm':'title'})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertEqual(len(data['questions']), data['total_questions'])

    def test_search_questions_searchterm_notfound(self):
        res = self.client().post('/questions', json={'searchTerm':'ZZZZZ'})
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['total_questions'], 0)
        self.assertEqual(len(data['questions']), 0)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()