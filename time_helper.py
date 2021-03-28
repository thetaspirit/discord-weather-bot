import datetime

def get_time_with_timezone(time_delta):
    """Parameter is timezone offset from UTC in seconds.  Returns a string H:M:S."""
    return (datetime.datetime.now() + datetime.timedelta(seconds=time_delta)).strftime("%H:%M") + " UTC" + str(time_delta / 3600)

#  print(get_time_with_timezone(-25200))
