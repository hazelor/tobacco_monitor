#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'guoxiao'

from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField
import time
from device import Device

class Device_Observed(Model):
    __table__ = "device_observed"

    id = StringField(primary_key=True, ddl='varchar(32)', default=next_id)
    device_id = StringField(ddl='varchar(32)')
    user_id = StringField(ddl='varchar(32)')

    def observe(self, user_id, device_id):
        observed = self.find_first('where user_id = ? and device_id = ?', user_id, device_id)
        if not observed:
            self.user_id = user_id
            self.device_id = device_id
            self.insert()
            return True
        return True

    def unobserve(self, user_id, device_id):
        observed = self.find_first('where user_id = ? and device_id = ?', user_id, device_id)
        if observed:
            observed.delete()
            return True
        return True


    def observed_devices(self, user_id):
        dev_ids = self.find_by('where user_id = ?', user_id)
        devices = []
        dev = Device()
        for dev_id in dev_ids:
            devices.append(dev.creator(dev_id.device_id))
        return devices

    def count_user_devices(self, user_id):
        return self.count_by('where user_id = ?', user_id)