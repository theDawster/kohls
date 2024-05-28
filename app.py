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
        render_template('generate.html', ready=False)
    else:
        numWorkers, MaxHrs = request.form.get('workers'),request.form.get('hours')
        week = main.main(numWorkers, MaxHrs)
        days = ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat']
        render_template('generate.html', week=week, days=days)