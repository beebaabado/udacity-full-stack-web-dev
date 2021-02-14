# filename: flask test_cases_api.py
# author:  modified by Connie Compos
# date: 2/2/2021
# version number: n/a
# Full Stack Web Developer Nanodegree Coffee Shop Full Stack unittests
# for testing api.py coffee shop api used by Udacity coffe shop full stack app - project 3

import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from database.models import db_drop_and_create_all, setup_db, Drink
#from .auth.auth import AuthError, requires_auth
class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    # @classmethod
    # def setUpClass(cls):
    #    cls.thing = Thing() # the `thing` is only instantiated onc

    def setUp(self):
        """Define test variables and initialize app."""
        # This function is called before each testcase
        
        self.app = create_app()
        self.client = self.app.test_client
        self.project_dir = os.path.dirname(os.path.abspath(__file__))
        self.database_name = "database.db"  #should really set up copy of database
        self.database_path = "sqlite:///{}".format(os.path.join(self.project_dir, self.database_name))
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            #self.db.create_all()  
    
        # default data
        # get last drink in drink table for deletion as default
        self.drink_to_delete_id = 0
        
        drink = Drink.query.order_by(Drink.id.desc()).first()
        if drink:
            self.drink_to_delete_id = drink.id

        self.new_drink = {
            "title": "Vanilla Latte",
            "recipe": [
                {
                    "color": "black",
                    "name": "cold brew",
                    "parts": 1
                },
                {
                    "color": "white",
                    "name": "milk",
                    "parts": 2
                }]
        }

        self.update_drink_title = {
            "title": "Iced Pumpkin Spice Latte"
        }
        self.update_drink_recipe = {
            "recipe": [
            {
                "color": "black",
                "name": "cold brew",
                "parts": 1
            },
            {
                "color": "orange",
                "name": "pumpkin chai",
                "parts": 1
            },
            {
                "color": "blue",
                "name": "cold milk",
                "parts": 2
            }
        ]
        }
    def tearDown(self):
        """Executed after reach test"""
        pass

    
    """
    Write at least one test for each test for successful operation and for expected errors.
    """
    # NOTE:  tests are run in order of function name...
    def test_get_drinks(self):
        """ Test GET drinks endpoint"""
        res = self.client().get('/drinks')
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['drinks_short'])

    # def test_get_drink_details(self):
    #     """ Test Get drink details long list"""
    #     res = self.client().post('/quizzes', json={'previous_questions': self.previous_questions[0:2], 'quiz_category': self.invalid_quiz_category})    
    #     data = json.loads(res.data)
    #     self.assertEqual(data['success'], False)
    #     self.assertEqual(res.status_code, 404)
    #     self.assertEqual(data['error'], 404)
    #     self.assertEqual(data['message'], "resource not found")       

    # def test_add_new_drink_POST(self):
    #     """ Test ADD/POST New dring """
    #     res = self.client().post('/drinks', json=self.new_question)
    #     data = json.loads(res.data)
    #     drink = Drink.query.desc().first()       
    #     self.assertTrue(data['drinks'], drink)
    #     self.assertEqual(data['success'], True)
    #     self.assertEqual(res.status_code, 200)
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()