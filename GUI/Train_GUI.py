import random
import sys
import ddddocr
from PyQt5 import QtWidgets,QtCore,QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

import DB.Train_DB

from Define import *
import Define

from DB import *
import DB

from Define import *
import Define

def dump_and_close_window(window):
    DB.Train_DB.reload_relations_to_json()
    window.close()

def Search_bought_available_train(id):
    get_bought_train_list = DB.Train_DB.DB_Search_bought_available_train(id)
    return get_bought_train_list

def check_tableWidget_radio_status(tableWidget):
    current_row_count = tableWidget.rowCount()
    current_col_count = tableWidget.columnCount()

    for row in range(current_row_count):
        radio = tableWidget.cellWidget(row,0)
        if radio.isChecked() and isinstance(radio, QRadioButton):
            Define.radio_row = row
            Define.radio_to_train_list = []
            for col in range(1,current_col_count):
                element = tableWidget.item(row,col).text()
                if element[0].isdigit() and element[:5] != '2024-':
                    Define.radio_to_train_list.append(round(float(element),1))
                else:
                    Define.radio_to_train_list.append(element)
            # print('Define.radio_row = ',Define.radio_row)
            # print('Define.radio_to_train_list = ',Define.radio_to_train_list)
            return True

    Define.radio_row = -1
    Define.radio_to_train_list = []
    return False

def Show_TableWidget_Train(tableWidget,available_train_list):
    tableWidget.setColumnWidth(0,50)
    tableWidget.setColumnWidth(2,180)
    tableWidget.setColumnWidth(4,180)
    tableWidget.setRowCount(0) #清除之前的行
    current_row_count = tableWidget.rowCount()

    for train_loc,train_list in enumerate(available_train_list):
        tableWidget.insertRow(current_row_count)
        radio = QRadioButton()
        #radio.clicked.connect(lambda checked,row=train_loc: on_radio_pinned(row,available_train_list[row],radio))
        tableWidget.setCellWidget(current_row_count,0,radio)
        for loc,element in enumerate(train_list):
            getinfo_item = QTableWidgetItem(str(element))
            getinfo_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            tableWidget.setItem(current_row_count,loc+1,getinfo_item)
        current_row_count = current_row_count + 1

def Show_TableWidget_Record(tableWidget,available_train_list):
    tableWidget.setColumnWidth(0,50)
    tableWidget.setColumnWidth(2,200)
    tableWidget.setColumnWidth(4,200)
    tableWidget.setColumnWidth(7,100)
    tableWidget.setRowCount(0)
    current_row_count = tableWidget.rowCount()

    for train_loc,train_list in enumerate(available_train_list):
        tableWidget.insertRow(current_row_count)
        radio = QRadioButton()
        #radio.clicked.connect(lambda checked,row=train_loc: on_radio_pinned(row,available_train_list[row],radio))
        # 清除之前的行
        tableWidget.setCellWidget(current_row_count,0,radio)
        for loc,element in enumerate(train_list):
            getinfo_item = QTableWidgetItem(str(element))
            getinfo_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            tableWidget.setItem(current_row_count,loc + 1,getinfo_item)
        current_row_count += 1

def Digital_Button_to_write_id_check(Label):
    for check_id in passenger_list:
        if check_id.id == Label.text():
            return "yes"
    return "no"

