from DB.All_Class import *

import Define
import os
import sys
import json
import sqlite3

BASE_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

def Init_Train_DB():
    create_tables()

    create_views()
    print()

    load_tables("station")
    load_tables("train")
    load_tables("passenger")
    load_tables("worker")
    load_tables("record")
    load_tables("regard")
    load_tables("pass")
    print()

    print('Init tables OK')

def create_trigger(connect):
    cursor = connect.cursor()

    CREATE_SQL_PATH1 = os.path.join(Define.SQL_DIR, 'buy.sql')
    with open(CREATE_SQL_PATH1, 'r') as f:
        sql_script = f.read()
        try:
            cursor.executescript(sql_script)
        except sqlite3.Error as e:
            print(f'create trigger buy error: {e}')

    CREATE_SQL_PATH2 = os.path.join(Define.SQL_DIR, 'reverse.sql')
    with open(CREATE_SQL_PATH2, 'r') as f:
        sql_script = f.read()
        try:
            cursor.executescript(sql_script)
        except sqlite3.Error as e:
            print(f'create trigger reverse error: {e}')

    print('create triggers successfully')

def create_views():
    connect = sqlite3.connect(Define.DB_NAME)
    cursor = connect.cursor()

    CREATE_SQL_PATH = os.path.join(Define.SQL_DIR, 'record.sql')
    with open(CREATE_SQL_PATH, 'r') as f:
        sql_script = f.read()
        try:
            cursor.executescript(sql_script)
        except sqlite3.Error as e:
            print(f'create view error: {e}')
            return

    CREATE_SQL_PATH = os.path.join(Define.SQL_DIR, 'pass.sql')
    with open(CREATE_SQL_PATH, 'r') as f:
        sql_script = f.read()
        try:
            cursor.executescript(sql_script)
        except sqlite3.Error as e:
            print(f'create view error: {e}')
            return

    connect.commit()
    print('create views successfully')
    connect.close()

def create_transactions_for_buy(trainid,seatlevel,record_list):
    connect = sqlite3.connect(Define.DB_NAME)
    cursor = connect.cursor()

    cursor.execute("BEGIN TRANSACTION;")

    try:
        if seatlevel == '一等座':
            sql = "SELECT SEAT1_NUM FROM TRAIN WHERE TRAINID=?"
            cursor.execute(sql,(trainid,))
            seat1_num = cursor.fetchone()
            seat1_num = seat1_num[0]
            if seat1_num <= 0:
                connect.rollback()
                connect.close()
                return False
            else:
                add_tables("record",record_list)
        elif seatlevel == '二等座':
            sql = "SELECT SEAT2_NUM FROM TRAIN WHERE TRAINID=?"
            cursor.execute(sql,(trainid,))
            seat2_num = cursor.fetchone()
            seat2_num = seat2_num[0]
            if seat2_num <= 0:
                connect.rollback()
                connect.close()
                return False
            else:
                add_tables("record", record_list)
        elif seatlevel == '无座':
            sql = "SELECT SEAT3_NUM FROM TRAIN WHERE TRAINID=?"
            cursor.execute(sql, (trainid,))
            seat3_num = cursor.fetchone()
            seat3_num = seat3_num[0]
            if seat3_num <= 0:
                connect.rollback()
                connect.close()
                return False
            else:
                add_tables("record", record_list)
    except sqlite3.Error as e:
        print(f'error: {e}')
        connect.rollback()
        connect.close()
        return False

    connect.commit()
    connect.close()
    return True

