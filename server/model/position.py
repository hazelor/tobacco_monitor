#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'guoxiao'

from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField
import time
from device import Device

class Position(Model):
    __table__ = "position"

    id = StringField(primary_key=True, ddl='varchar(32)', default=next_id)
    device_id = StringField(ddl='varchar(32)')
    position = IntegerField()
    object_name = StringField(ddl='varchar(50)')
    duration = IntegerField()

    def validate(self):
        dev = Device()
        if not dev.creator(self.device_id):
            return False
        if self.duration <=0:
            return False
        return True

    def create(self):
        if not self.validate():
            return
        pos = self.find_first('where device_id = ? and position = ?', self.device_id, self.position)

        if pos:
            self.id = pos.id
            self.update()
        else:
            self.insert()
        return self.id

    def get_position_id(self, device_id, position):
        pos = self.find_first('where device_id = ? and position = ?', device_id, position)
        if not pos:
            return None
        return pos.id

    def get_position_by_device_id(self, device_id):
        pos = self.find_by('where device_id = ?', device_id)
        if pos:
            return pos
        return []