def Digital_Button_to_write_id(stackedWidget_id,stackedWidget,Button,Label,trite="digital",function='',window=None):
    Buttonname = Button.text()
    Origin_id = Label.text()
    if trite == "revocate":
        if len(Origin_id) !=0:
            Origin_id = Origin_id[:len(Origin_id)-1]
            Label.setText(Origin_id)
    elif trite == "enter":
        if Digital_Button_to_write_id_check(Label) == "yes":
            stackedWidget.setCurrentIndex(1)  # 显示第二个界面
            Define.search_bought_train_by_id = str(Label.text())

            # 去除上一次页面操作的radio残余
            Define.radio_row = -1
            Define.radio_to_train_list = []

            if function == "change" or function == "reverse" or function == "get":
                available_train_list = DB.Train_DB.Search_Available_Train_By_Record(Define.search_bought_train_by_id)
                if available_train_list != None:
                    if function == "change":
                        Show_TableWidget_Record(window.ui.tableWidget_train_2, available_train_list)
                    elif function == "reverse":
                        Show_TableWidget_Record(window.ui.tableWidget_train_4, available_train_list)
                    elif function == "get":
                        Show_TableWidget_Record(window.ui.tableWidget_train_5, available_train_list)
                else:
                    if function == "change":
                        Show_TableWidget_Record(window.ui.tableWidget_train_2,[])
                    elif function == "reverse":
                        Show_TableWidget_Record(window.ui.tableWidget_train_4,[])
                    elif function == "get":
                        Show_TableWidget_Record(window.ui.tableWidget_train_5,[])
                        window.ui.stackedWidget_get.setCurrentIndex(2)
        else:
            stackedWidget_id.setCurrentIndex(1)
            QTimer.singleShot(800,lambda:stackedWidget_id.setCurrentIndex(0))
    else:
        Origin_id = Origin_id + str(Buttonname)
        Label.setText(Origin_id)

def Buy_show_search_result_available_train(comboBox_from,comboBox_to,stackedWidget_buy_search,tableWidget_train):  #购买左边的搜索按键
    from_str = comboBox_from.currentText()
    to_str = comboBox_to.currentText()

    if len(from_str)!=0 and len(to_str)!=0:
        available_train_list = DB.Train_DB.Search_Available_Train_By_From_To(from_str,to_str) #从sql中获取
        if len(available_train_list)!=0:
            Show_TableWidget_Train(tableWidget_train,available_train_list)
            stackedWidget_buy_search.setCurrentIndex(2)

            Define.radio_row = -1
            Define.radio_to_train_list = []

        else:
            stackedWidget_buy_search.setCurrentIndex(1)
            QTimer.singleShot(800, lambda: stackedWidget_buy_search.setCurrentIndex(0))
    else:
        stackedWidget_buy_search.setCurrentIndex(1)
        QTimer.singleShot(800,lambda:stackedWidget_buy_search.setCurrentIndex(0))

def Buy_change_from_to(comboBox_from,comboBox_to):
    from_str = comboBox_from.currentText()
    to_str = comboBox_to.currentText()

    if len(from_str)!=0 and len(to_str)!=0:
        comboBox_from.setCurrentText(to_str)
        comboBox_to.setCurrentText(from_str)

def Buy_pinned_available_train(stackedWidget_buy_search,tableWidget):  # Button_enter2
    check_tableWidget_radio_status(tableWidget)
    if Define.radio_row != -1:
        stackedWidget_buy_search.setCurrentIndex(3) # 选座位等级
        Define.buy_ticket_infor['trainid'] = str(Define.radio_to_train_list[0])
        Define.test_buy_success += 1

