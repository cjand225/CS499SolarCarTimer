from time import time

class Lap_Time():
    def __init__(self, previousTime = None):
        self.recordedTime = time()
        if previousTime is None:
            self.elapsedTime = None
        else:
            self.elapsedTime = self.recordedTime - previousTime

