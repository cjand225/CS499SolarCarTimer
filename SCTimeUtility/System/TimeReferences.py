import datetime
from SCTimeUtility.Log.Log import getLog

'''  
    Function: strpTimeMultiple
    Parameters: text, formats
    Return Value: dateTime str
    Purpose: Returns a conversion of text into the specified format within the formats list in relation to datetime
             strptime.
'''


def strptimeMultiple(text, formats):
    for f in formats:
        try:
            return datetime.datetime.strptime(text, f)
        except ValueError:
            pass
    raise ValueError()


'''  
    Function: splitTimes
    Parameters: text
    Return Value: int
    Purpose: Returns a conversion of the string text into the equivalent amount of time in integer form.
'''


def splitTimes(text):
    delta = None
    if text.isdigit():
        # hours/min/sec
        if len(text) > 4:
            hour = int(text[4:])
            min = int(text[2:3])
            sec = int(text[0:1])

            delta = datetime.timedelta(hours=hour, minutes=min, seconds=sec).total_seconds()
        # Minutes/sec
        elif len(text) > 2 and len(text) <= 3:
            min = int(text[0:2])
            sec = int(text[2:])

            delta = datetime.timedelta(minutes=min, seconds=sec).total_seconds()
        # seconds
        elif len(text) >= 1 and len(text) <= 2:
            sec = int(text)
            delta = datetime.timedelta(seconds=sec).total_seconds()
        # throw out bad data
        else:
            delta = datetime.timedelta(seconds=0).total_seconds()

    return int(delta)
