from flask import Flask, render_template, redirect, request
import main
import sqlite3

app = Flask(__name__)


DAYS = ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat']

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html', days=DAYS)
    else:
        with sqlite3.connect('employees.db') as database:
            db = database.cursor()

            ID = int(request.form.get("id"))
            first = request.form.get("first")
            last = request.form.get("last")

            db.execute('INSERT INTO employees (id, first, last) VALUES (?, ?, ?)', (ID, first, last))
            db.execute('INSERT INTO availiability (employee_id) VALUES (?)', (ID,))
            for day in DAYS:
                avail_change = request.form.get(day)
                if avail_change:
                    db.execute('UPDATE availiability SET ? = ? WHERE employee_id = ?',
                                (day, avail_change, ID))
                    
            database.commit()
            print("SUCCESS!")
            
            return redirect("/")


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == "GET":
        return render_template('generate.html', ready=None)
    else:
        numWorkers, MaxHrs = int(request.form.get('workers')),int(request.form.get('hours'))
        week = main.make_schedule(numWorkers, MaxHrs)
        
        return render_template('generate.html', week=week, days=DAYS, ready=1)