# coding=utf-8
from model.device import Device
from model.user import User
from model.device_observed import Device_Observed
import sys

def connect_db():
    import transwarp.db as dbutil
    dbutil.create_engine('sonic513', 'sonic513', 'tobacco_monitor')

if __name__=="__main__":
    connect_db()
    user_name = sys.argv[1]
    mac = sys.argv[3]
    dev = Device.find_first("where mac = ?", mac)
    usr = User.find_first("where name = ?", user_name)
    dev_obs = Device_Observed()
    if dev_obs.observe(usr.id, dev.id):
        print "dev observe success!"
    else:
        print "dev observe fail!"