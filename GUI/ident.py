# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ident.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(490, 413)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(30, 10, 450, 350))
        self.frame.setMinimumSize(QtCore.QSize(450, 350))
        self.frame.setMaximumSize(QtCore.QSize(450, 350))
        self.frame.setStyleSheet("#frame{\n"
"    border-radius: 20px;\n"
"}\n"
"QLineEdit{\n"
"    background-color: rgb(255, 255, 255);\n"
"    border: none;\n"
"    border-radius: 10px;\n"
"    \n"
"    font: 16pt \"Noto Sans Brahmi\";\n"
"}\n"
"QLabel{\n"
"    font: 16pt \"Noto Sans Brahmi\";\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setStyleSheet("#frame_2{\n"
"        border-top-left-radius:20px;\n"
"        border-top-right-radius:20px;\n"
"    background-color: rgb(28, 113, 216);\n"
"}")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_notice = QtWidgets.QLabel(self.frame_2)
        self.label_notice.setGeometry(QtCore.QRect(157, 12, 151, 27))
        self.label_notice.setStyleSheet("QLabel{\n"
"    \n"
"    color: rgb(255, 255, 255);\n"
"    font: 20pt \"Noto Sans Brahmi\";\n"
"}")
        self.label_notice.setObjectName("label_notice")
        self.Button_close = QtWidgets.QPushButton(self.frame_2)
        self.Button_close.setGeometry(QtCore.QRect(327, 4, 121, 41))
        self.Button_close.setStyleSheet("#Button_close{\n"
"    border:none;\n"
"    background-color: rgba(255, 255, 255,0);\n"
"}")
        self.Button_close.setText("")
        self.Button_close.setObjectName("Button_close")
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(5)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setStyleSheet("background-color: rgb(246, 245, 244);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.Button_enter = QtWidgets.QPushButton(self.frame_3)
        self.Button_enter.setGeometry(QtCore.QRect(329, 180, 71, 41))
        self.Button_enter.setStyleSheet("QPushButton{\n"
"    border: 1px solid;\n"
"    border-radius: 10px;\n"
"    font: 12pt \"Noto Sans Brahmi\";\n"
"}\n"
"QPushButton:pressed{\n"
"    padding-top: 5px;\n"
"    padding-left: 5px;\n"
"}")
        self.Button_enter.setObjectName("Button_enter")
        self.label_code_infor = QtWidgets.QLabel(self.frame_3)
        self.label_code_infor.setGeometry(QtCore.QRect(23, 110, 111, 27))
        self.label_code_infor.setObjectName("label_code_infor")
        self.label_root_infor = QtWidgets.QLabel(self.frame_3)
        self.label_root_infor.setGeometry(QtCore.QRect(20, 30, 101, 31))
        self.label_root_infor.setObjectName("label_root_infor")
        self.lineEdit_root = QtWidgets.QLineEdit(self.frame_3)
        self.lineEdit_root.setGeometry(QtCore.QRect(150, 30, 181, 41))
        self.lineEdit_root.setStyleSheet("QLineEdit{\n"
"    font: 16pt \"Noto Sans Brahmi\";\n"
"    background-color: rgb(255, 255, 255);\n"
"}")
        self.lineEdit_root.setObjectName("lineEdit_root")
        self.lineEdit_code = QtWidgets.QLineEdit(self.frame_3)
        self.lineEdit_code.setGeometry(QtCore.QRect(150, 100, 181, 41))
        self.lineEdit_code.setStyleSheet("QLineEdit{\n"
"    font: 16pt \"Noto Sans Brahmi\";\n"
"    background-color: rgb(255, 255, 255);\n"
"}")
        self.lineEdit_code.setText("")
        self.lineEdit_code.setObjectName("lineEdit_code")
        self.stackedWidget_code = QtWidgets.QStackedWidget(self.frame_3)
        self.stackedWidget_code.setGeometry(QtCore.QRect(330, 100, 71, 41))
        self.stackedWidget_code.setStyleSheet("")
        self.stackedWidget_code.setObjectName("stackedWidget_code")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.stackedWidget_code.addWidget(self.page)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.label_2 = QtWidgets.QLabel(self.page_3)
        self.label_2.setGeometry(QtCore.QRect(0, -4, 85, 41))
        self.label_2.setStyleSheet("QLabel{\n"
"    color: rgb(237, 51, 59);\n"
"    font: 14pt \"Noto Sans Brahmi\";\n"
"}")
        self.label_2.setObjectName("label_2")
        self.stackedWidget_code.addWidget(self.page_3)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.label = QtWidgets.QLabel(self.page_2)
        self.label.setGeometry(QtCore.QRect(0, 10, 85, 27))
        self.label.setStyleSheet("QLabel{\n"
"    color: rgb(237, 51, 59);\n"
"    font: 14pt \"Noto Sans Brahmi\";\n"
"}")
        self.label.setObjectName("label")
        self.stackedWidget_code.addWidget(self.page_2)
        self.graphicsView = QtWidgets.QGraphicsView(self.frame_3)
        self.graphicsView.setGeometry(QtCore.QRect(150, 173, 120, 50))
        self.graphicsView.setMinimumSize(QtCore.QSize(120, 50))
        self.graphicsView.setMaximumSize(QtCore.QSize(120, 50))
        self.graphicsView.setObjectName("graphicsView")
        self.Button_changeing = QtWidgets.QPushButton(self.frame_3)
        self.Button_changeing.setGeometry(QtCore.QRect(13, 192, 131, 35))
        self.Button_changeing.setStyleSheet("QPushButton{\n"
"    border:none;\n"
"    font: 12pt \"Noto Sans Brahmi\";\n"
"    \n"
"    color: rgb(61, 56, 70);\n"
"    background-color: rgba(255, 255, 255,0);\n"
"}\n"
"QPushButton:hover{\n"
"    color: rgb(28, 113, 216);\n"
"}\n"
"QPushButton:pressed{\n"
"    padding-top: 3px;\n"
"    padding-left: 3px;\n"
"}")
        self.Button_changeing.setObjectName("Button_changeing")
        self.verticalLayout.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.frame_4.sizePolicy().hasHeightForWidth())
        self.frame_4.setSizePolicy(sizePolicy)
        self.frame_4.setStyleSheet("#frame_4{\n"
"        border-bottom-left-radius:20px;\n"
"        border-bottom-right-radius:20px;\n"
"    background-color: rgb(28, 113, 216);\n"
"}")
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout.addWidget(self.frame_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget_code.setCurrentIndex(0)
        self.Button_close.clicked.connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_notice.setText(_translate("MainWindow", "权  限  操  作"))
        self.Button_enter.setText(_translate("MainWindow", "确 定"))
        self.label_code_infor.setText(_translate("MainWindow", "验   证   码"))
        self.label_root_infor.setText(_translate("MainWindow", "管 理 账 号"))
        self.label_2.setText(_translate("MainWindow", "  空"))
        self.label.setText(_translate("MainWindow", "  错 误"))
        self.Button_changeing.setText(_translate("MainWindow", "看不清？换一张"))
import svg_rc
