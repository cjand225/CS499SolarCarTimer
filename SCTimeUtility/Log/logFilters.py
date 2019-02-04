import logging

'''  
    Class: debugFilter
    Parameters: self, record
    Return Value: record
    Purpose: Returns only records that are related to the debug level of logging.
'''


class debugFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.DEBUG:
            return record


'''  
    Class: infoFilter
    Parameters: self, record
    Return Value: record
    Purpose: Returns only records that are related to the info level of logging.
'''


class infoFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.INFO:
            return record


'''  
    Class: warningFilter
    Parameters: self, record
    Return Value: record
    Purpose: Returns only records that are related to the warning level of logging.
'''


class warningFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.WARNING:
            return record


'''  
    Class: errorFilter
    Parameters: self, record
    Return Value: record
    Purpose: Returns only records that are related to the error level of logging.
'''


class errorFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.ERROR:
            return record


'''  
    Class: criticalFilter
    Parameters: self, record
    Return Value: record
    Purpose: Returns only records that are related to the critical level of logging.
'''


class criticalFilter(logging.Filter):
    def filter(self, record):
        if record.levelno == logging.CRITICAL:
            return record