def Buy_pinned_available_train_choose_seat(parent,radio_seat_level1,radio_seat_level2,radio_seat_level3,init_window): #Button_enter3
    if not radio_seat_level1.isChecked() and not radio_seat_level2.isChecked() and not radio_seat_level3.isChecked():
        parent.ui.stackedWidget_main.setCurrentIndex(1)
        parent.ui.stackedWidget_buy.setCurrentIndex(1)
        parent.ui.stackedWidget_buy_search.setCurrentIndex(3)
        return

    seatprice = 0.0
    is_teenager = 1

    Define.buy_ticket_infor["id"] = Define.search_bought_train_by_id
    Define.test_buy_success += 1

    available_train = DB.Train_DB.Find_element_from_table("TRAIN","TRAINID",Define.buy_ticket_infor["trainid"])
    available_passenger = DB.Train_DB.Find_element_from_table("PASSENGER","ID",Define.buy_ticket_infor["id"])

    if available_train == None or available_passenger == None:
        return

    if available_passenger[0][3] < 18:
        is_teenager = 0.75

    if radio_seat_level1.isChecked():
        Define.buy_ticket_infor['seatlevel'] = str('一等座')
        seatprice = round(available_train[0][6]*is_teenager,1)
        Define.buy_ticket_infor["seatprice"] = seatprice
        Define.test_buy_success += 2
    elif radio_seat_level2.isChecked():
        Define.buy_ticket_infor['seatlevel'] = str('二等座')
        seatprice = round(available_train[0][8]*is_teenager,1)
        Define.buy_ticket_infor["seatprice"] = seatprice
        Define.test_buy_success += 2
    elif radio_seat_level3.isChecked():
        Define.buy_ticket_infor['seatlevel'] = str('无座')
        seatprice = round(available_train[0][10]*is_teenager,1)
        Define.buy_ticket_infor["seatprice"] = seatprice
        Define.test_buy_success += 2

    #生成座位号
    seat_id_loc = chr(random.randint(ord('A'),ord('F')))
    seat_id_loc_2 = random.randint(0,20) + 1

    Define.buy_ticket_infor['seatid'] = str(Define.radio_to_train_list[0] + seat_id_loc + str(seat_id_loc_2))
    Define.buy_ticket_infor['begintime'] = str(Define.radio_to_train_list[1])
    Define.buy_ticket_infor['beginplace'] = str(Define.radio_to_train_list[2])
    Define.buy_ticket_infor['endtime'] = str(Define.radio_to_train_list[3])
    Define.buy_ticket_infor['endplace'] = str(Define.radio_to_train_list[4])
    Define.test_buy_success += 5

    if Define.test_buy_success == 9:
        DB_INFOR = [Define.buy_ticket_infor['id'],Define.buy_ticket_infor['trainid'],Define.buy_ticket_infor["seatid"],Define.buy_ticket_infor["seatlevel"],Define.buy_ticket_infor["seatprice"]]
        if check_modified_seatnum(DB_INFOR[1],DB_INFOR[3]) == True:
            if DB.Train_DB.check_repeat_list("record",Define.record_list,DB_INFOR) == True:
                My_MessageBox = QMessageBox.information(parent, "成功", "购买成功，可前往凭证处取票！", QMessageBox.Ok)
                DB.Train_DB.add_tables("record", DB_INFOR)
            else:
                My_MessageBox = QMessageBox.information(parent,"重复","你购买的列车票已重复！",QMessageBox.Ok)
        else:
            My_MessageBox = QMessageBox.information(parent,"无票",f"你购买的{DB_INFOR[3]}已售罄！",QMessageBox.Ok)
        QTimer.singleShot(800,lambda:init_window)
        Define.test_buy_success = 0
        radio_seat_level1.setChecked(False)
        radio_seat_level2.setChecked(False)
        radio_seat_level3.setChecked(False)
    else:
        print('系统故障，暂时无法购票(购买参数错误)')

    Define.radio_row = -1
    Define.radio_to_train_list = []

def Change_pinned_available_train(stackedWidget_change_search_right,tableWidget_train_left,tableWidget_train_right,seat_radio1,seat_radio2,seat_radio3): #Button_change_search 左边
    check_tableWidget_radio_status(tableWidget_train_left)
    if Define.radio_row != -1:
        Define.change_before_train = Define.radio_to_train_list

        stackedWidget_change_search_right.setCurrentIndex(2) # 显示可以改签的列车
        from_str = Define.radio_to_train_list[2]
        to_str = Define.radio_to_train_list[4]

        from_str = from_str[:2]
        to_str = to_str[:2]

        available_train_list = DB.Train_DB.Search_Available_Train_By_From_To(from_str,to_str)

        # import datetime
        # from_time = datetime.datetime.strptime(Define.radio_to_train_list[1],"%Y-%m-%d %H:%M")
        # for available_train_list_tmp in available_train_list:
        #     from_time_tmp = datetime.datetime.strptime(available_train_list_tmp[1],"%Y-%m-%d %H:%M")
        #     if from_time >= from_time_tmp:
        #         removed_train_list.append(available_train_list_tmp)
        bought_available_trainid_list = [train[1] for train in Define.record_list]
        final_available_train_list = [train for train in available_train_list if train[0] != Define.radio_to_train_list[0] and train[0] not in bought_available_trainid_list]
        if len(final_available_train_list) == 0:
            stackedWidget_change_search_right.setCurrentIndex(1)
            QTimer.singleShot(800,lambda: stackedWidget_change_search_right.setCurrentIndex(0))
        seat_radio1.setChecked(False)
        seat_radio2.setChecked(False)
        seat_radio3.setChecked(False)
        Show_TableWidget_Train(tableWidget_train_right,final_available_train_list)
    else:
        stackedWidget_change_search_right.setCurrentIndex(1) #显示没有改签
        QTimer.singleShot(800,lambda: stackedWidget_change_search_right.setCurrentIndex(0))

