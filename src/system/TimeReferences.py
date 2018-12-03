import datetime
import time
from src.log.Log import getInfoLog, getCriticalLog, getDebugLog, getErrorLog, getWarningLog


def strptimeMultiple(text,formats):
    for f in formats:
        try:
            return datetime.datetime.strptime(text,f)
        except ValueError:
            pass
    raise ValueError()
# def strptimeMultiple(text, formats):
#   myForm = None
#   for f in formats:
#     try:
#       if datetime.datetime.strptime(text, f).time() is not None:
#         return str(datetime.datetime.strptime(text, f).time())
#     except ValueError:
#       pass
#   return myForm


def splitTimes(text):
  delta = None

  if text.isdigit():
    # hours/min/sec
    if len(text) > 4:
      hour = int(text[4:])
      min = int(text[2:3])
      sec = int(text[0:1])

      delta = datetime.timedelta(hours=hour, minutes=min, seconds=sec).total_seconds()
    # Minutes/sec
    elif len(text) > 2 and len(text) <= 3:
      min = int(text[0:2])
      sec = int(text[2:])

      print([min, sec])
      print('\n')

      delta = datetime.timedelta(minutes=min, seconds=sec).total_seconds()
    # seconds
    elif len(text) >= 1 and len(text) <= 2:
      sec = int(text)
      delta = datetime.timedelta(seconds=sec).total_seconds()
    # throw out bad data
    else:
      delta = datetime.timedelta(seconds=0).total_seconds()

  return int(delta)


class LapTime():
  def __init__(self, timeData):
    self.elapsedTime = timeData

  def setElapsed(self, timeData):
    self.elapsedTime = timeData

  def getElapsed(self):
    return int(self.elapsedTime)

  def __str__(self):
    return str(round(datetime.timedelta(seconds=self.elapsedTime)))

  def __int__(self):
      return int(datetime.timedelta(seconds=self.elapsedTime).total_seconds())

  def __sub__(self, other):
      sub = int(self.elapsedTime) - other
      return sub

