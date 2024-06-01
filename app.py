from flask import Flask, render_template, redirect, request
import main
import sqlite3

app = Flask(__name__)


DAYS = ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat']

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/employees')
def employees():
    with sqlite3.connect('employees.db') as database:
        db = database.cursor()
        employees = list(db.execute("SELECT * FROM employees"))
        print(employees)
    return render_template('employees.html', employees=employees)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'GET':
        return render_template('add.html')
    else:
        with sqlite3.connect('employees.db') as database:
            db = database.cursor()

            ID = int(request.form.get("id"))
            first = request.form.get("first").strip()
            last = request.form.get("last").strip()

            db.execute('INSERT INTO employees (id, first, last) VALUES (?, ?, ?)', (ID, first, last))
            db.execute('INSERT INTO availiability (employee_id) VALUES (?)', (ID,))
            database.commit()
            
            return availiability(ID)


@app.route('/availiability', methods=['GET', 'POST'])
def availiability(employee=None):
    if request.method == "POST":
        with sqlite3.connect("employees.db") as database:
            db = database.cursor()
            
            for day in DAYS:
                avail_change = request.form.get(day, None)
                ID = employee if employee else int(request.form.get("id"))
                if avail_change:
                    try:
                        db.execute('UPDATE availiability SET :day = \':change\' WHERE employee_id = :id',
                                    {"day":day, "change":avail_change, "id":ID})
                    except Exception:
                        print(day)
                    
            database.commit()
            print("SUCCESS!")
            return redirect("/")
    else:
        return render_template('availiability.html', employee=employee,  days=DAYS)


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == "GET":
        return render_template('generate.html', ready=None)
    else:
        numWorkers, MaxHrs = int(request.form.get('workers')),int(request.form.get('hours'))
        week = main.make_schedule(numWorkers, MaxHrs)
        
        return render_template('generate.html', week=week, days=DAYS, ready=1)