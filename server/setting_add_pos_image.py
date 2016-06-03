# coding=utf-8
from model.position import Position_Image
from model.device import Device
import sys

def connect_db():
    import transwarp.db as dbutil
    dbutil.create_engine('sonic513', 'sonic513', 'tobacco_monitor', port=3307)

if __name__=="__main__":
    connect_db()
    mac = sys.argv[1]
    position = sys.argv[2]
    object_name = sys.argv[3]
    duration = sys.argv[4]
    dev = Device.find_first("where mac=?", mac)
    if not dev:
        print "device with mac not found!"

    pos = Position_Image(position = int(position), object_name=object_name, device_id = dev.id, duration = duration)
    pos.create_table()
    id= pos.create()
    if id:
        print "add image pos %s OK!" % position
    else:
        print "add image pos error!"
