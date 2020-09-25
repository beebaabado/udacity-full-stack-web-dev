# TODO list application 
# 
# Written by Connie Compos

from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/todoappdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# connect database to the app server
db = SQLAlchemy(app)

# connect migration service to app and database
migrate = Migrate(app,db)

#Database schema 

#Table for Todo lists (Parent)
class TodoList(db.Model):
   __tablename__= 'todolist' 
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(), nullable=False)
   todos = db.relationship('Todo', backref='todolist', lazy=True)  #Lazy be default 

   def __repr__(self):
       return f'<Todo {self.id} {self.description}>'

#Table for todo items has (Child)
class Todo(db.Model):
    __tablename__ = 'todos'  #by default will take class name with lowercase letter
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)
    completed = db.Column(db.Boolean, nullable=False, default=False)
    todolist_id = db.Column(db.Integer, db.ForeignKey('todolist.id'), nullable=False)

    def __repr__(self):
       return f'<Todo {self.id} {self.description}>'

#  using migrations now .... don' use db.create_all()
@app.route('/')
@app.route('/index')
def index():
   return  render_template('index.html', data=Todo.query.order_by('id').all())

# display home/index page with Todo lists
@app.route('/')
@app.route('/index')
def index():
   return  render_template('index.html', data=List.query.order_by('id').all())

#Add new todo item and refresh index page with new todo item
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body={}
    
    try:
        description=request.get_json()['description']
        #do something with user input data
        if (description):
           newtodoitem = Todo(description=description)
           db.session.add(newtodoitem)
           db.session.commit()
           # did the commit so our item should have an id now so we can include in returned 
           # response  let's test this first ...
           body['description'] = newtodoitem.description  
           body['id'] = newtodoitem.id 
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort(400)  #HTTP exception for Internal Server Error   NEED to get actual error      
    else: 
        #refresh
        return jsonify(body)
      
#Update the completed column for provied user id
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
def set_completed_todo(todo_id):
   error = False
   try:
        completed=request.get_json()['completed']
        todoitem = Todo.query.get(todo_id)
        todoitem.completed = completed
        db.session.commit()  
   except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
   finally:
        db.session.close()
   
   return redirect(url_for('index'))

# Delete item for provided user id
@app.route('/todos/<todo_id>/delete-item', methods=['DELETE'])
def delete_todo_item(todo_id):
   error = False
   
   try:
      todoitem=Todo.query.get(todo_id)
      db.session.delete(todoitem)
       #can also write as
       #Todo.query.filter_by(id=todo_id).delete()
      db.session.commit()
   except:    
      error = True
      db.session.rollback()
      print(sys.exc_info())
   finally:
      db.session.close()
  
   return jsonify({ 'success': True })

    
if __name__=='__main__':
    app.run()
