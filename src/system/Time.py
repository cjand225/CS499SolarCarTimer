from time import time

class Lap_Time():
    def __init__(self, recordedTime, elapsedTime = None):
        self.recordedTime = recordedTime
        self.elapsedTime = elapsedTime


    @classmethod
    def fromCurrentTime(cls, previousTime = None):
        recordedTime = time()
        if previousTime is None:
            elapsedTime = None
        else:
            elapsedTime = recordedTime - previousTime
        return cls(recordedTime,elapsedTime)

    # def __eq__(self, other):
    #     return (self.recordedTime == other.recordedTime) and (self.elapsedTime == other.elapsedTime)

    # def __ne__(self, other):
    #     return not self == other
