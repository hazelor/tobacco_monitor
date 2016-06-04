__author__ = 'guoxiao'

from serialUtils import *
from updateUtils import *
from commUtils import *
# from confUtils import *
import os, time
import gpio
import redis

if __name__ == "__main__":
    #sync time for devies
    print "start sync time"
    os.system("ntpdate -u ntp.api.bz")

    
    ser = init_serial_port()
    ser = open_serial_port(ser)
    TProcess = CountDownExec.get_instance('serial_update', duration, exe_collection_datas, args={"serial": ser})
    UProcess = CountDownExec.get_instance('net_update', duration, exe_update)
    CProcess = CountDownExec.get_instance('ctrl_update', CTRL_UPDATE_DURATION, exe_ctrl)

    TProcess.start()
    UProcess.start()
    CProcess.start()