def Change_pinned_next_available_train(window=None):  #Button_change_search 右边
    check_tableWidget_radio_status(window.ui.tableWidget_train_3)
    if Define.radio_row != -1:
        changed_train = Define.radio_to_train_list
        window.ui.stackedWidget_change_2.setCurrentIndex(3)

        Define.buy_ticket_infor['id'] = Define.search_bought_train_by_id
        Define.buy_ticket_infor['trainid'] = changed_train[0]
        Define.buy_ticket_infor['begintime'] = changed_train[1]
        Define.buy_ticket_infor['beginplace'] = changed_train[2]
        Define.buy_ticket_infor['endtime'] = changed_train[3]
        Define.buy_ticket_infor['endplace'] = changed_train[4]
        # 生成座位号
        seat_id_loc = chr(random.randint(ord('A'), ord('F')))
        seat_id_loc_2 = random.randint(0, 20) + 1
        Define.buy_ticket_infor['seatid'] = Define.buy_ticket_infor['trainid'] + seat_id_loc + str(seat_id_loc_2)
        Define.test_buy_success += 7

def Change_pinned_seat(window=None):
    if not window.ui.radioButton_change_seatlevel1.isChecked() and not window.ui.radioButton_change_seatlevel2.isChecked() and not window.ui.radioButton_change_seatlevel3.isChecked():
        window.ui.stackedWidget_main.setCurrentIndex(2)
        window.ui.stackedWidget_change.setCurrentIndex(1)
        window.ui.stackedWidget_change_2.setCurrentIndex(3)
        return

    seatprice = 0.0
    is_teenager = 1

    teen_list = [i for i in Define.passenger_list if i.id == Define.search_bought_train_by_id]
    if int(teen_list[0].age) < 18:
        is_teenager = 0.75

    current_train = [i for i in train_list if i.trainid == Define.buy_ticket_infor['trainid']]
    if window.ui.radioButton_change_seatlevel1.isChecked():
        seatprice = round(current_train[0].seat1_price * is_teenager, 1)
        Define.buy_ticket_infor['seatlevel'] = str('一等座')
        Define.buy_ticket_infor['seatprice'] = seatprice
        Define.test_buy_success += 2
    elif window.ui.radioButton_change_seatlevel2.isChecked():
        seatprice = round(current_train[0].seat2_price * is_teenager, 1)
        Define.buy_ticket_infor['seatlevel'] = str('二等座')
        Define.buy_ticket_infor['seatprice'] = seatprice
        Define.test_buy_success += 2
    elif window.ui.radioButton_change_seatlevel3.isChecked():
        seatprice = round(current_train[0].seat3_price * is_teenager, 1)
        Define.buy_ticket_infor['seatlevel'] = str('无座')
        Define.buy_ticket_infor['seatprice'] = seatprice
        Define.test_buy_success += 2

    if Define.test_buy_success == 9:
        DB.Train_DB.delete_tables("record", [Define.search_bought_train_by_id, Define.change_before_train[0]])
        DB.Train_DB.add_tables("record", [Define.buy_ticket_infor['id'], Define.buy_ticket_infor['trainid'],
                                          Define.buy_ticket_infor["seatid"], Define.buy_ticket_infor["seatlevel"],
                                          Define.buy_ticket_infor["seatprice"]])
        My_MessageBox = QMessageBox.information(window, "购票", "改签成功，可前往凭证处取票！", QMessageBox.Ok)
        Define.test_buy_success = 0
        window.ui.radioButton_change_seatlevel1.setChecked(False)
        window.ui.radioButton_change_seatlevel2.setChecked(False)
        window.ui.radioButton_change_seatlevel3.setChecked(False)
        QTimer.singleShot(800, lambda: window.Init_window())
    else:
        print('改签失败，请稍后重试')

def Reverse_pinned_record(window=None):
    check_tableWidget_radio_status(window.ui.tableWidget_train_4)
    if Define.radio_row != -1:
        reversed_train = Define.radio_to_train_list
        DB.Train_DB.delete_tables("record",[Define.search_bought_train_by_id, reversed_train[0]])
        My_MessageBox = QMessageBox.information(window,"退票","退票成功！",QMessageBox.Ok)
        QTimer.singleShot(800,lambda: window.Init_window())

