"""

    Module:
    Purpose:
    Depends On:

"""
import math, numpy as np, scipy.stats

from SCTimeUtility.Table.LapTime import LapTime
from SCTimeUtility.Log.Log import get_log

'''  
    Function: predictNextLapTime
    Parameters: lapTimes (lists
    Return Value: LapTime Object
    Purpose: Returns an estimated approximation on when the next lap will occur based on the current laps
             provided by the lapTimes parameter.
'''


# TODO
def predict_next_lap_occurrence(lap_list):
    # Returns the predicted time for the next lap.
    if len(lap_list) > 1:
        percentile = 0.05
        elapsed_array = np.array([t.elapsedTime for t in lap_list])
        sample_mean = np.mean(elapsed_array)
        sample_std = np.std(elapsed_array, ddof=1)
        t = scipy.stats.t.ppf(percentile, len(lap_list) - 1)
        lower = sample_mean + (t * sample_std * math.sqrt(1 + (1 / float(len(lap_list)))))
    elif len(lap_list) == 1:
        lower = lap_list[0].elapsedTime
    else:
        raise LapPredictionError("Need at least one lap time to predict.")
    newest_time = max(lap_list, key=lambda t: t.recordedTime)
    return LapTime(newest_time.recordedTime + lower, lower)


class LapPredictionError(Exception):
    pass