def reload_relations_to_json():
    connect = sqlite3.connect(Define.DB_NAME)
    cursor = connect.cursor()

    cursor.execute("SELECT * FROM PASSENGER ORDER BY ID ASC;")
    passenger_list1 = cursor.fetchall()
    PASSENGER_DIR = os.path.join(Define.JSON_BASE_DIR,'SOURCE/passenger.json')
    try:
        with open(PASSENGER_DIR,mode='w',encoding='utf-8') as f:
            json.dump(passenger_list1,f,ensure_ascii=False,indent=4)
    except json.JSONDecodeError:
        print(f'{PASSENGER_DIR} error')

    cursor.execute("SELECT * FROM TRAIN ORDER BY BEGINPLACE ASC;")
    train_list1 = cursor.fetchall()
    TRAIN_DIR = os.path.join(Define.JSON_BASE_DIR, 'SOURCE/train.json')
    try:
        with open(TRAIN_DIR, mode='w', encoding='utf-8') as f:
            json.dump(train_list1, f, ensure_ascii=False, indent=4)
    except json.JSONDecodeError:
        print(f'{TRAIN_DIR} error')

    cursor.execute("SELECT * FROM WORKER ORDER BY WORKID ASC;")
    worker_list1 = cursor.fetchall()
    WORKER_DIR = os.path.join(Define.JSON_BASE_DIR, 'SOURCE/station.json')
    try:
        with open(WORKER_DIR, mode='w', encoding='utf-8') as f:
            json.dump(worker_list1, f, ensure_ascii=False, indent=4)
    except json.JSONDecodeError:
        print(f'{WORKER_DIR} error')

    cursor.execute("SELECT * FROM STATION ORDER BY STATIONNAME ASC;")
    station_list1 = cursor.fetchall()
    STATION_DIR = os.path.join(Define.JSON_BASE_DIR, 'SOURCE/station.json')
    try:
        with open(STATION_DIR, mode='w', encoding='utf-8') as f:
            json.dump(station_list1, f, ensure_ascii=False, indent=4)
    except json.JSONDecodeError:
        print(f'{STATION_DIR} error')

    cursor.execute("SELECT * FROM REGARD ORDER BY WORKID ASC;")
    regard_list1 = cursor.fetchall()
    REGARD_DIR = os.path.join(Define.JSON_BASE_DIR,'EXPORT/regard.json')
    try:
        with open(REGARD_DIR,mode='w',encoding='utf-8') as f:
            json.dump(regard_list1, f, ensure_ascii=False, indent=4)
    except json.JSONDecodeError:
        print(f'{REGARD_DIR} error')

    cursor.execute("SELECT * FROM RECORD ORDER BY ID ASC;")
    record_list1 = cursor.fetchall()
    RECORD_DIR = os.path.join(Define.JSON_BASE_DIR,'EXPORT/record.json')
    try:
        with open(RECORD_DIR,mode='w',encoding='utf-8') as f:
            json.dump(record_list1,f,ensure_ascii=False,indent=4)
    except json.JSONDecodeError:
        print(f'{RECORD_DIR} error')

    cursor.execute("SELECT * FROM PASS_VIEW ORDER BY TRAINID ASC;")
    pass_list1 = cursor.fetchall()
    PASS_DIR = os.path.join(Define.JSON_BASE_DIR,'EXPORT/pass.json')
    try:
        with open(PASS_DIR,mode='w',encoding='utf-8') as f:
            json.dump(pass_list1,f,ensure_ascii=False,indent=4)
    except json.JSONDecodeError:
        print(f'{PASS_DIR} error')

    connect.commit()
    print('reload all tables successfully')
    connect.close()

def clear_tables():
    connect = sqlite3.connect(Define.DB_NAME)
    cursor = connect.cursor()

    cursor.execute("DELETE FROM PASSENGER;")
    cursor.execute("DELETE FROM TRAIN;")
    cursor.execute("DELETE FROM STATION;")
    cursor.execute("DELETE FROM WORKER;")

    cursor.execute("DELETE FROM RECORD;")
    cursor.execute("DELETE FROM PASS;")
    cursor.execute("DELETE FROM REGARD;")

    connect.commit()
    print('clear tables successfully')
    connect.close()

def create_tables():
    connect = sqlite3.connect(Define.DB_NAME)
    cursor = connect.cursor()

    CREATE_SQL_PATH = os.path.join(Define.SQL_DIR,'create.sql')

    with open(CREATE_SQL_PATH,'r') as f:
        sql_script = f.read()
        try:
            cursor.executescript(sql_script)
        except sqlite3.Error as e:
            print(f'create error: {e}')
            return

    create_trigger(connect) #先创建表，再创建触发器

    connect.commit()
    print('create tables successfully')
    connect.close()

