from collections import defaultdict
import employee # type: ignore
import generate_combos  # type: ignore

days = []

OPEN = 9
CLOSE = 20

def main():
    employees = load_employees()
    week = defaultdict(dict)
    numWorkers = int(input('number of workers:'))
    workingHrs = CLOSE - OPEN
    blocks = round(workingHrs / numWorkers, 1)

    maxHrs = float(input('maximum hours per employee (hrs): '))

    for day in days:
        generate_combos.create_day(week[day],day, employees, maxHrs, blocks, numWorkers)

    print_week(week)

    return


def load_employees():
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


def print_week(week):
    with open('schedule.txt', 'w') as f:
        '''print headers'''
        x=''
        print(f"{x:^10}", end='', file=f)
        for day in days:
            print(f'{day:^10}', end='', file=f)
        print(file=f)

        '''print schedule'''
        blocks = list(week['Sun'].keys())

        for shift in blocks:
            print(f"{shift:^10}", end='', file=f)
            for day in week:
                try:
                    print(f'{week[day][shift].name:^10}', end='', file=f)
                except Exception:
                    print(f'{'None':^10}', end='', file=f)
            print(file=f)
        return


main()
