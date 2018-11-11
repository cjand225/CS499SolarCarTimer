from time import time
import numpy as np
from src.system.Time import Lap_Time

def generateLapTimes(elapsedMean,elapsedStd,n,seed=None,currentTime=None):
    if seed is not None:
        np.random.seed(seed)
    if currentTime is None:
        currentTime = time()
    elapsedTimes = np.random.normal(loc=elapsedMean,scale=elapsedStd,size=n)
    lapTimes = []
    for i in range(n):
        nextTime = currentTime + elapsedTimes[i]
        lapTime = Lap_Time(nextTime, nextTime - currentTime)
        currentTime= nextTime
        lapTimes.append(lapTime)
    return lapTimes
    
