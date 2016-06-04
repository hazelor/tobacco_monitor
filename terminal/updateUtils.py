#!/usr/bin/env python
#--coding:utf-8--

__author__ = 'guoxiao'

import time,os
import json
import urllib2
import urllib
from commUtils import *
from queueUtils import DataPool
from macros import *
# from confUtils import set_update_duration, get_update_duration
import redis


def update_data(c_data):
    url = "http://{0}:{1}{2}".format(SERVER_URL, UPDATE_PORT, API_DATACHANNEL_URL)
    j_data = json.dumps(c_data)
    req = urllib2.Request(url, j_data)
    try:
        res = urllib2.urlopen(req, timeout = 30)
        if res.read().strip() == RES_SUCCESS:
            return True
        else:
            return False
    except Exception as e:
        return False


def update_ctrl():
    url = "http://{0}:{1}{2}".format(SERVER_URL, UPDATE_PORT, API_CTRL_URL)
    try:
        print get_md5(get_mac_address())
        data = {'mac_address': get_md5(get_mac_address())} 
        j_data = json.dumps(data)
        res = urllib2.urlopen(url, j_data, timeout=30)
        # j_res = json.loads(res.read())
        # print j_res
        # duration = int(j_res['duration'])
        # if duration == get_update_duration():
        #     return
        # set_update_duration(duration)
     
        j_res = res.read()
        #print type(j_res)
        #print j_res
        r=redis.Redis()
        duration = r.get('duration')
        if j_res != '':
            if duration != j_res:
                r.set('duration', j_res)
            duration = int(j_res)
        else:
            if not duration:
                duration = 10
            else:
                duration = int(duration)
        # print type(duration)
        # print duration

        # CountDownExec.get_instance('serial_update').set_duration(duration)
        # CountDownExec.get_instance('net_update').set_duration(duration)
    except Exception as e:
        #return
        print e

def exe_update(args):
    dp = DataPool.get_instance()
    length = dp.get_len() if dp.get_len()<10 else 10
    print 'len:',dp.get_len()

    c_datas = []
    for i in range(length):
        res = dp.pull_data()
        if res:
            c_datas.append(res)
    if c_datas:
        res = update_data(c_datas)
        print 'res:',res
        if not res:
	    dp.g_counts_reboot+=1
            if dp.g_counts_reboot>10:
               os.system("sudo reboot")
            for cd in c_datas:
                dp.push_data(cd)

def exe_ctrl(args):
    update_ctrl()

if __name__ == '__main__':
    os.system("sudo reboot")
    #update_ctrl()
