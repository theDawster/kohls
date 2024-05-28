from collections import defaultdict
import employee # type: ignore
import generate_combos  # type: ignore

days = []

OPEN = 9
CLOSE = 20

def main(numWorkers, maxHrs):
    employees = load_employees()
    week = defaultdict(dict)
    workingHrs = CLOSE - OPEN
    blocks = round(workingHrs / numWorkers, 1)

    for day in days:
        generate_combos.create_day(week[day],day, employees, maxHrs, blocks, numWorkers)

    return week


def load_employees(): #update to use sql
    with open('employees.txt') as f:
        emp_pref = {}
        first = True
        for line in f:
            line = line.strip()
            parts = line.split(',')
            if first:
                first = False
                i = 1
                while i < len(parts):
                    days.append(parts[i].strip())
                    i+=1
            else:
                name = parts[0].strip()
                emp_pref[name] = {}
                avail = parts[1:]
                i = 0
                for day in days:
                    emp_pref[name][day] = avail[i].strip()
                    i+=1

    employees = []
    for name in emp_pref:
        employees.append(employee.Employee(name))
        employees[-1].availiability = emp_pref[name]


    return employees
