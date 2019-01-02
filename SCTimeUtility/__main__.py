from SCTimeUtility.app.App import App
from SCTimeUtility.log.Log import initLogs

if __name__ == '__main__':
    initLogs()
    MyApp = App()
    MyApp.run()
