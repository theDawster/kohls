import random

OPEN = 9
CLOSE = 20

def create_day(schedule, day, employees, maxHrs, block, numWorkers, time=OPEN):
    if time + block > CLOSE + 1:
        return
    unreliable = set()
    flexible = set()
    for employee in employees:
        if not employee.check_availiable(day, time, time + block):
            continue
        else:
            if employee.availiability[day] == 'all':
                flexible.add(employee)
            else:
                unreliable.add(employee)
        
    worker = None
    if not flexible and not unreliable:
        worker = None
    elif unreliable:
        worker = get_worker(unreliable.copy(), maxHrs, schedule)
    else:
         worker = get_worker(flexible.copy(), maxHrs, schedule)

    if not worker:
        if unreliable:
            worker = get_worker(unreliable.copy(), 1000, schedule)
        if not worker:
            worker = get_worker(flexible.copy(), 1000, schedule)

    start = adjust_time(time)
    end = adjust_time(time + block)

    schedule[f'{start}-{end}'] = worker
    if worker: 
        worker.hours += block

    create_day(schedule, day, employees, maxHrs, block, numWorkers, time + block)

    return
            

def get_worker(copy: set, maxHrs, schedule: dict):
        for person in schedule.values():
            if person in copy:
                copy.remove(person)
        while True:
            if not copy:
                return None
            worker = random.choice(list(copy))
            if worker.hours < maxHrs:
                return worker
            else:
                copy.remove(worker)


def adjust_time(time):
    if time >= 13:
        time = time - 12
    if type(time) == type(1.2):  # noqa: E721
        time = str(int(time)) + get_min(time)
    return time


def get_min(time) -> str:
    n = time * 10
    decimal = n % 10

    if decimal < 5:
        return ':15'
    elif decimal > 5:
        return ':45'
    else:
        return ':30'