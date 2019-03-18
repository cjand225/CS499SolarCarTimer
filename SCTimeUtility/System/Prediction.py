"""

    Module:
    Purpose:
    Depends On:

"""
import math, numpy as np, scipy.stats

from SCTimeUtility.Table.LapTime import LapTime
from SCTimeUtility.Log.Log import getLog

'''  
    Function: predictNextLapTime
    Parameters: lapTimes (lists
    Return Value: LapTime Object
    Purpose: Returns an estimated approximation on when the next lap will occur based on the current laps
             provided by the lapTimes parameter.
'''


def predictNextLapTime(lapTimes):
    # Returns the predicted time for the next lap.
    if len(lapTimes) > 1:
        percentile = 0.05
        elapsedArr = np.array([t.elapsedTime for t in lapTimes])
        sampleMean = np.mean(elapsedArr)
        sampleStd = np.std(elapsedArr, ddof=1)
        t = scipy.stats.t.ppf(percentile, len(lapTimes) - 1)
        lower = sampleMean + (t * sampleStd * math.sqrt(1 + (1 / float(len(lapTimes)))))
    elif len(lapTimes) == 1:
        lower = lapTimes[0].elapsedTime
    else:
        raise LapPredictionError("Need at least one lap time to predict.")
    newestTime = max(lapTimes, key=lambda t: t.recordedTime)
    return LapTime(newestTime.recordedTime + lower, lower)


class LapPredictionError(Exception):
    pass
