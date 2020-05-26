import time, numpy as np, string, random, sys

from SCTimeUtility.Table.LapTime import LapTime
from SCTimeUtility.Table.Car import Car


def generateLapData(numOfLaps):
    lapList = []
    for x in range(0, numOfLaps):
        sleepAmount = float(random.randrange(0, 100) / 1000)
        lapList.append(time.time() * sleepAmount)
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


def populateStorage(numOfCars, storage):
    carInfo = generateCarInfo(numOfCars)
    for car in carInfo:
        storage.create_car(car[0], car[1])
    return storage

