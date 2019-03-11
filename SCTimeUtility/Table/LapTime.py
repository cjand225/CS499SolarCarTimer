import datetime, math


class LapTime():
    def __init__(self, timeData):
        self.elapsedTime = timeData

    '''  
        Function: setElapsed
        Parameters: self, timeData
        Return Value: N/A
        Purpose: Allows setting of time data for LapTime when invoked, same as constructing an instance.
    '''

    def setElapsed(self, timeData):
        self.elapsedTime = timeData

    '''  
        Function: getElapsed
        Parameters: self
        Return Value: int of elapsedTime
        Purpose: returns the integer value of the current elapsed time in milliseconds
    '''

    def getElapsed(self):
        return int(self.elapsedTime)

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
        return str(datetime.timedelta(seconds=self.elapsedTime).total_seconds())

    '''  
        Function: __float__
        Parameters: self
        Return Value: float 
        Purpose: re-definition of float() conversion allowing use of float() on LapTime objects.
    '''

    def __float__(self):
        return float(datetime.timedelta(seconds=self.elapsedTime).total_seconds())

    '''  
        Function: __int__
        Parameters: self
        Return Value: int
        Purpose: re-definition of int() conversion allowing use of int() on LapTime objects.
    '''

    def __int__(self):
        return int(math.floor(datetime.timedelta(seconds=self.elapsedTime).total_seconds()))

    '''  
        Function: __sub__
        Parameters: self, other
        Return Value: int
        Purpose: re-definition of - allowing use of - between LapTime objects.
    '''

    def __sub__(self, other):
        return int(self.elapsedTime) - int(other.elapsedTime)

    '''  
        Function: __add__
        Parameters: self, other
        Return Value: int
        Purpose: re-definition of + allowing use of + between LapTime objects.
    '''

    def __add__(self, other):
        return int(self.elapsedTime) + int(other)

    '''  
        Function: __lt__
        Parameters: self, other
        Return Value: boolean
        Purpose: re-definition of < allowing use of < between LapTime objects.
    '''

    def __lt__(self, other):
        return int(self.elapsedTime) < int(other)

    '''  
        Function: __gt__
        Parameters: self, other
        Return Value: boolean
        Purpose: re-definition of >  allowing use of > between LapTime objects.
    '''

    def __gt__(self, other):
        return int(self.elapsedTime) > int(other)

    '''  
        Function: __eq__
        Parameters: self, other
        Return Value: Boolean
        Purpose: re-definition of == allowing use of == between LapTime objects.
    '''

    def __eq__(self, other):
        return int(self.elapsedTime) == int(other)

    '''  
        Function: __le__
        Parameters: self, other
        Return Value: boolean
        Purpose: re-definition of <= allowing use of <= between LapTime objects.
    '''

    def __le__(self, other):
        return int(self.elapsedTime) <= int(other)

    '''  
        Function: __ge__
        Parameters: self, other
        Return Value: boolean
        Purpose: re-definition of >= allowing use of >= between LapTime objects.
    '''

    def __ge__(self, other):
        return int(self.elapsedTime) >= int(other)

    '''  
        Function: __abs__
        Parameters: self
        Return Value: + float or int
        Purpose: re-definition of absolute value conversion allowing use of abs() on LapTime objects.
    '''

    def __abs__(self):
        return abs(self.elapsedTime)
