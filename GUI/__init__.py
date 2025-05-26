from PyQt5.QtWidgets import *
from GUI.Train_Window import Train_Window
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)

    My_Window = Train_Window(function='铁路自动售票系统')
    My_Window.show()

    sys.exit(app.exec_())