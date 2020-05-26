"""

    Module:
    Purpose:
    Depends On:

"""
import datetime
from SCTimeUtility.Log.Log import get_log

'''  
    Function: strpTimeMultiple
    Parameters: text, formats
    Return Value: dateTime str
    Purpose: Returns a conversion of text into the specified format within the formats list in relation to datetime
             strptime.
'''


def strptime_multiple(text, formats):
    for f in formats:
        try:
            return datetime.datetime.strptime(text, f)
        except ValueError:
            pass
    raise ValueError()
