# filename: models.py
# author:  modified by Connie Compos
# date: 12/5/2020 
# version number: n/a
# Full Stack Web Developer Nanodegree Trivia API Backend 
# Database models used by Udacity triva app - project 2

import os
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "trivia_test"
database_path = "postgresql://{}@{}/{}".format('postgres','localhost:5432', database_name)
db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

'''
Question
'''
class Question(db.Model):  
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String)
  answer = Column(String)
  category = Column(Integer)
  difficulty = Column(Integer)
  rating = Column(Integer)

  def __init__(self, question, answer, category, difficulty, rating):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty
    self.rating = rating


  def __repr__(self):
    return f'<Question {self.id} {self.question} {self.answer} {self.category} {self.difficulty} {self.rating}>'

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty,
      'rating': self.rating
    }

'''
Category
'''
class Category(db.Model):  
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String)

  def __init__(self, type):
    self.type = type

  def __repr__(self):
    return f'<Category {self.id} {self.type}>'

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }

'''
User    
'''
class Player(db.Model):
  __tablename__ = 'player'
  
  id = Column(Integer, primary_key=True)
  name = Column(String, unique=True)

  scores = db.relationship("Score", back_populates="player",  cascade="all, delete-orphan", lazy=True)

  def __init__(self, name):
    self.name = name
  
  def __repr__(self):
    return f'<Player {self.id} {self.name} Scores {self.scores}>'

  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'name': self.name, 
    }

'''
Score
'''
class Score(db.Model):
  __tablename__ = 'score'

  id = Column(Integer, primary_key=True)
  value = Column(Integer)
  category_id = Column(Integer)
  player_id = Column(Integer, ForeignKey('player.id'))
  player = db.relationship("Player", back_populates="scores")

  def __init__(self, value, category_id, player_id):
    self.value = value
    self.category_id = category_id
    self.player_id = player_id

  def __repr__(self):
    return f'<Score {self.id} {self.value} {self.category_id} {self.player_id}>'
 
  def insert(self):
    db.session.add(self)
    db.session.commit()
  
  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'value': self.value,
      'category_id': self.category_id,
      'playerId': self.player_id, 
    }  