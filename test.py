from datetime import datetime, time

def is_time_between(begin_time, end_time, weekday=None, check_time=None):
    # If check time is not given, default to current UTC time
    check_time = check_time or datetime.utcnow().time()
    print(check_time)
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time

dayTimes = {
    0 : (time(8,00),time(23,00),"monday"),
    1 : (time(8,00),time(23,00),"tuesday"),
    2 : (time(8,00),time(23,00),"wednesday"),
    3 : (time(8,00),time(23,00),"thursday"),
    4 : (time(8,00),time(23,00),"Friday"),
    5 : (time(9,00),time(1,00),"Saturday"),
    6 : (time(9,00),time(1,00),"Sunday"),
}

print(is_time_between(*dayTimes[datetime.now().weekday()]))
hour = time(8,00)
print(datetime.utcnow().time())