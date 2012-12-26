import datetime
from datetime import date

days_in_month = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

def add(__date, __year=None, __month=None, __day=None):
    __date = get_date(__date) if ( not isinstance(__date, datetime.date) ) else __date
    if ( __year != None ):
        __date = __date.replace(year=__date.year+abs(int(__year)))

    if ( __month != None ):
        if ( int(__month)/12 > 0 ):
            year = int(__month)/12
            add(__date, year, None, None)
            __month = __month - year * 12
        if ( __date.month + abs(int(__month)) > 12 ):
            __date = __date.replace(year=__date.year+1, month=__date.month+abs(int(__month))-12)
        else:
            __date = __date.replace(month=__date.month+abs(int(__month)))
    
    if ( __day != None ):
        if ( abs(int(__day)) > 28 ):
            __day = 28

        days_in_month[2] = 29 if ( __date.year%4 == 0 and __date.month == 2 ) else 28

        if ( __date.day + abs(int(__day)) > days_in_month[__date.month] ):
            month  = 1 if ( __date.month + 1 > 12 ) else __date.month
            year = __date.year + 1 if ( __date.month + 1 > 12 ) else __date.year
            __date = __date.replace(year=year, month=month, day=__date.day+abs(int(__day))-days_in_month[__date.month])
        else:
            __date = __date.replace(day=__date.day+abs(int(__day)))

    return datetime.datetime.strftime(__date, '%Y-%m-%d')

def this_month():
    month = date.today().month
    days = days_in_month[month]
    return datetime.datetime.strftime(date.today().replace(day=days), '%Y-%m-%d')

def this_week():
    weekday = date.today().isoweekday()
    return add(date.today(), None, None, 7-weekday)

def compare(__date1, __date2):
    __date1 = get_date(__date1) if ( not isinstance(__date1, datetime.date) ) else __date1
    __date2 = get_date(__date2) if ( not isinstance(__date2, datetime.date) ) else __date2

    if ( __date1 < __date2 ):
        return -1
    elif ( __date1 == __date2 ):
        return 0
    elif ( __date1 > __date2 ):
        return 1

def before_today(__date):
    return True if ( compare_today(__date) == -1) else False

def equal_today(__date):
    return True if ( compare_today(__date) == 0) else False

def after_today(__date):
    return True if ( compare_today(__date) == 1) else False

def today():
    return datetime.datetime.strftime(date.today(), '%Y-%m-%d')

def get_date(__date):
    return datetime.datetime.strptime(__date, '%Y-%m-%d').date()

def compare_today(__date):
    return compare(__date, date.today())

def within(__year=None, __month=None, __day=None):
    return add(date.today(), __year, __month, __day)