def load_tables(choose):
    connect = sqlite3.connect(Define.DB_NAME)
    cursor = connect.cursor()
    choose_dict = {
        "passenger":[6,"ID"],
        "station":[2,"STATIONNAME"],
        "train":[11,"TRAINID"],
        "worker":[2,"WORKID"],
        "pass":[2],
        "record":[5],
        "regard":[3]
    }
    BASE_DIR = Define.JSON_BASE_DIR
    DB_NAME = choose + ".json"
    if choose != "record" and choose != "regard" and choose != "pass":
        DB_DIR = os.path.join(BASE_DIR,"SOURCE",DB_NAME)
    else:
        DB_DIR = os.path.join(BASE_DIR,"EXPORT",DB_NAME)

    try:
        with open(DB_DIR,mode='r',encoding='utf-8') as f:
            try:
                DATAS = f.read()
            except FileNotFoundError:
                with open(DB_DIR,mode='w',encoding='utf-8') as f:
                    pass
                with open(DB_DIR,mode='r',encoding='utf-8') as f:
                    DATAS = f.read()
        DB_LIST = json.loads(DATAS)
    except FileNotFoundError:
        print(f'no {choose}.json')
    except json.JSONDecodeError:
        print(f'no data in {choose}.json')

    placeholders = "?,"*(choose_dict[choose][0]-1)+"?"

    for DB in DB_LIST:
        # 添加sql表
        DB_TUPLE = tuple(DB)
        if choose != "pass" and choose != "record" and choose != "regard":
            cursor.execute(f"INSERT INTO {choose} VALUES({placeholders}) ON CONFLICT ({choose_dict[choose][1]}) DO NOTHING;",DB_TUPLE)
        else:
            cursor.execute(f"SELECT * FROM {choose}")
            EXISTDB_list = cursor.fetchall()
            mark = True
            for DB_CHECK in EXISTDB_list:
                if DB_CHECK[0] == DB[0] and DB_CHECK[1] == DB[1]:
                    mark = False
                    break
            if mark == True:
                sql = f"INSERT INTO {choose} VALUES({placeholders})"
                cursor.execute(sql,DB_TUPLE)

        #添加list表
        if choose == "passenger":
            DB_OBJECT = passenger(DB[0],DB[1],DB[2],DB[3],DB[4],DB[5])
            Define.passenger_list.append(DB_OBJECT)
        elif choose == "station":
            DB_OBJECT = station(DB[0],DB[1])
            Define.station_list.append(DB_OBJECT)
        elif choose == "train":
            DB_OBJECT = train(DB[0],DB[1],DB[2],DB[3],DB[4],DB[5],DB[6],DB[7],DB[8],DB[9],DB[10])
            Define.train_list.append(DB_OBJECT)
        elif choose == "worker":
            DB_OBJECT = worker(DB[0],DB[1])
            Define.worker_list.append(DB_OBJECT)
        elif choose == "pass":
            Define.pass_list.append(list(DB))
        elif choose == "record":
            Define.record_list.append(list(DB))
        elif choose == "regard":
            Define.regard_list.append(list(DB))

    #将视图pass_view的数据导入到pass当中
    if choose == "pass":
        cursor.execute("SELECT * FROM PASS_VIEW;")
        pass_list1 = cursor.fetchall()
        for pass_tmp in pass_list1:
            sql = f"INSERT INTO {choose} VALUES({placeholders});"
            cursor.execute(sql,tuple(pass_tmp))

    #排序
    if choose != "record" and choose != "regard" and choose != "pass":
        sql = f"SELECT * FROM {choose} ORDER BY ? ASC;"
        cursor.execute(sql,(choose_dict[choose][1],))

    connect.commit()
    print(f'load table {choose} successfully')
    connect.close()

def check_repeat_list(DB,DB_LIST,DB_INFOR):
    #检测重复性，用于add
    if DB != "record" and DB != "regard" and DB != "pass":
        for DB_LIST_LOC in DB_LIST:
            if DB_LIST_LOC[0] == DB_INFOR[0]:
                return False
    else:
        for DB_LIST_LOC in DB_LIST:
            if DB_LIST_LOC[0] == DB_INFOR[0] and DB_LIST_LOC[1] == DB_INFOR[1]:
                return False
    return True

