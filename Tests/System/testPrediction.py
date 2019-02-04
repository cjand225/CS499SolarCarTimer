import os, sys, unittest

sys.path.insert(0, os.path.abspath("SCTimeUtility"))
from time import time
from SCTimeUtility.System.Prediction import predictNextLapTime, LapPredictionError
from SCTimeUtility.Table.LapTime import LapTime
from Tests.System.GenerateLapTimes import generateLapTimes


class TestPrediction(unittest.TestCase):
    def testPredictNextLapTime(self):
        epsilon = 0.0005  # Tolerance for rounding error.
        expectedPrediction = 804.7637128  # 0.05 percentile
        elapsedMean = 1000
        elapsedStd = 200
        n = 20
        seed = 0
        lapTimes = generateLapTimes(elapsedMean, elapsedStd, n, seed=seed, currentTime=0)
        self.assertTrue((abs(expectedPrediction - predictNextLapTime(lapTimes).elapsedTime) < epsilon))

    def testSingleLapPrediction(self):
        elapsedTime = 100
        recordedTime = time()
        lapTimes = [LapTime(recordedTime, elapsedTime)]
        predictedTime = predictNextLapTime(lapTimes)
        self.assertEqual(predictedTime.elapsedTime, elapsedTime)
        self.assertEqual(abs(predictedTime.recordedTime - recordedTime) - elapsedTime, 0)

    def testNoDataLapPrediction(self):
        lapTimes = []
        self.assertRaises(LapPredictionError, predictNextLapTime, lapTimes)
