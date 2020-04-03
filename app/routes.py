import os
from app import app
from flask import render_template, request, redirect


import datetime

x = datetime.datetime.now()

print(x)

from flask_pymongo import PyMongo

# name of database
app.config['MONGO_DBNAME'] = 'events'

# URI of database
app.config['MONGO_URI'] = 'mongodb+srv://dbUser:sWaN9SdDtqPFF3Wr@cluster0-stiba.mongodb.net/events?retryWrites=true&w=majority'

mongo = PyMongo(app)


# INDEX

@app.route('/')
@app.route('/index')

def index():
    #connect to the database
    collection = mongo.db.events
    #query the database to get all the events
    #store those events as a list of dictionaries called events
    events = list(collection.find({}))
    #print the events
    for event in events:
        print(event["event_name"])
        print(event["event_date"])
    return render_template('index.html', events = events)


# CONNECT TO DB, ADD DATA

@app.route('/add')

def add():
    # connect to the database
    collection = mongo.db.events
    # insert new data
    collection.insert({"event_name": "test", "event_date": "today"})
    # return a message to the user
    return "you added an event to the database!"

# need a get and a post method
@app.route('/results', methods = ["get", "post"])
def results():
    # store userinfo from the form
    user_info = dict(request.form)
    print(user_info)




    return redirect('/index')

@app.route('/notes_results', methods = ["get", "post"])
def notes_results():
    user_info = dict(request.form)
    print(user_info)


    notes_text = user_info["notes_text"]
    print("Here are your notes: ", notes_text)
    collection = mongo.db.notes
    collection.insert({"notes_text": notes_text})
    notes = list(collection.find({}))
    return render_template('notes_results.html', notes = notes)

@app.route('/calendar_results', methods = ["get", "post"])
def calendar_results():
    user_info = dict(request.form)
    print(user_info)

    calendar = user_info["calendar_text"]
    calendar_date = user_info["event_date"]
    print("Here are your events: ", calendar)
    collection = mongo.db.calendar
    collection.insert({"calendar": calendar ,"calendar_date": calendar_date})
    calendar = list(collection.find({}))
    return render_template('calendar_results.html', calendar = calendar)

@app.route('/tasks_results', methods = ["get", "post"])
def tasks_results():
    user_info = dict(request.form)
    print(user_info)

    tasks_date = user_info["tasks_date"]
    tasks_text = user_info["tasks_text"]
    print("Here are your tasks: ", tasks_date)
    collection = mongo.db.tasks
    collection.insert({"tasks_date": tasks_date ,"tasks_text": tasks_text})
    tasks = list(collection.find({}))
    return render_template('tasks_results.html', tasks = tasks)

@app.route('/calendar_viewall')
def calendar_viewall():
    collection = mongo.db.calendar
    calendar = list(collection.find({}))
    return render_template('calendar_viewall.html', calendar = calendar)

@app.route('/tasks_viewall')
def tasks_viewall():
    collection = mongo.db.tasks
    tasks = list(collection.find({}))
    return render_template('tasks_viewall.html', tasks = tasks)

@app.route('/notes_viewall')
def notes_viewall():
    collection = mongo.db.notes
    notes = list(collection.find({}))
    return render_template('notes_viewall.html', notes = notes)


@app.route("/secret")
def secret():
    #connect to the database
    collection = mongo.db.events
    #delete everything from the database
    #invoke the delete_many method on the collection
    collection.delete_many({})
    return redirect('/index')

@app.route("/home")
def home():
    return redirect('/index')

@app.route("/calendar")
def calendar():
    return render_template('calendar.html')

@app.route("/tasks")
def tasks():
    return render_template('tasks.html')

@app.route("/notes")
def notes():
    return render_template('notes.html')