def add_tables(DB,DB_INFOR):
    connect = sqlite3.connect(Define.DB_NAME)
    cursor = connect.cursor()
    DB_DICT = {
        "passenger": [6,[],"ID"],
        "station": [2,[],"STATIONNAME"],
        "train": [11,[],"TRAINID"],
        "worker":[2,[],"WORKID"],
        "pass": [2,[]],
        "record":[5,[]],
        "regard":[3,[]]
    }
    DB_DICT[DB][1] = DB_INFOR

    #写入sql表
    placeholders = "?," * (DB_DICT[DB][0] - 1) + "?"
    try:
        DB_TUPLE = tuple(DB_DICT[DB][1])
        if DB != "pass" and DB != "regard" and DB != "record":
            cursor.execute(f'INSERT INTO {DB} VALUES({placeholders}) ON CONFLICT ({DB_DICT[DB][2]}) DO NOTHING;',DB_TUPLE)
        else:
            mark = True
            cursor.execute(f"SELECT * FROM {DB}")
            EXISTDB_list = cursor.fetchall()
            for DB_CHECK in EXISTDB_list:
                if DB_CHECK[0] == DB_DICT[DB][1][0] and DB_CHECK[1] == DB_DICT[DB][1][1]:
                    mark = False
                    break
            if mark == True:
                cursor.execute(f'INSERT INTO {DB} VALUES({placeholders})',DB_TUPLE)
    except sqlite3.Error:
        print(f'add table {DB} error')

    #写入list表
    if DB == "passenger":
        trite_list = [maincode.id for maincode in Define.passenger_list]
        if check_repeat_list("passenger",trite_list,DB_DICT["passenger"][1]) == True:
            new_passenger = passenger(DB_DICT["passenger"][1][0],DB_DICT["passenger"][1][1],DB_DICT["passenger"][1][2],DB_DICT["passenger"][1][3],DB_DICT["passenger"][1][4],DB_DICT["passenger"][1][5])
            Define.passenger_list.append(new_passenger)
    elif DB == "station":
        trite_list = [maincode.stationname for maincode in Define.station_list]
        if check_repeat_list("station",trite_list,DB_DICT["station"][1]) == True:
            new_station = station(DB_DICT["station"][1][0],DB_DICT["station"][1][1])
            Define.station_list.append(new_station)
    elif DB == "train":
        trite_list = [maincode.trainid for maincode in Define.train_list]
        if check_repeat_list("train",trite_list,DB_DICT["train"][1]) == True:
            new_train = train(DB_DICT["train"][1][0],DB_DICT["train"][1][1],DB_DICT["train"][1][2],DB_DICT["train"][1][3],DB_DICT["train"][1][4],DB_DICT["train"][1][5],DB_DICT["train"][1][6],DB_DICT["train"][1][7],DB_DICT["train"][1][8],DB_DICT["train"][1][9],DB_DICT["train"][1][10])
            Define.train_list.append(new_train)
    elif DB == "worker":
        trite_list = [maincode.workid for maincode in Define.worker_list]
        if check_repeat_list("worker",trite_list,DB_DICT["worker"][1]) == True:
            new_worker = worker(DB_DICT["worker"][1][0],DB_DICT["worker"][1][1])
            Define.worker_list.append(new_worker)

    if DB == "record":
        if check_repeat_list("record",Define.record_list,DB_DICT["record"][1]) == True:
            Define.record_list.append(DB_INFOR)
    elif DB == "regard":
        if check_repeat_list("regard",Define.regard_list,DB_DICT["regard"][1]) == True:
            Define.regard_list.append(DB_INFOR)
    elif DB == "pass":
        if check_repeat_list("pass",Define.pass_list,DB_DICT["pass"][1]) == True:
            Define.pass_list.append(DB_INFOR)

    #写入json文件(SOURCE文件夹)
    if DB != "record" and DB != "regard" and DB != "pass":
        BASE_DIR = Define.JSON_BASE_DIR
        DB_NAME = DB + ".json"
        DB_DIR = os.path.join(BASE_DIR, "SOURCE", DB_NAME)

        try:
            with open(DB_DIR,mode='r',encoding='utf-8') as f:
                DATAS = json.load(f)
                mark = True
                for DATA in DATAS:
                    if DATA[0] == DB_INFOR[0]: #第一位是主码
                        mark = False           #重复
                        break
                if mark == True:
                    DATAS.append(DB_INFOR)
        except FileNotFoundError:
            print(f'no {DB}.json')
            return
        except json.JSONDecodeError:
            print(f'no data in {DB}.json')
            return

        #写入json文件
        with open(DB_DIR,mode='w',encoding='utf-8') as f:
            json.dump(DATAS,f,ensure_ascii=False,indent=4)

    connect.commit()
    print(f'add table {DB} successfully')
    connect.close()

