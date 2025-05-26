from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import GUI.ident


class Ident_Window(QMainWindow):
    def __init__(self,function):
        super().__init__()
        self.function = function
        self.ui = GUI.ident.Ui_MainWindow()
        self.ui.setupUi(self)
        # 隐藏外面
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # 鼠标拖拽
        self.dragging = False
        self.drag_position = self.pos()
        # 居中
        self.Location_center()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.drag_position = event.globalPos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.dragging:
            delta = QPoint(event.globalPos() - self.drag_position)
            self.move(self.pos() + delta)
            self.drag_position = event.globalPos()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.dragging = False

    def Location_center(self):
        center = QDesktopWidget().availableGeometry().center()
        x = center.x()
        y = center.y()

        old_x, old_y, width, height = self.frameGeometry().getRect()
        self.move(int(x - width / 2), int(y - height / 2))
        self.move(int(x - width / 2), int(y - height / 2))
        self.move(int(x - width / 2), int(y - height / 2))

