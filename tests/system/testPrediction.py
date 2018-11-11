import os, sys, unittest
sys.path.insert(0, os.path.abspath("src"))
from time import time
from src.system.Prediction import predictNextLapTime, LapPredictionError
from src.system.Time import Lap_Time
from tests.system.GenerateLapTimes import generateLapTimes


class TestPrediction(unittest.TestCase):
    def testPredictNextLapTime(self):
        epsilon = 0.0005 # Tolerance for rounding error.
        expectedPrediction = 804.7637128 # 0.05 percentile
        elapsedMean = 1000
        elapsedStd = 200
        n = 20
        seed = 0
        lapTimes = generateLapTimes(elapsedMean,elapsedStd,n,seed=seed,currentTime=0)
        self.assertTrue((abs(expectedPrediction-predictNextLapTime(lapTimes).elapsedTime) < epsilon))

    def testSingleLapPrediction(self):
        elapsedTime = 100
        recordedTime = time()
        lapTimes = [Lap_Time(recordedTime,elapsedTime)]
        predictedTime = predictNextLapTime(lapTimes)
        self.assertEqual(predictedTime.elapsedTime,elapsedTime)
        self.assertEqual(abs(predictedTime.recordedTime-recordedTime)-elapsedTime,0)

    def testNoDataLapPrediction(self):
        lapTimes = []
        self.assertRaises(LapPredictionError,predictNextLapTime,lapTimes)
