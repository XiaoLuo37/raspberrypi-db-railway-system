from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import GUI.ticket


class Ticket_Window(QMainWindow):
    def __init__(self,function):
        super().__init__()
        self.function = function
        self.ui = GUI.ticket.Ui_MainWindow()
        self.ui.setupUi(self)
        #隐藏外面
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        #鼠标拖拽
        self.dragging = False
        self.drag_position = self.pos()
        #居中
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

        old_x,old_y,width,height = self.frameGeometry().getRect()
        self.move(int(x - width/2),int(y - height/2))

    def Set_Ticket_Element(self,element_dict):
        beginplace = element_dict['beginplace']
        beginplace = ' '.join(list(beginplace))
        endplace = element_dict['endplace']
        endplace = ' '.join(list(endplace))

        seatlevel = element_dict['seatlevel']
        seatlevel = ' '.join(list(seatlevel))

        from datetime import datetime
        begintime = element_dict['begintime']
        regex = datetime.strptime(begintime,'%Y-%m-%d %H:%M')
        formatted_begintime = regex.strftime('%Y年%m月%d日 %H时%M分')

        self.ui.label_trainid.setText(element_dict['trainid'])
        self.ui.label_from.setText(beginplace)
        self.ui.label_to.setText(endplace)
        self.ui.label_seat.setText(seatlevel)
        self.ui.label_time.setText(formatted_begintime)
        self.ui.label_seatid.setText(element_dict['seatid'])
        self.ui.label_price.setText(str(round(float(element_dict['seatprice']),1)))
        self.ui.label_id.setText(element_dict['id'])
