JSON_BASE_DIR = 'E:/pycharm/railway/DB'
DB_NAME = 'E:/pycharm/railway/DB/Train_System.db'
SQL_DIR = 'E:/pycharm/railway/DB/SQL'
IMG_DIR = 'E:/pycharm/railway/GUI/IMG'

#存放类(随时改变)
passenger_list = []
station_list = []
train_list = []
worker_list = []

#存放关系(随时该百年，关闭后保存最终版到.json文件中)
pass_list = []
record_list = []
regard_list = []
record_dict = {
    "id": [],
    "trainid": [],
    "seatid": [],
    "seatlevel": [],
    "seatprice": []
}
regard_dict = {
    "trainid": [],
    "worktime": [],
    "workid": []
}

#管理操作所需要的信息   regard
test_manage_access = 0
manage_train_infor = {
    "trainid":[],
    "workid":[],
    "worktime":[]
}

# 输出凭证所需要的信息  record
test_buy_success = 0 # 检测所有列表的长度是否相同，一一对应
buy_ticket_infor = {
    "id": None,
    "trainid": None,
    "seatid": None,
    "beginplace": None,
    "endplace": None,
    "begintime": None,
    "endtime": None,
    "seatlevel": None,
    "seatprice": 0.0
}
#保存购买时输入的id
search_bought_train_by_id = ''

#!购买界面数据
#标注tableWidget所选择的行和列车
radio_row = -1
radio_to_train_list = []  # [列车号, 出发时间, 出发地点, 到达时间, 到达地点]

#保存改签前的车次
change_before_train = None

#识别验证码
ocr_code = ''

#保存增加列车的信息
add_train_list = [] #{列车号，出发时间，出发地点，到达时间，到达地点，一等座数量，一等座价格，二等座数量，二等座价格，无座数量，无座价格}
