"""

    Module: LapTime.py
    Purpose:
    Depends On:

"""

import datetime, math


class LapTime():
    def __init__(self, timeData):
        if isinstance(timeData, datetime.timedelta):
            self.elapsedTime = timeData
            self.initialWrite = datetime.datetime.now()
            self.lastWrite = self.initialWrite
        else:
            raise TypeError("Not a valid instance of datetime.")

    '''  
        Function: setElapsed
        Parameters: self, timeData
        Return Value: N/A
        Purpose: Allows setting of time data for LapTime when invoked, same as constructing an instance.
    '''

    def setElapsed(self, timeData):
        self.elapsedTime = timeData
        self.lastWrite = datetime.datetime.now()

    '''  
        Function: getElapsed
        Parameters: self
        Return Value: int of elapsedTime
        Purpose: returns the integer value of the current elapsed time in milliseconds
    '''

    def getElapsed(self):
        return int(self.elapsedTime.total_seconds())

    '''  
        Function: clear
        Parameters: self
        Return Value: N/A
        Purpose: Defaults the elapsed time back to zero.
    '''

    def clear(self):
        self.elapsedTime = 0.0

    '''  
        Function: __str__
        Parameters: self
        Return Value: string
        Purpose: re-definition of str() conversion allowing use of str() on LapTime objects.
    '''

    def __str__(self):
        return str(self.elapsedTime.total_seconds())

    '''  
        Function: __float__
        Parameters: self
        Return Value: float 
        Purpose: re-definition of float() conversion allowing use of float() on LapTime objects.
    '''

    def __float__(self):
        return float(self.elapsedTime.total_seconds())

    '''  
        Function: __int__
        Parameters: self
        Return Value: int
        Purpose: re-definition of int() conversion allowing use of int() on LapTime objects.
    '''

    def __int__(self):
        return int(math.floor(self.elapsedTime.total_seconds()))

    '''  
        Function: __sub__
        Parameters: self, other
        Return Value: int
        Purpose: re-definition of - allowing use of - between LapTime objects.
    '''

    def __sub__(self, other):
        return int(self.elapsedTime.total_seconds()) - int(other.elapsedTime.total_seconds())

    '''  
        Function: __add__
        Parameters: self, other
        Return Value: int
        Purpose: re-definition of + allowing use of + between LapTime objects.
    '''

    def __add__(self, other):
        return int(self.elapsedTime.total_seconds()) + int(other.total_seconds())

    '''  
        Function: __lt__
        Parameters: self, other
        Return Value: boolean
        Purpose: re-definition of < allowing use of < between LapTime objects.
    '''

    def __lt__(self, other):
        return int(self.elapsedTime.total_seconds()) < int(other.total_seconds())

    '''  
        Function: __gt__
        Parameters: self, other
        Return Value: boolean
        Purpose: re-definition of >  allowing use of > between LapTime objects.
    '''

    def __gt__(self, other):
        return int(self.elapsedTime.total_seconds()) > int(other.total_seconds())

    '''  
        Function: __eq__
        Parameters: self, other
        Return Value: Boolean
        Purpose: re-definition of == allowing use of == between LapTime objects.
    '''

    def __eq__(self, other):
        return int(self.elapsedTime.total_seconds()) == int(other.total_seconds())

    '''  
        Function: __le__
        Parameters: self, other
        Return Value: boolean
        Purpose: re-definition of <= allowing use of <= between LapTime objects.
    '''

    def __le__(self, other):
        return int(self.elapsedTime.total_seconds()) <= int(other.total_seconds())

    '''  
        Function: __ge__
        Parameters: self, other
        Return Value: boolean
        Purpose: re-definition of >= allowing use of >= between LapTime objects.
    '''

    def __ge__(self, other):
        return int(self.elapsedTime.total_seconds()) >= int(other.total_seconds())

    '''  
        Function: __abs__
        Parameters: self
        Return Value: + float or int
        Purpose: re-definition of absolute value conversion allowing use of abs() on LapTime objects.
    '''

    def __abs__(self):
        return abs(self.elapsedTime.total_seconds())
