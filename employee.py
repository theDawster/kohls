OPEN = 9
CLOSE = 20

class Employee:
    def __init__(self, name) -> None:
        self.name = name
        self.availiability = {}
        self.hours = 0

    
    def check_availiable(self, day, shift_start, shift_end) -> bool:
        hours = self.availiability[day]

        if hours == 'all':
            return True
        elif hours == 'none':
            return False
        else:
            start, end = hours.split('-')
            start = OPEN if start == 'open' else float(start)
            end = CLOSE if end == 'close' else float(end)
            if start > shift_start or end < shift_end:
                return False
            return True


