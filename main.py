from collections import defaultdict
import employee # type: ignore
import generate_combos  # type: ignore
import sqlite3

days = ['Sun', 'Mon', 'Tues', 'Wed', 'Thurs', 'Fri', 'Sat']

OPEN = 9
CLOSE = 20

def make_schedule(numWorkers, maxHrs):
    employees = load_employees()
    week = defaultdict(dict)
    workingHrs = CLOSE - OPEN
    blocks = round(workingHrs / numWorkers, 1)

    for day in days:
        generate_combos.create_day(week[day],day, employees, maxHrs, blocks, numWorkers)

    return week


def load_employees() -> list[employee.Employee]: #update to use sql
    with sqlite3.connect('employees.db') as database:
        db = database.cursor()

        e = list(db.execute('SELECT first, id FROM employees'))
        
        employees = []

        for name, ID in e:
            employees.append(employee.Employee(name))
            avail = list(db.execute('SELECT * FROM availiability WHERE employee_id = ?', (ID,)))[0]
            for i, day in enumerate(days):
                employees[-1].availiability[day] = avail[i]

    return employees

make_schedule(2, 25)