import time, numpy as np, string, random, sys

from SCTimeUtility.table.LapTime import LapTime


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


def generateLapData(numOfLaps):
    lapList = []
    for x in range(0, numOfLaps):
        lapList.append(time.time())
        sleepAmount = float(random.randrange(0, 100)/1000)
        time.sleep(sleepAmount)
    return lapList


def generateCarData(numOfCars):
    carDataList = [[]]
    carDataList.clear()
    for x in range(0, numOfCars - 1):
        randWordLength = random.randint(0, 20)
        ID = x
        randWord = generateRandomWord(randWordLength)
        randCarNum = random.randint(0, 9999)
        listItem = [ID, randWord, randCarNum]
        carDataList.append(listItem)
    return carDataList


def generateCarInfo(numOfCars):
    carDataList = [[]]
    carDataList.clear()
    for x in range(0, numOfCars):
        randWordLength = random.randint(0, 20)
        randWord = generateRandomWord(randWordLength)
        randCarNum = random.randint(0, 9999)
        listItem = [randWord, randCarNum]
        carDataList.append(listItem)
    return carDataList


def generateRandomWord(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))
