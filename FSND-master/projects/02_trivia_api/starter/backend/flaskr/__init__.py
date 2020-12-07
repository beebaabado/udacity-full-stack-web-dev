# filename: __init__.py
# author:  modified by Connie Compos
# date: 12/5/2020 
# version number: n/a
# Full Stack Web Developer Nanodegree Trivia API Backend 
# for accessing database used by Udacity triva app - project 2

#import sys  #for debugging
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
from models import setup_db, Question, Category, Player, Score

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

  # ---------------------- ENDPOINTS ------------------------------------
  
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
  
  # ---------------------- Create Categories --------------------------------
  # Add a new category    
  @app.route('/categories', methods=['POST'])
  def create_category():
      
      body = request.get_json()
      if body==None:
          abort(400)
      
      try: 
          new_category = Category(
            type = body['category_type']
          )
          new_category.insert()

          return jsonify({
            "success": True,
            "created": new_category.id
          })
      except:
          abort(422)  

  # ---------------------- Delete Category -------------------------------
  # Delete category with give id, returns deleted category id
  @app.route('/categories/<int:category_id>', methods=['DELETE'])
  def delete_category(category_id):

      try:
          category = Category.query.get(category_id)
          category.delete()
      except:
          abort(422)

      return jsonify({
        "success": True,
        "deleted": category.id
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
          "categories": categories
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
                  category = body['category'],
                  rating = 0
              )
              new_question.insert()
          
              selection = Question.query.all()
              current_questions = paginate_questions(request, selection)
              return jsonify({
                  "success": True,
                  "questions": current_questions,
                  "created": new_question.id,
                  "total_questions": len(selection)
              })
      except:
          abort(422)  

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

  # ---------------------- Add New Player --------------------------------
  # Add new player. Returns new player id.

  @app.route('/players', methods=['POST'])   
  def add_player():
      body = request.get_json()

      if body==None: 
          abort(400)
         
      try:
      
         # check if user exists
          player = Player.query.filter(Player.name == body['name']).one_or_none()
          if player!=None:
              abort(422)
              
          new_player = Player(
              name = body['name']
              )    
          new_player.insert()
         
          return jsonify({
              "success": True,
              "created": new_player.id
              })
      except:
          abort(422) 


  # ---------------------- Get Player info -------------------------------
  # Retrieve player info by name.  Returns player object and player scores
  #
  @app.route('/players/<string:player_name>', methods=['GET'])
  def get_player(player_name):
      scores = []

      a_player = Player.query.filter(Player.name == player_name).one_or_none()

      if a_player == None:
          abort(404)

      a_player_formatted = a_player.format()  
      scores = [score.format() for score in a_player.scores]
      
      for score in scores:
          score_category = Category.query.filter(Category.id == score["category_id"]).one_or_none()
          score["category_type"] = score_category.type 

      return jsonify({
          "success": True,
          "player": a_player_formatted,
          "scores": scores,
          'scoreCount': len(scores) 
      })
  
  # ---------------------- Delete Player -------------------------------
  # Delete player with give id, returns deleted player id
  @app.route('/players/<int:player_id>', methods=['DELETE'])
  def delete_player(player_id):

      try:
          a_player = Player.query.get(player_id)
          a_player.delete()
      except:
          abort(422)

      return jsonify({
        "success": True,
        "deleted": a_player.id
      })

  # --------------------- Add Player score ------------------------------
  # Add new score to specified player
  #
  @app.route('/score', methods=['POST'])
  def add_score():
      body = request.get_json()
      
      if body==None: 
          abort(400)
         
      try:
          new_score = Score(
              value = int(body['value']),
              category_id = int(body['category_id']),
              player_id = int(body['player_id'])
              )    
          new_score.insert()
          
          return jsonify({
              "success": True,
              "created": new_score.id
              })
      except:
          #print(sys.exc_info())
          abort(422) 

  # ---------------------- Update question Rating -----------------------
  # update rating for question with specified id
  #
  @app.route('/ratings', methods=['POST'])
  def update_rating():

      body = request.get_json()

      if body==None:
          abort(400)

      try:
          question = Question.query.get(body["id"])
          question.rating = body["rating"]
          question.update()

          return jsonify({
              "success": True,
              "modified": question.id
          })
      except:
          #print(sys.exc_info())
          abort(422) 
 
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