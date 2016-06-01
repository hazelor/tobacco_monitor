# coding=utf-8
from model.device import Device
import sys

def connect_db():
    import transwarp.db as dbutil
    dbutil.create_engine('sonic513', 'sonic513', 'tobacco_monitor')

if __name__=="__main__":
    connect_db()
    location = sys.argv[1]
    mac = sys.argv[2]

    dev = Device(location = location, mac=mac)
    id= dev.create()
    if id:
        print "add dev %s OK!" % mac
    else:
        print "add dev error!"