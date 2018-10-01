import sys
from PyQt5.Qt import QApplication
from App import AppWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AppWindow()
    sys.exit(app.exec_())


