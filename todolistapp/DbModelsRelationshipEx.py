from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

class Driver(db.Model):
    __tablename__ = 'driver'  #by default will take class name with lowercase letter
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    vehicles = db.relationship('Vehicle', backref='driver', lazy=True)
    
    def __repr__(self):
       return f'<Todo {self.id} {self.description}>'


class Vehicle(db.Model):
    __tablename__ = 'vehicle'
    id = db.Column(db.Integer, primary_key=True)
    make= db.Column(db.String(), nullable=False)
    model= db.Column(db.String(), nullable=False)   
    
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'), nullable=False)