import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS
from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
#CORS(app)


# Set up CORS. Allow for all origins.
CORS(app, resources={r"./*": {"origins": "*"}})
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, PATCH, DELETE, OPTIONS')
    return (response) 

'''
   uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

## ROUTES

'''
 Endpoint GET /drinks   PUBLIC access Detail for all drinks - with drink.short() representation with drink 
 title and short recipe (color and parts)
 not athenticated.  Allows visitors to site to view menu
'''
@app.route('/drinks', methods=['GET'])
def get_drinks_public_view():
    
    drinks = Drink.query.all()
    if drinks== None:
         abort(404) 
    drinks_short = [drink.short() for drink in drinks]
    
    return jsonify({
        "status_code": 200,
        "success": True,
        "drinks": drinks_short,
        "number_drinks": len(drinks_short)
    }), 200

'''
 Endpoint GET /drinks     Detail for all drinks - with drink.short() representation with drink 
 title and short recipe (color and parts)
 requires permission:  get:drinks
'''
@app.route('/drinks', methods=['GET'])
@requires_auth('get:drinks')
def get_drinks(payload):
    print(payload)
    
    drinks = Drink.query.all()
    if drinks== None:
         abort(404) 
    drinks_short = [drink.short() for drink in drinks]
    
    return jsonify({
        "status_code": 200,
        "success": True,
        "drinks": drinks_short,
        "number_drinks": len(drinks_short)
    }), 200
    
'''
 Endpoint GET /drink-detail   Detail for one drink specifed by drink id- with drink.short() representation with 
 drink title and short recipe (color and parts) 
 requires permission get:drinks-detail
'''
@app.route('/drink-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drink_detail(payload):
   #print(payload)
    
    body = request.get_json()
    if body==None:
        print("NO BODY")
        abort(400)
    try: 
        drink = Drink.query.filter(Drink.id==body['drink_id']).one_or_none()
        if drink == None:
            abort(404) 

        return jsonify({
            "status_code": 200,
            "success": True,
            "drinks": drink.short()
        }), 200
    except:
        abort(422)


'''
Endpoint GET /drinks-detail
requires the 'get:drinks-detail' permission
Detail for all drinks with drink.long() representation 
'''
@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(payload):
    #print(payload)
    
    drinks = Drink.query.all()
    if drinks==None:
        abort(404)
    drinks_long = [drink.long() for drink in drinks]

    return jsonify({
        "status_code": 200,
        "success": True,
        "drinks": drinks_long,
        "number_drinks": len(drinks_long)
    }), 200

'''
Endpoint POST /drinks
Requires the 'post:drinks' permission
Create new drink in database and returns drink.long() data representation
'''
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def add_drink(payload):
    #print(payload)
    
    body = request.get_json()
    if body==None:
        print("NO BODY")
        abort(400)
    try: 

        # check if drink exists
        drink = Drink.query.filter(Drink.title == body['title']).one_or_none()
        if drink!=None:
          abort(422)
              
        recipe_formatted = json.dumps(body['recipe'])
        new_drink = Drink(
            title = body['title'], 
            recipe = recipe_formatted
        )
        new_drink.insert()
        return jsonify({
            "status_code": 200,
            "success": True,
            "drinks": [new_drink.long()]
        }), 200
    except:
        abort(422)  

'''
Endpoint PATCH /drinks/<id>
Require the 'patch:drinks' permission
<id> is the existing drink id
Returns drink.long() data representation
'''
@app.route('/drinks/<int:id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drink(payload, id):
    #print(payload)
    
    body = request.get_json()
    if body==None:
        print("NO BODY")
        abort(400)
    try: 
        # check if drink exists
        drink = Drink.query.filter(Drink.id == id).one_or_none()
        if drink==None:
          abort(404)
        
        updated_recipe = body.get('recipe', None)    
        if updated_recipe:  
            drink.recipe = json.dumps(updated_recipe)  #formatted recipe
        updated_title = body.get('title', None)
        if updated_title:
            drink.title = updated_title
        
        drink.update()
            
        return jsonify({
            "status_code": 200,
            "success": True,
            "drinks": [drink.long()]
        }), 200
    except:
        abort(422) 

'''
Endpoint DELETE /drinks/<id>
require the 'delete:drinks' permission        
<id> is the existing drink id
returns deleted drink id
'''
@app.route('/drinks/<int:id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(payload, id):
    #print(payload)
    # check if drink exists
    drink = Drink.query.filter(Drink.id==id).one_or_none()

    if drink==None:
        abort(404)
    try:       
        drink.delete()
        return jsonify({
            "status_code": 200,
            "success": True,
            "delete": id
        }), 200
    except:
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
def internal_server_error(error):
    return jsonify({ 
          "success": False,
          "error": 500,
          "message": "Internal Server Error"
    }), 500

'''
error handler for AuthError
'''
@app.errorhandler(AuthError)
def auth_error(ex):
    return jsonify({
        "success": False,
        "error": ex.status_code,
        "message": ex.error['description']
    }), ex.status_code
    

# Default port 5000 on localhost:
#if __name__ == '__main__':
 #   app.run()

# Or specify port manually:
import os
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='127.0.0.1', port=port)