def delete_tables(DB,DB_PRIMARY):  #DB_PRIMARY为列表
    connect = sqlite3.connect(Define.DB_NAME)
    cursor = connect.cursor()

    DB_DICT = {
        "passenger": ["ID"],
        "station": ["STATIONNAME"],
        "train": ["TRAINID"],
        "worker": ["WORKID"],
        "pass": ["TRAINID","STATIONNAME"],
        "record": ["ID","TRAINID"],
        "regard": ["TRAINID","WORKID"]
    }

    #删除sql表中
    try:
        if DB != "pass" and DB != "regard" and DB !="record":
            sql = f"DELETE FROM {DB} WHERE {DB_DICT[DB][0]}=?"
            cursor.execute(sql,(DB_PRIMARY[0],))
        else:
            sql = f"DELETE FROM {DB} WHERE {DB_DICT[DB][0]}=? AND {DB_DICT[DB][1]}=?"
            cursor.execute(sql,(DB_PRIMARY[0],DB_PRIMARY[1],))
    except sqlite3.Error:
        print(f'delete table {DB} error')

    #删除json文件
    if DB != "pass" and DB != "regard" and DB != "record":
        BASE_DIR = Define.JSON_BASE_DIR
        DB_NAME = DB + ".json"
        DB_DIR = os.path.join(BASE_DIR, "SOURCE", DB_NAME)

        try:
            with open(DB_DIR,mode='r',encoding='utf-8') as f:
                DATAS = json.load(f)
                DATAS_TMP = [i for i,DEL_DATA in enumerate(DATAS) if DEL_DATA[0] == DB_PRIMARY[0]]
                for i in reversed(DATAS_TMP):
                    del DATAS[i]
        except FileNotFoundError:
            print(f'no {DB}.json')
        except json.JSONDecodeError:
            print(f'no data in {DB}.json')

        # 重新写入json本文件
        with open(DB_DIR,mode='w',encoding='utf-8') as f:
            json.dump(DATAS,f,ensure_ascii=False,indent=4)

    #删除list表
    if DB == "passenger":
        passenger_list_temp = [item for item in Define.passenger_list if not item.id==DB_PRIMARY[0]]
        Define.passenger_list = passenger_list_temp
    elif DB == "station":
        station_list_temp = [item for item in Define.station_list if not item.stationname==DB_PRIMARY[0]]
        Define.station_list = station_list_temp
    elif DB == "train":
        train_list_temp = [item for item in Define.train_list if not item.trainid==DB_PRIMARY[0]]
        Define.train_list = train_list_temp
    elif DB == "worker":
        worker_list_temp = [item for item in Define.worker_list if not item.workid==DB_PRIMARY[0]]
        Define.worker_list = worker_list_temp
    elif DB == "regard":
        regard_list_temp = [item for item in Define.regard_list if item[0] != DB_PRIMARY[0] and item[1] != DB_PRIMARY[1]]
        Define.regard_list = regard_list_temp
    elif DB == "record":
        record_list_temp = [item for item in Define.record_list if item[0] != DB_PRIMARY[0] and item[1] != DB_PRIMARY[1]]
        Define.record_list = record_list_temp

    connect.commit()
    if DB != "pass" and DB != "regard" and DB != "record":
        print(f'delete {DB_PRIMARY[0]} from {DB} successfully')
    else:
        print(f'delete {DB_PRIMARY[0]},{DB_PRIMARY[1]} from {DB} successfully')
    connect.close()

def update_tables(DB,DB_MAINTRITE,DB_MAINVALUE,DB_NEWTRITE,DB_NEWVALUE):
    connect = sqlite3.connect(Define.DB_NAME)
    cursor = connect.cursor()
    sql = f"UPDATE {DB} SET {DB_NEWTRITE}=? WHERE {DB_MAINTRITE}=?"
    cursor.execute(sql,(DB_NEWVALUE,DB_MAINVALUE))

    #修改list表
    if DB == "passenger":
        for DB_TEMP in Define.passenger_list:
            if DB_TEMP.id == DB_MAINVALUE:
                DB_TEMP.DB_NEWTRITE = DB_NEWVALUE
                break
    elif DB == "station":
        for DB_TEMP in Define.station_list:
            if DB_TEMP.stationname == DB_MAINVALUE:
                DB_TEMP.DB_NEWTRITE = DB_NEWVALUE
                break
    elif DB == "train":
        for DB_TEMP in Define.train_list:
            if DB_TEMP.trainid == DB_MAINVALUE:
                DB_TEMP.DB_NEWTRITE = DB_NEWVALUE
                break
    elif DB == "worker":
        for DB_TEMP in Define.worker_list:
            if DB_TEMP.workid == DB_MAINVALUE:
                DB_TEMP.DB_NEWTRITE = DB_NEWVALUE
                break

    #更新json文件
    if DB != "pass" and DB != "record" and DB != "regard":
        BASE_DIR = Define.JSON_BASE_DIR
        DB_NAME = DB + ".json"
        DB_DIR = os.path.join(BASE_DIR, "SOURCE", DB_NAME)

        sql = f"SELECT * FROM {DB}"
        cursor.execute(sql)
        DATAS = cursor.fetchall()
        DATAS_LIST = [list(row) for row in DATAS]

        # 重新写入json本文件
        with open(DB_DIR, mode='w', encoding='utf-8') as f:
            json.dump(DATAS_LIST, f, ensure_ascii=False, indent=4)

    connect.commit()
    print(f'update {DB}.{DB_NEWTRITE} successfully')
    connect.close()

