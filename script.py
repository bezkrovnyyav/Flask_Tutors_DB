from flask import Flask

from flask_sqlalchemy import SQLAlchemy

import json

from models import Teacher, Booking, Selection
from data import teachers

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

for i in teachers:
    teacher = Teacher(name = i["name"], about = i["about"], rating = i["rating"],
        picture = i["picture"], goals = json.dumps(i["goals"]),
        free = json.dumps(i["free"]))
    db.session.add(teacher)
    
db.session.commit()