def Get_pinned_ticket(window=None):
    check_tableWidget_radio_status(window.ui.tableWidget_train_5)
    if Define.radio_row != -1:
        element_dict = {
            'id': Define.search_bought_train_by_id,
            'trainid': Define.radio_to_train_list[0],
            'begintime': Define.radio_to_train_list[1],
            'beginplace': Define.radio_to_train_list[2],
            'endtime': Define.radio_to_train_list[3],
            'endplace': Define.radio_to_train_list[4],
            'seatid': Define.radio_to_train_list[5],
            'seatlevel': Define.radio_to_train_list[6],
            'seatprice': Define.radio_to_train_list[7]
        }
        window.Init_Ticket_Window(element_dict)
        window.Ticket_Window.show()

def Message_search_train(stackedWidget,tableWidget,lineEdit):
    sentence = lineEdit.text()
    if len(sentence) != 0:
        infor_list = DB.Train_DB.Decode_place_from_sentence(sentence)
        if infor_list != None:
            if infor_list[0] == 'place':
                from_str = infor_list[1]
                to_str = infor_list[2]
                available_train_list = DB.Train_DB.Search_Available_Train_By_From_To(from_str,to_str)
                if len(available_train_list) > 0:
                    stackedWidget.setCurrentIndex(1)
                    Show_TableWidget_Train(tableWidget, available_train_list)
                else:
                    Show_TableWidget_Train(tableWidget, [])
                    stackedWidget.setCurrentIndex(2)
                    QTimer.singleShot(500, lambda: stackedWidget.setCurrentIndex(0))
            elif infor_list[0] == 'from_place':
                from_str = infor_list[1]
                available_train_list = DB.Train_DB.Search_Available_Train_By_From_To(from_str=from_str)
                if len(available_train_list) > 0:
                    stackedWidget.setCurrentIndex(1)
                    Show_TableWidget_Train(tableWidget, available_train_list)
                else:
                    Show_TableWidget_Train(tableWidget, [])
                    stackedWidget.setCurrentIndex(2)
                    QTimer.singleShot(500, lambda: stackedWidget.setCurrentIndex(0))
            elif infor_list[0] == 'to_place':
                to_str = infor_list[1]
                available_train_list = DB.Train_DB.Search_Available_Train_By_From_To(to_str=to_str)
                if len(available_train_list) > 0:
                    stackedWidget.setCurrentIndex(1)
                    Show_TableWidget_Train(tableWidget, available_train_list)
                else:
                    Show_TableWidget_Train(tableWidget, [])
                    stackedWidget.setCurrentIndex(2)
                    QTimer.singleShot(500, lambda: stackedWidget.setCurrentIndex(0))
            else:
                available_train_list = DB.Train_DB.Search_Available_Train_By_Trainid(infor_list)
                if len(available_train_list) > 0:
                    stackedWidget.setCurrentIndex(1)
                    Show_TableWidget_Train(tableWidget,available_train_list)
                else:
                    Show_TableWidget_Train(tableWidget, [])
                    stackedWidget.setCurrentIndex(2)
                    QTimer.singleShot(500, lambda: stackedWidget.setCurrentIndex(0))
        else:
            if '所有' in sentence.lower() or '全部' in sentence.lower() or 'all' in sentence.lower() or 'ALL' in sentence.lower():
                available_train = DB.Train_DB.Search_Available_Train_All()
                stackedWidget.setCurrentIndex(1)
                Show_TableWidget_Train(tableWidget,available_train)
            else:
                Show_TableWidget_Train(tableWidget, [])
                stackedWidget.setCurrentIndex(2)
                QTimer.singleShot(1000, lambda: stackedWidget.setCurrentIndex(0))
    else:
        Show_TableWidget_Train(tableWidget,[])
        stackedWidget.setCurrentIndex(2)
        QTimer.singleShot(500,lambda: stackedWidget.setCurrentIndex(0))

