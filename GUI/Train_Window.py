from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


import GUI.lobby
import GUI.Train_GUI
import GUI.Ticket_Window
import GUI.Ident_Window
import GUI.Addmenu_Window
import DB.Train_DB


class Train_Window(QMainWindow):
    def __init__(self,function):
        super().__init__()
        self.function = function
        self.ui = GUI.lobby.Ui_MainWindow()
        self.ui.setupUi(self)
        #清理数据库
        self.clear_Sqlite3()
        # 隐藏外面
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # 居中
        self.Location_center()

       #显示时间
        self.Show_time()

        #身份
        self.Ident_Window = GUI.Ident_Window.Ident_Window('ident')
        self.scene = QtWidgets.QGraphicsScene(self.Ident_Window)
        self.Ident_Bind_button()
        #增加列车
        self.Addmenu_Window = GUI.Addmenu_Window.Addmenu_Window('addmenu')
        self.Addmenu_Bind_button()

        #鼠标拖拽
        self.dragging = False
        self.drag_position = self.pos()
        # 按钮绑定(信号与槽)
        self.Bind_button()
        #票
        self.Ticket_Window = GUI.Ticket_Window.Ticket_Window('ticket')

        # 初始化界面
        self.Init_window()

    def clear_Sqlite3(self):
        DB.Train_DB.create_tables()
        DB.Train_DB.clear_tables()
        DB.Train_DB.Init_Train_DB()
    def Location_center(self):
        center = QDesktopWidget().availableGeometry().center()
        x = center.x()
        y = center.y()

        old_x, old_y, width, height = self.frameGeometry().getRect()
        self.move(int(x - width / 2), int(y - height / 2))

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

    def Init_window(self):
        self.ui.stackedWidget_main.setCurrentIndex(0)

        self.ui.stackedWidget_buy.setCurrentIndex(0)
        self.ui.stackedWidget_buy_iderror.setCurrentIndex(0)
        self.ui.stackedWidget_buy_search.setCurrentIndex(0)

        self.ui.stackedWidget_change.setCurrentIndex(0)
        self.ui.stackedWidget_change_iderror.setCurrentIndex(0)
        self.ui.stackedWidget_change_2.setCurrentIndex(0)

        self.ui.stackedWidget_reverse.setCurrentIndex(0)
        self.ui.stackedWidget_reverse_iderror.setCurrentIndex(0)

        self.ui.stackedWidget_get.setCurrentIndex(0)
        self.ui.stackedWidget_get_iderror.setCurrentIndex(0)

        self.ui.stackedWidget_message.setCurrentIndex(0)
        self.ui.stackedWidget_message_showtrain.setCurrentIndex(0)

        self.ui.lineEdit_message_searchtrain.clear()
        self.ui.tableWidget_train_6.setRowCount(0)

        #清除字符串
        self.ui.label_showid.clear()
        self.ui.label_showid2.clear()
        self.ui.label_showid3.clear()
        self.ui.label_showid4.clear()

        #清除管理员字符串
        self.Ident_Window.ui.lineEdit_root.clear()
        self.Ident_Window.ui.lineEdit_code.clear()

        #清除购买搜索信息
        self.ui.comboBox_from.setCurrentIndex(0)
        self.ui.comboBox_to.setCurrentIndex(0)
        self.ui.stackedWidget_buy_search.setCurrentIndex(0)

        # 清除添加列车窗口的信息
        self.Addmenu_Window.ui.lineEdit_trainid.clear()
        self.Addmenu_Window.ui.comboBox_year3.setCurrentIndex(0)
        self.Addmenu_Window.ui.comboBox_month3.setCurrentIndex(0)
        self.Addmenu_Window.ui.comboBox_day3.setCurrentIndex(0)
        self.Addmenu_Window.ui.comboBox_hour3.setCurrentIndex(0)
        self.Addmenu_Window.ui.comboBox_minute3.setCurrentIndex(0)
        self.Addmenu_Window.ui.comboBox_beginplace.setCurrentIndex(0)
        self.Addmenu_Window.ui.comboBox_year4.setCurrentIndex(0)
        self.Addmenu_Window.ui.comboBox_month4.setCurrentIndex(0)
        self.Addmenu_Window.ui.comboBox_day4.setCurrentIndex(0)
        self.Addmenu_Window.ui.comboBox_hour4.setCurrentIndex(0)
        self.Addmenu_Window.ui.comboBox_minute4.setCurrentIndex(0)
        self.Addmenu_Window.ui.comboBox_endplace.setCurrentIndex(0)
        self.Addmenu_Window.ui.lineEdit_seat1num.clear()
        self.Addmenu_Window.ui.lineEdit_seat1price.clear()
        self.Addmenu_Window.ui.lineEdit_seat2num.clear()
        self.Addmenu_Window.ui.lineEdit_seat2price.clear()
        self.Addmenu_Window.ui.lineEdit_seat3num.clear()
        self.Addmenu_Window.ui.lineEdit_seat3price.clear()
        self.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(0)

    def Update_time(self):
        currentTime = QDateTime.currentDateTime().toString('yyyy年MM月dd日 hh时mm分ss秒')
        self.ui.label_time.setText(currentTime)

    def Show_time(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: self.Update_time())
        self.timer.start(1000)

    def Init_Ticket_Window(self,element_dict):
        self.Ticket_Window.Set_Ticket_Element(element_dict)

    def Ident_Bind_button(self):
        self.Ident_Window.ui.Button_enter.clicked.connect(lambda: GUI.Train_GUI.Message_ident_enter(self,self.Ident_Window.ui.lineEdit_root,self.Ident_Window.ui.lineEdit_code))
        self.Ident_Window.ui.Button_changeing.clicked.connect(lambda: GUI.Train_GUI.Message_code_change(self))

    def Addmenu_Bind_button(self):
        self.Addmenu_Window.ui.Button_add_enter.clicked.connect(lambda: GUI.Train_GUI.Message_add_train_confirm(self))
        self.Addmenu_Window.ui.Button_add_cancel.clicked.connect(lambda: GUI.Train_GUI.Message_add_train_cancel(self))

    def Bind_button(self):
        #关闭主页
        self.ui.Button_header_cancel.clicked.connect(lambda:GUI.Train_GUI.dump_and_close_window(self))

        #返回主页
        self.ui.Button_return1.clicked.connect(lambda: self.Init_window())
        self.ui.Button_return2.clicked.connect(lambda: self.Init_window())
        self.ui.Button_return3.clicked.connect(lambda: self.Init_window())
        self.ui.Button_return4.clicked.connect(lambda: self.Init_window())
        self.ui.Button_return5.clicked.connect(lambda: self.Init_window())
        self.ui.Button_return6.clicked.connect(lambda: self.Init_window())
        self.ui.Button_return7.clicked.connect(lambda: self.Init_window())
        self.ui.Button_return8.clicked.connect(lambda: self.Init_window())
        self.ui.Button_return9.clicked.connect(lambda: self.Init_window())
        self.ui.Button_return10.clicked.connect(lambda: self.Init_window())
        self.ui.Button_return11.clicked.connect(lambda:self.Init_window())

        #主页面跳转
        self.ui.Button_buy_icon.clicked.connect(lambda:self.ui.stackedWidget_main.setCurrentIndex(1))
        self.ui.Button_get_icon.clicked.connect(lambda:self.ui.stackedWidget_main.setCurrentIndex(4))
        self.ui.Button_reverse_icon.clicked.connect(lambda:self.ui.stackedWidget_main.setCurrentIndex(3))
        self.ui.Button_change_icon.clicked.connect(lambda:self.ui.stackedWidget_main.setCurrentIndex(2))
        self.ui.Button_message_icon.clicked.connect(lambda:self.ui.stackedWidget_main.setCurrentIndex(5))

        #逻辑绑定
        #购买输入id
        self.ui.Button_press0.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_buy_iderror,self.ui.stackedWidget_buy,self.ui.Button_press0,self.ui.label_showid))
        self.ui.Button_press1.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_buy_iderror,self.ui.stackedWidget_buy,self.ui.Button_press1,self.ui.label_showid))
        self.ui.Button_press2.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_buy_iderror,self.ui.stackedWidget_buy,self.ui.Button_press2,self.ui.label_showid))
        self.ui.Button_press3.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_buy_iderror,self.ui.stackedWidget_buy,self.ui.Button_press3, self.ui.label_showid))
        self.ui.Button_press4.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_buy_iderror,self.ui.stackedWidget_buy,self.ui.Button_press4, self.ui.label_showid))
        self.ui.Button_press5.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_buy_iderror,self.ui.stackedWidget_buy,self.ui.Button_press5, self.ui.label_showid))
        self.ui.Button_press6.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_buy_iderror,self.ui.stackedWidget_buy,self.ui.Button_press6, self.ui.label_showid))
        self.ui.Button_press7.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_buy_iderror,self.ui.stackedWidget_buy,self.ui.Button_press7, self.ui.label_showid))
        self.ui.Button_press8.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_buy_iderror,self.ui.stackedWidget_buy,self.ui.Button_press8, self.ui.label_showid))
        self.ui.Button_press9.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_buy_iderror,self.ui.stackedWidget_buy,self.ui.Button_press9, self.ui.label_showid))
        self.ui.Button_revocate.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_buy_iderror,self.ui.stackedWidget_buy,self.ui.Button_revocate,self.ui.label_showid,"revocate"))
        self.ui.Button_enter.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_buy_iderror,self.ui.stackedWidget_buy,self.ui.Button_enter,self.ui.label_showid,"enter","buy",self))

        #购买--搜索列车
        self.ui.Button_buy_fromto_enter.clicked.connect(lambda:GUI.Train_GUI.Buy_show_search_result_available_train(self.ui.comboBox_from,self.ui.comboBox_to,self.ui.stackedWidget_buy_search,self.ui.tableWidget_train))
        self.ui.Button_buy_turn.clicked.connect(lambda: GUI.Train_GUI.Buy_change_from_to(self.ui.comboBox_from,self.ui.comboBox_to))

        #购买--选择购买列车
        self.ui.Button_buy_fromto_enter_2.clicked.connect(lambda:GUI.Train_GUI.Buy_pinned_available_train(self.ui.stackedWidget_buy_search,self.ui.tableWidget_train))
        self.ui.Button_buy_fromto_enter_3.clicked.connect(lambda:GUI.Train_GUI.Buy_pinned_available_train_choose_seat(self,self.ui.radioButton_seatlevel1,self.ui.radioButton_seatlevel2,self.ui.radioButton_seatlevel3,self.Init_window()))

        #改签输入id
        self.ui.Button_press0_2.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_change_iderror,self.ui.stackedWidget_change,self.ui.Button_press0_2,self.ui.label_showid2))
        self.ui.Button_press1_2.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_change_iderror,self.ui.stackedWidget_change,self.ui.Button_press1_2,self.ui.label_showid2))
        self.ui.Button_press2_2.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_change_iderror, self.ui.stackedWidget_change,self.ui.Button_press2_2, self.ui.label_showid2))
        self.ui.Button_press3_2.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_change_iderror, self.ui.stackedWidget_change,self.ui.Button_press3_2, self.ui.label_showid2))
        self.ui.Button_press4_2.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_change_iderror, self.ui.stackedWidget_change,self.ui.Button_press4_2, self.ui.label_showid2))
        self.ui.Button_press5_2.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_change_iderror, self.ui.stackedWidget_change,self.ui.Button_press5_2, self.ui.label_showid2))
        self.ui.Button_press6_2.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_change_iderror, self.ui.stackedWidget_change,self.ui.Button_press6_2, self.ui.label_showid2))
        self.ui.Button_press7_2.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_change_iderror, self.ui.stackedWidget_change,self.ui.Button_press7_2, self.ui.label_showid2))
        self.ui.Button_press8_2.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_change_iderror, self.ui.stackedWidget_change,self.ui.Button_press8_2, self.ui.label_showid2))
        self.ui.Button_press9_2.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_change_iderror, self.ui.stackedWidget_change,self.ui.Button_press9_2, self.ui.label_showid2))
        self.ui.Button_revocate_2.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_change_iderror, self.ui.stackedWidget_change,self.ui.Button_revocate_2, self.ui.label_showid2,"revocate"))
        self.ui.Button_enter_2.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_change_iderror, self.ui.stackedWidget_change,self.ui.Button_enter_2, self.ui.label_showid2,"enter","change",self))

        #改签 选择要改签的车次后(左边)
        self.ui.Button_change_search.clicked.connect(lambda: GUI.Train_GUI.Change_pinned_available_train(self.ui.stackedWidget_change_2,self.ui.tableWidget_train_2,self.ui.tableWidget_train_3,self.ui.radioButton_change_seatlevel1,self.ui.radioButton_change_seatlevel2,self.ui.radioButton_change_seatlevel3))
        #改签 选择要改签的车次后(右边)
        self.ui.Button_change_enter.clicked.connect(lambda: GUI.Train_GUI.Change_pinned_next_available_train(self))
        self.ui.Button_change_fromto_enter.clicked.connect(lambda: GUI.Train_GUI.Change_pinned_seat(self))

        #退票输入id
        self.ui.Button_press0_3.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_reverse_iderror,self.ui.stackedWidget_reverse,self.ui.Button_press0_3,self.ui.label_showid3))
        self.ui.Button_press1_3.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_reverse_iderror,self.ui.stackedWidget_reverse,self.ui.Button_press1_3,self.ui.label_showid3))
        self.ui.Button_press2_3.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_reverse_iderror,self.ui.stackedWidget_reverse, self.ui.Button_press2_3,self.ui.label_showid3))
        self.ui.Button_press3_3.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_reverse_iderror,self.ui.stackedWidget_reverse, self.ui.Button_press3_3,self.ui.label_showid3))
        self.ui.Button_press4_3.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_reverse_iderror,self.ui.stackedWidget_reverse, self.ui.Button_press4_3,self.ui.label_showid3))
        self.ui.Button_press5_3.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_reverse_iderror,self.ui.stackedWidget_reverse, self.ui.Button_press5_3,self.ui.label_showid3))
        self.ui.Button_press6_3.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_reverse_iderror,self.ui.stackedWidget_reverse, self.ui.Button_press6_3,self.ui.label_showid3))
        self.ui.Button_press7_3.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_reverse_iderror,self.ui.stackedWidget_reverse, self.ui.Button_press7_3,self.ui.label_showid3))
        self.ui.Button_press8_3.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_reverse_iderror,self.ui.stackedWidget_reverse, self.ui.Button_press8_3,self.ui.label_showid3))
        self.ui.Button_press9_3.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_reverse_iderror,self.ui.stackedWidget_reverse, self.ui.Button_press9_3,self.ui.label_showid3))
        self.ui.Button_revocate_3.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_reverse_iderror,self.ui.stackedWidget_reverse, self.ui.Button_revocate_3,self.ui.label_showid3,"revocate"))
        self.ui.Button_enter_3.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_reverse_iderror, self.ui.stackedWidget_reverse, self.ui.Button_enter_3,self.ui.label_showid3,"enter","reverse",self))

        #退票 -- 删除record记录
        self.ui.Button_reverse_enter.clicked.connect(lambda: GUI.Train_GUI.Reverse_pinned_record(self))

        #取票输入id
        self.ui.Button_press0_4.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_get_iderror,self.ui.stackedWidget_get,self.ui.Button_press0_4,self.ui.label_showid4))
        self.ui.Button_press1_4.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_get_iderror,self.ui.stackedWidget_get,self.ui.Button_press1_4,self.ui.label_showid4))
        self.ui.Button_press2_4.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_get_iderror, self.ui.stackedWidget_get,self.ui.Button_press2_4, self.ui.label_showid4))
        self.ui.Button_press3_4.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_get_iderror, self.ui.stackedWidget_get,self.ui.Button_press3_4, self.ui.label_showid4))
        self.ui.Button_press4_4.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_get_iderror, self.ui.stackedWidget_get,self.ui.Button_press4_4, self.ui.label_showid4))
        self.ui.Button_press5_4.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_get_iderror, self.ui.stackedWidget_get,self.ui.Button_press5_4, self.ui.label_showid4))
        self.ui.Button_press6_4.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_get_iderror, self.ui.stackedWidget_get,self.ui.Button_press6_4, self.ui.label_showid4))
        self.ui.Button_press7_4.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_get_iderror, self.ui.stackedWidget_get,self.ui.Button_press7_4, self.ui.label_showid4))
        self.ui.Button_press8_4.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_get_iderror, self.ui.stackedWidget_get,self.ui.Button_press8_4, self.ui.label_showid4))
        self.ui.Button_press9_4.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_get_iderror, self.ui.stackedWidget_get,self.ui.Button_press9_4, self.ui.label_showid4))
        self.ui.Button_revocate_4.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_get_iderror, self.ui.stackedWidget_get,self.ui.Button_revocate_4, self.ui.label_showid4,"revocate"))
        self.ui.Button_enter_4.clicked.connect(lambda: GUI.Train_GUI.Digital_Button_to_write_id(self.ui.stackedWidget_get_iderror, self.ui.stackedWidget_get,self.ui.Button_enter_4, self.ui.label_showid4,"enter","get",self))

        #取票 -- 展现凭证
        self.ui.Button_get_enter.clicked.connect(lambda: GUI.Train_GUI.Get_pinned_ticket(self))

        #查询
        self.ui.Button_message_searchtrain.clicked.connect(lambda: GUI.Train_GUI.Message_search_train(self.ui.stackedWidget_message_showtrain,self.ui.tableWidget_train_6,self.ui.lineEdit_message_searchtrain))
        self.ui.Button_message_roottrain.clicked.connect(lambda: GUI.Train_GUI.Message_code_window(self))

        #查询 -- 确认调整，增加列车，删除列车
        self.ui.Button_modify_enter.clicked.connect(lambda: GUI.Train_GUI.Message_modify_time(self))
        self.ui.Button_modify_add.clicked.connect(lambda: GUI.Train_GUI.Message_add_train(self))
        self.ui.Button_modify_delete.clicked.connect(lambda: GUI.Train_GUI.Message_delete_train(self))
