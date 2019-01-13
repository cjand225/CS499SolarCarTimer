import datetime, math


class LapTime():
    def __init__(self, timeData):
        self.elapsedTime = timeData

    def setElapsed(self, timeData):
        self.elapsedTime = timeData

    def getElapsed(self):
        return int(self.elapsedTime)

    def __str__(self):
        return str(round(datetime.timedelta(seconds=self.elapsedTime).seconds))

    def __float__(self):
        return float(datetime.timedelta(seconds=self.elapsedTime).total_seconds())

    def __int__(self):
        return int(math.floor(datetime.timedelta(seconds=self.elapsedTime).total_seconds()))

    def __sub__(self, other):
        return int(self.elapsedTime) - int(other.elapsedTime)

    def __add__(self, other):
        return int(self.elapsedTime) + int(other)

    def __lt__(self, other):
        return int(self.elapsedTime) < int(other)

    def __gt__(self, other):
        return int(self.elapsedTime) > int(other)

    def __eq__(self, other):
        return int(self.elapsedTime) == int(other)

    def __le__(self, other):
        return int(self.elapsedTime) <= int(other)

    def __ge__(self, other):
        return int(self.elapsedTime) >= int(other)

    def __abs__(self):
        return abs(self.elapsedTime)