def Search_Available_Train_All():
    connect = sqlite3.connect(Define.DB_NAME)
    cursor = connect.cursor()

    sql = "SELECT * FROM TRAIN"
    cursor.execute(sql)
    available_train_list1 = cursor.fetchall()
    available_train_list2 = [list(available_train) for available_train in available_train_list1]

    connect.commit()
    connect.close()
    return available_train_list2

def Search_Available_Train_By_Trainid(trainid):
    connect = sqlite3.connect(Define.DB_NAME)
    cursor = connect.cursor()

    train_list2 = []
    sql = "SELECT * FROM TRAIN WHERE TRAINID=?"
    if not isinstance(trainid,list):
        cursor.execute(sql,(trainid,))
        train_list1 = cursor.fetchall()
        train_list2 = [list(train) for train in train_list1]
    else:
        for trainid_tmp in trainid:
            cursor.execute(sql,(trainid_tmp,))
            train_list1 = cursor.fetchall()
            if len(train_list1) != 0:
                train_list2.append(list(train_list1[0]))
    connect.commit()
    connect.close()
    return train_list2

def Decode_place_from_sentence(sentence):
    import re
    pattern1 = r'[从]{0,1}\s*([^到\s]+)\s*到\s*([^到\s]+)'
    match1 = re.search(pattern1,sentence)
    if match1:
        from_str = match1.group(1)
        to_str = match1.group(2)
        if len(from_str) >= 2:
            from_str = from_str[-2:]
        if len(to_str) >= 2:
            to_str = to_str[:2]
        return ['place',from_str,to_str]
    else:
        pattern2 = r'[从]{0,1}\s*([^出\s]+)\s*出'
        match2 = re.search(pattern2,sentence)
        if match2:
            from_str = match2.group(1)
            if len(from_str) >= 1:
                from_str = from_str[-2:]
                return ['from_place',from_str]
        else:
            pattern3 = r'[到]{0,1}\s*([^的\s]+)的'
            match3 = re.search(pattern3,sentence)
            if match3:
                to_str = match3.group(1)
                if len(to_str) >= 1:
                    to_str = to_str[-2:]
                    return ['to_place',to_str]
            else:
                pattern4 = r'\b[A-Z][0-9]{1,5}\b'
                matches = re.findall(pattern4,sentence)
                if len(matches) > 0:
                    return matches
    return None

