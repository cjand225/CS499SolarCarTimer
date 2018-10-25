'''
Module: App.py
Purpose: Controller for entire application, used to periodically update project with data to and from the
         modal.

'''

from PyQt5.QtCore import *


class App():

    def __init__(self):
        self.mainWindow = None
        self.updateTimer = None
        self.updateTime = 0

        self.initUpdateTimer()


    def initUpdateTimer(self):
        self.updateTimer = QTimer()
        self.updateTime = 1
        self.updateTimer.timeout.connect(self.update)
        self.updateTimer.start(self.updateTime)

    def update(self):
        print("PH")

