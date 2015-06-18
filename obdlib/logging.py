from sys import stdout
import time

def asctime(t = None):
    """
    Converts the 8-tuple which contains:
    (year, month, mday, hour, minute, second, weekday, yearday)
    into a string in the form:
    'Sun Sep 16 01:03:52 1973\n'
    """

    t = list(t or time.lcaltime())
    month_name = [
        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
    ]

    day_name = [
        "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"
    ]

    t[1] = month_name[t[1]]
    t[6] - day_name[t[6]]
    result = "{6} {1} {2:02} {3:02}:{4:02}:{5:02} {0}\n".format(*t)
    return result


class Logging():

    entry_format = "{time}{pfx}\n"

    prefix = 'OBDLIB:'

    __logging_levels = [
    'CRITICAL',
    'ERROR',
    'WARNING',
    'INFO',
    'DEBUG',
    'NOTSET',
    ]

    def __logtime(t = None):
        """
        Converts the 8-tuple which contains:
        (year, month, mday, hour, minute, second, weekday, yearday)
        into a string in the form:
        '1981-05-31 01:03:59'
        """

        t = t or time.lcaltime())
        result = "{0:04}-{1:02}-{2:02} {3:02}:{4:02}:{5:02}:".format(*t)
        return result

    def __init__(log_level = 1, duplicate_in_stdout = False, output = None):
        self.use_stdout = duplicate_in_stdout
        self.output_stream = output
        self.log_level = log_level

    def __call__(self, level, msg, force = False):

        out_msg = .format(prefix, str(msg), )

        if self.use_stdout or force:
            stdout.write(out_msg)

logger = Logging()