def Message_code_window(window):
    check_tableWidget_radio_status(window.ui.tableWidget_train_6)
    if Define.radio_row != -1:
        from datetime import datetime
        modified_train = Define.radio_to_train_list

        time_obj = datetime.strptime(modified_train[1],"%Y-%m-%d %H:%M")
        window.ui.comboBox_year1.setCurrentText(str(time_obj.year))
        window.ui.comboBox_month1.setCurrentText("{:02d}".format(time_obj.month))
        window.ui.comboBox_day1.setCurrentText("{:02d}".format(time_obj.day))
        window.ui.comboBox_hour1.setCurrentText("{:02d}".format(time_obj.hour))
        window.ui.comboBox_minute1.setCurrentText("{:02d}".format(time_obj.minute))

        time_obj = datetime.strptime(modified_train[3],"%Y-%m-%d %H:%M")
        window.ui.comboBox_year2.setCurrentText(str(time_obj.year))
        window.ui.comboBox_month2.setCurrentText("{:02d}".format(time_obj.month))
        window.ui.comboBox_day2.setCurrentText("{:02d}".format(time_obj.day))
        window.ui.comboBox_hour2.setCurrentText("{:02d}".format(time_obj.hour))
        window.ui.comboBox_minute2.setCurrentText("{:02d}".format(time_obj.minute))

        window.ui.label_message_from.setText(modified_train[2])
        window.ui.label_message_to.setText(modified_train[4])
        window.ui.label_trainid.setText(modified_train[0])

        code_img_path = Define.IMG_DIR + '/code' + str(random.randint(1,20)) + '.png'

        My_ocr = ddddocr.DdddOcr()
        f = open(code_img_path,mode='rb')
        code_img = f.read()
        Define.ocr_code = My_ocr.classification(code_img)

        pixmap = QtGui.QPixmap(code_img_path)
        if pixmap.isNull():
            print('pixmap error')
            return
        pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
        window.scene.addItem(pixmap_item)
        window.Ident_Window.ui.graphicsView.setScene(window.scene)

        window.Ident_Window.show()

def Message_ident_enter(window,lineEdit_root,lineEdit_code):
    workid = lineEdit_root.text()
    code = lineEdit_code.text()

    if len(workid) != 0 and len(code) != 0:
        if Define.ocr_code == code:
            extract_workid_from_worker_list = [worker.workid for worker in Define.worker_list]
            if workid in extract_workid_from_worker_list:
                window.Ident_Window.close()
                QTimer.singleShot(100,lambda: window.ui.stackedWidget_message.setCurrentIndex(1))
            else:
                window.Ident_Window.ui.stackedWidget_code.setCurrentIndex(2)
                QTimer.singleShot(500, lambda: window.Ident_Window.ui.stackedWidget_code.setCurrentIndex(0))
        else:
            window.Ident_Window.ui.stackedWidget_code.setCurrentIndex(2)
            QTimer.singleShot(500,lambda: window.Ident_Window.ui.stackedWidget_code.setCurrentIndex(0))
    else:
        window.Ident_Window.ui.stackedWidget_code.setCurrentIndex(1)
        QTimer.singleShot(500, lambda: window.Ident_Window.ui.stackedWidget_code.setCurrentIndex(0))

def Message_code_change(window):
    code_img_path = Define.IMG_DIR + '/code' + str(random.randint(1, 20)) + '.png'

    My_ocr = ddddocr.DdddOcr()
    f = open(code_img_path, mode='rb')
    code_img = f.read()
    Define.ocr_code = My_ocr.classification(code_img)

    pixmap = QtGui.QPixmap(code_img_path)
    if pixmap.isNull():
        print('pixmap error')
        return
    pixmap_item = QtWidgets.QGraphicsPixmapItem(pixmap)
    window.scene.addItem(pixmap_item)
    window.Ident_Window.ui.graphicsView.setScene(window.scene)

def check_modified_seatnum(trainid,seatlevel):
    available_train_list = DB.Train_DB.Search_Available_Train_By_Trainid(trainid)
    train = available_train_list[0]
    if seatlevel == '一等座':
        seatnum = train[5]
        return seatnum > 0
    elif seatlevel == '二等座':
        seatnum = train[7]
        return seatnum > 0
    elif seatlevel == '无座':
        seatnum = train[9]
        return seatnum > 0
    else:
        return True