#购票时搜索A地到B地的所有列车
def Search_Available_Train_By_From_To(from_str='',to_str=''):
    connect = sqlite3.connect(Define.DB_NAME)
    cursor = connect.cursor()

    available_train_list = []
    if from_str != "武汉" and to_str != "武汉":
        if len(from_str) != 0 and len(to_str) != 0:
            sql = f"SELECT * FROM TRAIN WHERE BEGINPLACE like ? AND ENDPLACE like ?"
            from_to_params = (f'{from_str}%',f'{to_str}%')
            cursor.execute(sql, from_to_params)
            available_train_list = cursor.fetchall()
        elif len(from_str) != 0 and len(to_str) == 0:
            sql = f"SELECT * FROM TRAIN WHERE BEGINPLACE like ?"
            from_to_params = (f'{from_str}%')
            cursor.execute(sql,from_to_params)
            available_train_list = cursor.fetchall()
        elif len(from_str) == 0 and len(to_str) != 0:
            sql = f"SELECT * FROM TRAIN WHERE ENDPLACE like ?"
            from_to_params = (f'{to_str}%')
            cursor.execute(sql, from_to_params)
            available_train_list = cursor.fetchall()
    elif from_str == "武汉" and to_str != "武汉":
        if len(to_str) != 0:
            sql = f"SELECT * FROM TRAIN WHERE BEGINPLACE IN(?,?,?) AND ENDPLACE like ?"
            from_to_params = ('武昌站','汉口站','武汉站',f'{to_str}%')
            cursor.execute(sql,from_to_params)
            available_train_list = cursor.fetchall()
        else:
            sql = f"SELECT * FROM TRAIN WHERE BEGINPLACE IN(?,?,?)"
            from_to_params = ('武昌站','汉口站','武汉站')
            cursor.execute(sql,from_to_params)
            available_train_list = cursor.fetchall()
    elif to_str == "武汉" and from_str != "武汉":
        if len(from_str) != 0:
            sql = f"SELECT * FROM TRAIN WHERE BEGINPLACE like ? AND ENDPLACE IN(?,?,?)"
            from_to_params = (f'{from_str}%','武昌站','汉口站','武汉站')
            cursor.execute(sql,from_to_params)
            available_train_list = cursor.fetchall()
        else:
            sql = f"SELECT * FROM TRAIN WHERE BEGINPLACE IN(?,?,?)"
            from_to_params = ('武昌站','汉口站','武汉站')
            cursor.execute(sql,from_to_params)

    connect.commit()
    connect.close()
    return available_train_list

def Search_Available_Train_By_Record(id):
    connect = sqlite3.connect(Define.DB_NAME)
    cursor = connect.cursor()

    cursor.execute("PRAGMA table_info(RECORD_VIEW);")
    columns = [column[1] for column in cursor.fetchall()[:-1]]
    sql = f"SELECT {','.join(columns)} FROM RECORD_VIEW WHERE ID={id}"
    try:
        cursor.execute(sql)
        recorded_train_list = cursor.fetchall()
    except sqlite3.Error:
        print(f'search record error')
        return None

    available_record_list = [list(recorded_train) for recorded_train in recorded_train_list]
    #
    # for recorded_train in recorded_train_list:
    #     # 从记录的list表中寻找trainid
    #     recorded_train = list(recorded_train)
    #     for loc, train in enumerate(Define.train_list):
    #         if recorded_train[0] == train.trainid:
    #             recorded_tmp_train = [train.trainid,train.begintime,train.beginplace,train.endtime,train.endplace]
    #             recorded_train = recorded_tmp_train + recorded_train[1:]
    #             available_record_list.append(recorded_train)
    #             break
    connect.commit()
    connect.close()

    if len(available_record_list) == 0:
        return None
    else:
        return available_record_list

def Find_element_from_table(table_name,table_primary_name,table_primary_value):  #购买生成订单时使用
    connect = sqlite3.connect(Define.DB_NAME)
    cursor = connect.cursor()
    target_table = None

    #测试
    sql = f"SELECT * FROM {table_name} WHERE {table_primary_name}=?"
    try:
        cursor.execute(sql,(table_primary_value,))
        target_table = cursor.fetchall()
    except sqlite3.OperationalError:
        print(f'Operational error, {table_name}')

    connect.commit()
    connect.close()
    return target_table

def DB_Search_bought_available_train(id):
    connect = sqlite3.connect(Define.DB_NAME)
    cursor = connect.cursor()
    get_bought_train_list = []

    try:
        sql = f"SELECT trainid FROM RECORD WHERE id=?"
        cursor.execute(sql,(id,))
        get_bought_trainid_list = cursor.fetchall()
    except sqlite3.OperationalError:
        print(f'Operational error, {id}')
        return None
    except sqlite3.ProgrammingError:
        print(f'Programming error, {id}')
        return None

    for trainid_tmp in get_bought_trainid_list:
        try:
            sql = f"SELECT * FROM TRAIN WHERE TRAINID=?"
            cursor.execute(sql,(trainid_tmp))
            from_trainid_get_train = cursor.fetchall()
            from_trainid_get_train = list(from_trainid_get_train[0])  #将存储元组的列表转换成列表
            get_bought_train_list.append(from_trainid_get_train)
        except sqlite3.OperationalError:
            print(f'Operational error, {id}')
            return None

    connect.commit()
    connect.close()
    return get_bought_train_list

