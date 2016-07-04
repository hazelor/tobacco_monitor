#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField
import time
from util import CountDownTimer
from util.marcos import DEV_ERROR_COUNT,\
    DEV_STATUS_ERROR, DEV_STATUS_GOOD,\
    DEV_STATUS_INACTIVE, DEV_STATUS_WARNING,\
    DEV_ERROR_DURATION

class Device(Model):
    __table__ = 'device'

    id = StringField(primary_key=True, ddl='varchar(32)', default=next_id)
    location = StringField(ddl='varchar(50)')
    mac = StringField(ddl='varchar(50)')
    dev_type = StringField(ddl='varchar(50)')
    lat = FloatField(ddl='double')
    lon = FloatField(ddl='double')
    status = IntegerField() #0 good; 1 inactive; 2 warning; 3 error
    created_at = FloatField(updatable=False, default=time.time)

    def create(self):
        #print self.location,self.mac
        try:
            if self.location and self.mac:
                self.insert()
                return self.id
            else:
                return None
        except Exception as e:
            return None


    def creator(self, device_id):
        return self.find_first('where id = ?', device_id)

    def update_info(self):
        try:
            if self.location and self.mac:
                dev_info = self.find_first('where mac = ?', self.mac)
                dev_info.location = self.location
                dev_info.update()
                return dev_info.id
            else:
                return None
        except:
            return None

    def get_device_by_mac(self, mac):
        #mac_wrapped = get_md5(mac)

        device = self.find_first('where mac = ?', mac)
        if device:
            return device
        return None



class DeivceStatusChecker(CountDownTimer):
    def __init__(self, seconds):
        dev = Device()
        devs = dev.find_all(sub_name = "")
        self.devs_status = {}
        for dev in devs:
            self.devs_status[dev.mac] = 0
        CountDownTimer.__init__(self, seconds)

    instance = None

    @staticmethod
    def get_instance():
        if DeivceStatusChecker.instance == None:
            DeivceStatusChecker.instance = DeivceStatusChecker(DEV_ERROR_DURATION)
        return DeivceStatusChecker.instance

    def run(self):
        while True:
            CountDownTimer.run(self)
            self.check_status()

    def check_status(self):
        for key, value in self.devs_status.items():
            self.devs_status[key]= self.devs_status[key]+1
            if self.devs_status[key] > DEV_ERROR_COUNT:
                dev = Device()
                dev = dev.get_device_by_mac(key)
                if dev:
                    dev.status = DEV_STATUS_ERROR
                    dev.update()

    def reset_status(self, mac):
        if self.devs_status.has_key(mac):
            self.devs_status[mac] = 0
        else:
            self.devs_status[mac] = 0
        dev = Device()
        dev = dev.get_device_by_mac(mac)
        if dev:
            dev.status = DEV_STATUS_GOOD
            dev.update()

            
