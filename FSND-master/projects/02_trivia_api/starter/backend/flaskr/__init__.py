# filename: __init__.py
# author:  modified by Connie Compos
# date: 11/10/2020 
# version number: n/a
# Full Stack Web Developer Nanodegree Trivia API Backend 
# for accessing database used by Udacity triva app - project 2

import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category

# Raginating questions max number to return
QUESTIONS_PER_PAGE = 10

# Create and configure the app
def create_app(test_config=None):

  app = Flask(__name__)
  setup_db(app)
  # Set up CORS. Allow fro all origins.
  CORS(app, resources={r"./*": {"origins": "*"}})
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
      response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, PATCH, DELETE, OPTIONS')
      return (response)
  
  # ---------------------- Paginate Questions ----------------------------
  # Send questions back in batches.  User sends page number as URL parameter
  # max number of questions per page is QUESTIONS_PER_PAGE = 10
  def paginate_questions(request, selection):      
      page = request.args.get('page', 1, type=int)
      start = (page - 1) * QUESTIONS_PER_PAGE
      end = start + QUESTIONS_PER_PAGE
      
      paged_questions = [question.format() for question in selection]
      selected_questions = paged_questions[start:end]
      return selected_questions

  # ---------------------- END POINTS ------------------------------------
  
  # ---------------------- GET Categories --------------------------------
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
  
  # ---------------------- GET Questions ---------------------------------
  # Return paginated questions, total question count, current category and 
  # total categories
  @app.route('/questions', methods=['GET'])
  def retrieve_questions():
    
      selection_questions = Question.query.all()
      current_questions = paginate_questions(request, selection_questions)
      selection_categories = Category.query.order_by(Category.type).all()
      #attach category type to each question
      for question in current_questions:
          for category in selection_categories:
              if category.id == question['category']:
                question["category_type"] = category.type
             
      categories = [item.format() for item in selection_categories]

      if len(current_questions) == 0:
          abort(404)
   
      return jsonify({
          "success": True,
          "questions": current_questions,
          "total_questions": len(Question.query.all()),
          "current_category": categories[0],  # default category is category for first question
          "categories": categories,
      })
  # ---------------------- Delete Question -------------------------------
  # Delete question with give id, returns deleted question id
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):

      try:
          question = Question.query.get(question_id)
          question.delete()
      except:
          abort(422)

      return jsonify({
        "success": True,
        "deleted": question.id
      })

  # ---------------------- Create or Search Question ---------------------------------
  # Create a new question or search for question
  @app.route('/questions', methods=['POST'])
  def add_search_question():
      body = request.get_json()
      
      if body==None:
          abort(400)

      try:
          search_term = body.get('searchTerm', None)
      except:
          pass  # not a search then maybe a create new question so keep going

      try: 
          if search_term:
              selection = Question.query.filter(Question.question.ilike('%' + search_term + '%')).all()
              current_questions = paginate_questions(request, selection)
              
              return jsonify({
                  "success":True,
                  "questions": current_questions,
                  "total_questions": len(selection)
              })
          else: 
              new_question = Question(
                  question = body['question'],
                  answer = body['answer'],
                  difficulty = body['difficulty'],
                  category = body['category']
              )
              new_question.insert()
          
              selection = Question.query.all()
              current_questions = paginate_questions(request, selection)
              return jsonify({
                  "success": True,
                  "questions": current_questions,
                  "created":new_question.id,
                  "total_questions": len(selection)
              })
      except:
          abort(422) 

  # ---------------------- GET Questions by Category ---------------------
  # return paginated questions by category 
  # also returns total questions count, current category
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

  # ---------------------- GET Random Question in Category ---------------
  # Returns a random question within the given category that is not 
  # a question that was previously stored in previous questions (from 
  # frontend)
  @app.route('/quizzes', methods=['POST'])
  def retrieve_quiz_question():
      data = request.get_json()
      previous_questions = data['previous_questions']
      current_category = data['quiz_category']
      current_question = []  # returns empty if no new quesiton found
      
      # If category type is "All" (id = 0) then choose from all questions
      if current_category["id"] == 0:
          selection_questions = Question.query.all()
      else:
          selection_questions = Question.query.filter(Question.category == current_category["id"]).all()
      
      # need to make questions have same format as incomping list of previous questions
      current_questions  = [question.format() for question in selection_questions]

      if len(current_questions) == 0:
          abort(404)

      # compare questions in current category with previous questions that 
      # were passed in and filter out new questions
      list_new_questions = [question for question in current_questions if question["id"] not in previous_questions]
      if (list_new_questions):
          # choose random question from list of question keys 
          # as new quiz question to return
          id_list = [question["id"] for question in list_new_questions]
          random_id = random.choice(id_list) 
          current_question = [question for question in list_new_questions if question["id"] == random_id]

      return jsonify({
          "success": True,
          "question": current_question
      })

  # --------------------- ERROR handlers ---------------------------------
  
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


  @app.errorhandler(500)
  def method_not_allowed(error):
    return jsonify({
          "success": False,
          "error": 500,
          "message": "Internal Server Error"
    }), 500

  return app

    