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
  # Set up CORS. Allow '*' for origins.  COMPLETED.
  CORS(app, resources={r"./*": {"origins": "*"}})

  # Use the after_request decorator to set Access-Control-Allow   COMPLETED.
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      #response.headers.add('Access-Control-Allow_Origins', '*')
      response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, PATCH, DELETE, OPTIONS')
      return (response)
  
  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  # Send questions back in batches.  User sends page number as URL parameter
  # max number of questions per page is QUESTIONS_PER_PAGE = 10
  def paginate_questions(request, selection):      
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      
      paged_questions = [question.format() for question in selection]
      selected_questions = paged_questions[start:end]
      return selected_questions

  # HOME
  # Default Route...index
  # @app.route('/')
  # @app.route('/index')
  # def index():
  #     return()

  # Retrieve all categories and total categories count    
  @app.route('/categories', methods=['GET'])
  def retrieve_categories():
      categories = Category.query.order_by(Category.type).all()
      categories = [category.format() for category in categories]
      
      if len(categories) == 0:
         abort(404) 

      return jsonify({
          "success": True,
          "categories": categories,
          "total_categories": len(Category.query.all())
      })
  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 
  '''
  
  # return questions paginated
  # also returns total questions count, current category , and total categories.
  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    
      selection_questions = Question.query.all()
      current_questions = paginate_questions(request, selection_questions)
      selection_categories = Category.query.order_by(Category.type).all()
      # This is not most efficient way to do this.  Should do join from database
      # to combine category type with questions.  However, we use question.format() which does
      # not handle category type.  So add category type after the fact.  
      for question in current_questions:
          for category in selection_categories:
              if category.id == question['category']:
                question["category_type"] = category.type
             
    
      categories = [item.format() for item in selection_categories]
      one_category = Category.query.filter(Category.id == 1).one_or_none()
      
      if (one_category):
          current_category = one_category.format()
      else:
         abort(404)

      if len(current_questions) == 0:
          abort(404)
   
      return jsonify({
          "success": True,
          "questions": current_questions,
          "total_questions": len(Question.query.all()),
          "current_category": current_category,
          "categories": categories,
      })

  '''
  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  # return questions by category and paginated
  # paramters:  int category_id
  # also returns total questions count, current category , and total categories.
  @app.route('/categories/<int:category_id>/questions', methods=['GET'])
  def retrieve_category_questions(category_id):
      selection_questions = Question.query.filter(Question.category == category_id).all()
      current_questions = paginate_questions(request, selection_questions)
      one_category = Category.query.filter(Category.id == category_id).one_or_none()
      
      if (one_category):
          current_category = one_category.format()
          for question in current_questions:
              question["category_type"] = one_category.type
      else:
         abort(404)

      if len(current_questions) == 0:
          abort(404)

      return jsonify({
          "success": True,
          "questions": current_questions,
          "current_category": current_category,
          "total_questions": len(selection_questions)
      })

  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random question within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quiz', methods=['POST'])
  def retrieve_quiz_question():
      data = request.get_json()
      previous_questions = data['previous_questions']
      current_category = data['quiz_category']
      current_question = []  # returns empty if no new quesiton found
      status_message = "OK"
    
      selection_questions = Question.query.filter(Question.category == current_category["id"]).all()
      current_questions  = [question.format() for question in selection_questions]

      if len(current_questions) == 0:
          abort(404)
          
      # compare questions in category with previous questions that were passed in as param
      # filter out new quiz questions
      list_new_quesitons = [question for question in current_questions if question not in previous_questions]
      
      if (list_new_quesitons):
          # choose random question by random selection from list of question keys 
          # as new quiz question to return
          id_list = [question["id"] for question in list_new_quesitons]
          random_id = random.choice(id_list) 
          current_question = [question for question in list_new_quesitons if question["id"] == random_id]
          previous_questions.append(current_question[0]) #only one item in array
      else:
        # no new questions  
          status_message = "No more questions in this category."
          current_question = {}

      return jsonify({
          "success": True,
          "previous_questions": previous_questions,
          "current_question": current_question,
          "status_message": status_message
      })

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
    }), 404        

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
         "success": False, 
         "error": 422,
         "message": "unprocessable"
    }), 422
        
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
         "success": False, 
         "error": 400,
         "message": "bad request"
    }), 400
  
  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
          "success": False,
          "error": 405,
          "message": "method not allowed"
    }), 405

  return app

    