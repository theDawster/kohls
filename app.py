from flask import Flask, render_template, redirect, request
import main

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    return render_template('add.html')


@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == "GET":
        return render_template('generate.html', ready=None)
    else:
        numWorkers, MaxHrs = int(request.form.get('workers')),int(request.form.get('hours'))
        week = main.make_schedule(numWorkers, MaxHrs)
        days = ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat']
        return render_template('generate.html', week=week, days=days, ready=1)