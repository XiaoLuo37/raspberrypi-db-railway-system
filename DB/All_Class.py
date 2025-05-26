import sqlite3
import Define

#乘客
class passenger:
    def __init__(self,id,name,gender,age,telephone,stationname):
        self.id = id
        self.name = name
        self.gender = gender
        self.age = age
        self.telephone = telephone
        self.stationname = stationname

    def load_passenger_table(self):
        connect = sqlite3.connect(Define.DB_NAME)
        cursor = connect.cursor()
        cursor.execute("INSERT INTO PASSENGER VALUES(?,?,?,?,?,?);",self.id,self.name,self.gender,self.age,self.telephone,self.stationname)
        connect.commit()
        connect.close()

#车站
class station:
    def __init__(self,cityname,stationname):
        self.cityname = cityname
        self.stationname = stationname

    def open_db(self):
        self.connect = sqlite3.connect(Define.DB_NAME)

    def load_station_table(self):
        connect = sqlite3.connect(Define.DB_NAME)
        cursor = connect.cursor()
        cursor.execute("INSERT INTO STATION VALUES(?,?);",self.stationname,self.cityname)
        connect.commit()
        connect.close()

#列车
class train:
    def __init__(self,trainid,begintime,beginplace,endtime,endplace,seat1_num,seat1_price,seat2_num,seat2_price,seat3_num,seat3_price):
        self.trainid = trainid
        self.begintime = begintime
        self.beginplace = beginplace
        self.endtime = endtime
        self.endplace = endplace
        self.seat1_num = seat1_num
        self.seat1_price = seat1_price
        self.seat2_num = seat2_num
        self.seat2_price = seat2_price
        self.seat3_num = seat3_num
        self.seat3_price = seat3_price

    def load_train_table(self):
        connect = sqlite3.connect(Define.DB_NAME)
        cursor = connect.cursor()
        cursor.execute("INSERT INTO TRAIN VALUES(?,?,?,?,?,?,?,?,?,?,?);",self.trainid,self.begintime,self.beginplace,self.endtime,self.endplace,self.seat1_num,self.seat1_price,self.seat2_num,self.seat2_price,self.seat3_num,self.seat3_price)
        connect.commit()
        connect.close()

#管理员
class worker:
    def __init__(self,workid,workage):
        self.workid = workid
        self.workage = workage

    def load_worker_table(self):
        connect = sqlite3.connect(Define.DB_NAME)
        cursor = connect.cursor()
        cursor.execute("INSERT INTO WORKER VALUES(?,?)",self.workid,self.workage)
        connect.commit()
        connect.close()