def check_modified_time(begin_time,end_time):
    from datetime import datetime
    begin_time_obj = datetime.strptime(begin_time,"%Y-%m-%d %H:%M")
    end_time_obj = datetime.strptime(end_time,"%Y-%m-%d %H:%M")
    if begin_time_obj < end_time_obj:
        return True
    else:
        return False

def check_modified_trainid(trainid):
    if len(trainid) == 0:
        return False
    if not trainid[0].isupper() or not 'A' <= trainid[0] <= 'Z':
        return False
    for trainid_char in trainid[1:]:
        if not trainid_char.isdigit():
            return False
    return True

def Message_modify_time(window):
    modified_begin_time = [window.ui.comboBox_year1.currentText(),window.ui.comboBox_month1.currentText(),window.ui.comboBox_day1.currentText(),
                           window.ui.comboBox_hour1.currentText(),window.ui.comboBox_minute1.currentText()]
    modified_end_time = [window.ui.comboBox_year2.currentText(),window.ui.comboBox_month2.currentText(),window.ui.comboBox_day2.currentText(),
                         window.ui.comboBox_hour2.currentText(),window.ui.comboBox_minute2.currentText()]
    begin_time = f"{modified_begin_time[0]}-{modified_begin_time[1]}-{modified_begin_time[2]} {modified_begin_time[3]}:{modified_begin_time[4]}"
    end_time = f"{modified_end_time[0]}-{modified_end_time[1]}-{modified_end_time[2]} {modified_end_time[3]}:{modified_end_time[4]}"

    if check_modified_time(begin_time,end_time) == True:
        DB.Train_DB.update_tables("train","trainid",Define.radio_to_train_list[0],"begintime",begin_time)
        DB.Train_DB.update_tables("train","trainid",Define.radio_to_train_list[0],"endtime",end_time)
        My_MessageBox = QMessageBox.information(window,"调整","调整成功",QMessageBox.Ok)
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        DB.Train_DB.add_tables("regard",[Define.radio_to_train_list[0],window.Ident_Window.ui.lineEdit_root.text(),current_time])
        QTimer.singleShot(800,lambda:window.Init_window())

        Define.radio_row = -1
        Define.radio_to_train_list = []
    else:
        My_MessageBox = QMessageBox.information(window,"调整","时间错误，请检查后重试！",QMessageBox.No)

def Message_add_train(window):
    window.Addmenu_Window.ui.lineEdit_seat1num.setPlaceholderText('一等座数量')
    window.Addmenu_Window.ui.lineEdit_seat1price.setPlaceholderText('一等座价格')
    window.Addmenu_Window.ui.lineEdit_seat2num.setPlaceholderText('二等座数量')
    window.Addmenu_Window.ui.lineEdit_seat2price.setPlaceholderText('二等座价格')
    window.Addmenu_Window.ui.lineEdit_seat3num.setPlaceholderText('无座数量')
    window.Addmenu_Window.ui.lineEdit_seat3price.setPlaceholderText('无座价格')
    window.Addmenu_Window.show()

