import datetime
from time import time

from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog



def strptimeMultiple(text, formats):
    for f in formats:
        try:
            return datetime.datetime.strptime(text, f)
        except ValueError:
            pass
    raise ValueError()


class Lap_Time():
    def __init__(self, recordedTime, elapsedTime=None):
        self.recordedTime = recordedTime
        self.elapsedTime = elapsedTime

    def __str__(self):
        return str(datetime.timedelta(seconds=self.elapsedTime))

    @classmethod
    def fromCurrentTime(cls, previousTime=None):
        recordedTime = time()
        if previousTime is None:
            elapsedTime = None
        else:
            elapsedTime = recordedTime - previousTime
        return cls(recordedTime, elapsedTime)

    # def __eq__(self, other):
    #     return (self.recordedTime == other.recordedTime) and (self.elapsedTime == other.elapsedTime)

    # def __ne__(self, other):
    #     return not self == other
