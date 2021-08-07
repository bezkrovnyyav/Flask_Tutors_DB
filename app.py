from flask import Flask, render_template, request

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import json
from random import randint


from models import Teacher, Booking, Selection
from data import goals


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tutors.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

week_days = {"mon" : "Понедельник", "tue" : "Вторник", "wed" : "Среда",
            "thu" : "Четверг", "fri" : "Пятница", "sat" :"Суббота", "sun" : "Воскресение"}
week_days_reverse = dict((v, k) for k, v in week_days.items())

@app.route("/")
def first():
    data = db.session.query(Teacher).all()
    maximum = len(data) - 1
    id_list = []
    if maximum <= 5:
        for i in range(maximum + 1):
            id_list.append(i)
    else:
        for i in range (6):
             while True:
                tmp = randint(1, maximum)
                if tmp not in id_list:
                    id_list.append(tmp)
                    break
        
    return render_template("index.html", form = data, goals = goals, id_list = id_list)

def dict_value(dictionary):
  return dictionary.rating

@app.route("/goals/<goal>/")
def goal(goal):
    if goal not in goals:
        return "Wrong goal", 404
    needed = []
    data = db.session.query(Teacher).all()
    for i in data:
        if goal in i.goals:
            needed.append(i)
    needed.sort(reverse=True, key=dict_value)
    return render_template("goal.html", teachers = needed, goal = goals[goal])

@app.route("/profiles/")
def profile_all():
    data = db.session.query(Teacher).all()
    return render_template("all_profiles.html", form = data)

@app.route("/profiles/<id>/")
def profile(id):
    try:
        data = db.session.query(Teacher).filter(Teacher.id == int(id)).first()
        if data == None:
            raise Exception
    except:
        return "Wrong ID", 404
    
    week = json.loads(data.free)
    week_remade = dict()
    for i in week:
      week_remade[week_days[i]] = []
      for key, value in week[i].items():
        if value == True:
          week_remade[week_days[i]].append(key)
    return render_template("profile.html", form=data, week = week_remade, week_reverse = week_days_reverse, goals = goals)

@app.route("/request/", methods = ["GET", "POST"])
def request_func():
    if not request.form:
        return render_template("request.html", goals = goals)
    else:
        if request.form["goal"] in goals:
            goal = goals[request.form["goal"]]
        else:
            goal = request.form["goal"]
        data = Selection(name = request.form["name"], time = request.form["time"],
            phone = request.form["phone"], goal = goal)

        db.session.add(data)
        db.session.commit()

        return render_template("request_done.html", form=data)

@app.route("/booking/<id>/<day>/<time>/", methods = ["GET", "POST"])
def booking(id, day, time):
    if not request.form:
        try:
            id = int(id)
            data = db.session.query(Teacher).filter(Teacher.id == id).first()
            if data == None:
                raise Exception
        except:
            return "Wrong ID", 404
    
        time = time.replace("_", ":")
        free = json.loads(data.free)
        if free[day][time] == False:
            return "Already booked"
        return render_template("booking.html", form = data,
            date_time = week_days[day] + ", " + time, day = day, time = time)
    else:
        data = { "name" : request.form["clientName"], "phone" : request.form["clientPhone"]}
        date_time = week_days[request.form["clientWeekday"]] + ", " + request.form["clientTime"]
        #add try except
        main_data = db.session.query(Teacher).filter(Teacher.id == int(request.form["clientTeacher"])).first()
        free = json.loads(main_data.free)
        if free[request.form["clientWeekday"]][request.form["clientTime"]] == True:
            free[request.form["clientWeekday"]][request.form["clientTime"]] = False
            main_data.free = json.dumps(free)
            db.session.commit()
        else:
            return "Alredy booked"
     
        booking = Booking(name = request.form["clientName"],
                    phone = request.form["clientPhone"],
                    day = request.form["clientWeekday"],
                    time = request.form["clientTime"],
                    teacher = main_data)
        
        db.session.add(booking)
        db.session.commit()
        return render_template("booking_done.html", form = data, time = date_time)
            
if __name__ == "__main__":
	app.run(debug=True)