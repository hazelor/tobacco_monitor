# coding=utf-8
from model.position import Position_Data
from model.device import Device
from model.data import DataParser
import sys

def connect_db():
    import transwarp.db as dbutil
    dbutil.create_engine('sonic513', 'sonic513', 'tobacco_monitor')

if __name__=="__main__":
    connect_db()
    mac = sys.argv[1]
    position = sys.argv[2]
    pos_type = sys.argv[3]
    duration = sys.argv[4]
    dev = Device.find_first("where mac=?", mac)
    if not DataParser.get_instance().has_type(pos_type):
        print "pos_type error!"
        return None
    if not dev:
        print "device with mac not found!"
        return None

    pos = Position_Data(position = int(position), pos_type=pos_type, device_id = dev.id, duration = duration)
    id= pos.create()
    if id:
        print "add data pos %s OK!" % position
    else:
        print "add data pos error!"