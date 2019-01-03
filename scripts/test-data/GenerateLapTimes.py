import time, numpy as np

from SCTimeUtility.system.TimeReferences import LapTime

def generateLapTimes(elapsedMean, elapsedStd, n, seed=None, currentTime=None):
    if seed is not None:
        np.random.seed(seed)
    if currentTime is None:
        currentTime = time.time()
    elapsedTimes = np.random.normal(loc=elapsedMean, scale=elapsedStd, size=n)
    lapTimes = []
    for i in range(n):
        nextTime = currentTime + elapsedTimes[i]
        lapTime = LapTime(nextTime, nextTime - currentTime)
        currentTime = nextTime
        lapTimes.append(lapTime)
    return lapTimes
