from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stepik.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

db = SQLAlchemy()

class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    about = db.Column(db.String)
    rating = db.Column(db.Float)
    picture = db.Column(db.String)
    goals = db.Column(db.String)
    free = db.Column(db.String)
    lessons = db.relationship("Booking")


class Booking(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    phone = db.Column(db.String)
    day = db.Column(db.String)
    time = db.Column(db.String)
    teacher = db.relationship("Teacher", ) #realition one to one
    teacher_id = db.Column(db.Integer, db.ForeignKey("teachers.id"))

class Selection(db.Model):
    __tablename__ = "selections"
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    time = db.Column(db.String)
    phone = db.Column(db.String)
    goal = db.Column(db.String)

# db.create_all()