"""

    Module:
    Purpose:
    Depends On:

"""

import logging

'''  
    Class: debugFilter
    Parameters: self, record
    Return Value: record
    Purpose: Returns only records that are related to the debug level of logging.
'''


class DebugFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.DEBUG:
            return record


'''  
    Class: infoFilter
    Parameters: self, record
    Return Value: record
    Purpose: Returns only records that are related to the info level of logging.
'''


class InfoFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.INFO:
            return record


'''  
    Class: warningFilter
    Parameters: self, record
    Return Value: record
    Purpose: Returns only records that are related to the warning level of logging.
'''


class WarningFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.WARNING:
            return record


'''  
    Class: errorFilter
    Parameters: self, record
    Return Value: record
    Purpose: Returns only records that are related to the error level of logging.
'''


class ErrorFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.ERROR:
            return record


'''  
    Class: criticalFilter
    Parameters: self, record
    Return Value: record
    Purpose: Returns only records that are related to the critical level of logging.
'''


class CriticalFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.CRITICAL:
            return record