def Message_delete_train(window):
    My_MessageBox = QMessageBox.question(window,'确认删除',
                                         f'您确定要删除列车{Define.radio_to_train_list[0]}吗？',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if My_MessageBox == QMessageBox.Yes:
        DB.Train_DB.delete_tables("train",Define.radio_to_train_list)
        My_MessageBox_delete = QMessageBox.information(
            window,'列车删除',f'成功删除列车{Define.radio_to_train_list[0]}',QMessageBox.Ok)
        Define.radio_row = -1
        Define.radio_to_train_list = []
        QTimer.singleShot(500,lambda: window.Init_window())

def Message_add_train_time_check(ui):
    begin = [ui.comboBox_year3.currentText(),ui.comboBox_month3.currentText(),ui.comboBox_day3.currentText(),ui.comboBox_hour3.currentText(),ui.comboBox_minute3.currentText()]
    end = [ui.comboBox_year4.currentText(),ui.comboBox_month4.currentText(),ui.comboBox_day4.currentText(),ui.comboBox_hour4.currentText(),ui.comboBox_minute4.currentText()]
    if not any(len(str1) == 0 for str1 in begin):
        if not any(len(str2) == 0 for str2 in end):
            begin_time = f"{begin[0]}-{begin[1]}-{begin[2]} {begin[3]}:{begin[4]}"
            end_time = f"{end[0]}-{end[1]}-{end[2]} {end[3]}:{end[4]}"
            if check_modified_time(begin_time,end_time) == True:
                return [begin_time,end_time,True]
            else:
                return ['0000-00-00 00:00','0000-00-00 00:00',False]
        else:
            return ['0000-00-00 00:00', '0000-00-00 00:00', False]
    else:
        return ['0000-00-00 00:00', '0000-00-00 00:00', False]

def Message_add_train_confirm(window):
    #列车是否重复
    trite_list = [maincode.trainid for maincode in Define.train_list]
    trainid = window.Addmenu_Window.ui.lineEdit_trainid.text()
    if len(trainid) != 0:
        if check_modified_trainid(trainid) == True:
            if trainid not in trite_list:
                Define.add_train_list.append(trainid)
                time = Message_add_train_time_check(window.Addmenu_Window.ui)
                #时间是否正确
                if time[2] == True:
                    Define.add_train_list.append(time[0])
                    beginplace = window.Addmenu_Window.ui.comboBox_beginplace.currentText()
                    #出发地是否为空
                    if len(beginplace) != 0:
                        Define.add_train_list.append(beginplace)
                        Define.add_train_list.append(time[1])
                        endplace = window.Addmenu_Window.ui.comboBox_endplace.currentText()
                        #到达地是否为空
                        if len(endplace) != 0:
                            Define.add_train_list.append(endplace)
                            seatnum_list = [window.Addmenu_Window.ui.lineEdit_seat1num.text(),
                                            window.Addmenu_Window.ui.lineEdit_seat2num.text(),window.Addmenu_Window.ui.lineEdit_seat3num.text()]
                            seatprice_list = [window.Addmenu_Window.ui.lineEdit_seat1price.text(),
                                              window.Addmenu_Window.ui.lineEdit_seat2price.text(),window.Addmenu_Window.ui.lineEdit_seat3price.text()]
                            try:
                                seatnum_int_list = [int(i) for i in seatnum_list]
                                try:
                                    seatprice_float_list = [round(float(j),1) for j in seatprice_list]
                                    Define.add_train_list.append(seatnum_int_list[0])
                                    Define.add_train_list.append(seatprice_float_list[0])
                                    Define.add_train_list.append(seatnum_int_list[1])
                                    Define.add_train_list.append(seatprice_float_list[1])
                                    Define.add_train_list.append(seatnum_int_list[2])
                                    Define.add_train_list.append(seatprice_float_list[2])
                                    DB.Train_DB.add_tables("train",Define.add_train_list)
                                    My_MessageBox = (QMessageBox.information
                                                     (window.Addmenu_Window,'添加列车',f'成功添加列车{Define.add_train_list[0]}',QMessageBox.Ok))
                                    Define.add_train_list = []
                                    QTimer.singleShot(500,lambda: window.Init_window())
                                    window.Addmenu_Window.close()
                                except ValueError:
                                    Define.add_train_list = []
                                    window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(3)
                                    QTimer.singleShot(500,lambda: window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(0))
                            except ValueError:
                                Define.add_train_list = []
                                window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(3)
                                QTimer.singleShot(500, lambda: window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(0))
                        else:
                            Define.add_train_list = []
                            window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(4)
                            QTimer.singleShot(500, lambda: window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(0))
                    else:
                        Define.add_train_list = []
                        window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(4)
                        QTimer.singleShot(500, lambda: window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(0))
                else:
                    Define.add_train_list = []
                    window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(2)
                    QTimer.singleShot(500, lambda: window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(0))
            else:
                Define.add_train_list = []
                window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(1)
                QTimer.singleShot(500,lambda: window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(0))
        else:
            Define.add_train_list = []
            window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(5)
            QTimer.singleShot(500, lambda: window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(0))
    else:
        Define.add_train_list = []
        window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(4)
        QTimer.singleShot(500, lambda: window.Addmenu_Window.ui.stackedWidget_status.setCurrentIndex(0))

def Message_add_train_cancel(window):
    Define.add_train_list = []

    self = window

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

    window.Addmenu_Window.close()