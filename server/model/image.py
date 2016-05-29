#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField
import time,os

class Image(Model):
    __table__ = 'image'

    id = StringField(primary_key=True, ddl='varchar(32)', default=next_id)
    position_id = StringField(ddl='varchar(32)')
    path = StringField(ddl='varchar(200)')
    created_at = FloatField(ddl='double', updatable=False, default=time.time)

    def validate(self):
        if os.path.exists(self.path):
            return True
        return False

    def create(self):
        #self.created_at = time.time()
        try:
            self.insert()
            return self.id
        except:
            return None

    def count_by_position_id(self, position_id):
        return self.count_by('where position_id = ?', position_id)
