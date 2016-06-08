# coding=utf-8
from model.device import Device
from model.device_observed import Device_Observed
from model.image import Image
from model.position import Position_Image
from model.data import Data, Data_Table_Map
from model.user import User

import sys

def connect_db():
    import transwarp.db as dbutil
    dbutil.create_engine('sonic513', 'sonic513', 'tobacco_monitor', port=3306)

if __name__=="__main__":
    connect_db()
    #dev = Device()
    #dev.create_table()
    #usr = User()
    #usr.create_table()
    #doed = Device_Observed()
    #doed.create_table()
    #dtm = Data_Table_Map()
    #dtm.create_table()
    #img = Image()
    #img.create_table()
    #pos_image = Position_Image()
    #pos_image.create_table()
    #data = Data()
    #data.create_table()

    
