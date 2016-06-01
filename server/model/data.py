#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField
import time,os
import json
from util.marcos import DATA_INFOS_FILE_PATH, MAX_TABLE_LINES
from util import *
from transwarp import db

class DataParser():
    
    __instance = null
    
    @staticmethod
    def get_instance():
        if DataParser.__instance == null:
            DataParser.__instance  = DataParser()
        return DataParser.__instance
    def __init__(self):
        self._data_infos = {}
        data_info_path = os.path.join(get_pwd_dir(), DATA_INFOS_FILE_PATH)
        with open(data_info_path,'r+') as dis:
            contents = dis.readlines()
            contents = [x.strip() for x in contents]
            json_str = ''.join(contents)
            self.data_infos = json.load(json_str)

    def parse_dev(self,  table_index, position_id, dev_type, data_content):
        for dev_info in self._data_infos:
            if dev_info['dev_type'] == dev_type.strip():
                for index in range(min(len(data_content), len(dev_info['data_content']))):
                    d = Data(position_id = position_id, type_id = dev_info['data_content'][index]['type_id'], value = data_content[index])
                    if d.count_all(sub_name = str(table_index)) > MAX_TABLE_LINES:
                        table_index+=1
                        Data.create(sub_name=str(table_index))
                        dtm = Data_Table_Map(end_time = time.time, index = table_index)
                        dtm.insert()

                    d.insert(sub_name=str(table_index))
                    cdtm = Data_Table_Map.find_first('where index = ?', table_index)
                    cdtm.end_time = time.time
                    cdtm.update()

    def parse_to_json(self, dev_type, data_content, date):
        res = []
        for dev_info in self._data_infos:
            if dev_info['dev_type'] == dev_type.strip():
                for index in range(min(len(data_content), len(dev_info['data_content']))):
                    res.append({'name':dev_info['data_content'][index]['name'], 'value': data_content[index]})
        return {"date":date, 'content':res}



class Data(Model):
    __table__ = 'Col_Data'

    id = StringField(primary_key=True, ddl='varchar(32)', default=next_id)
    position_id = StringField(ddl='varchar(32)')
    type_id = StringField(ddl='varchar(32)')
    value = FloatField(ddl='double')
    created_at = FloatField(ddl='double', updatable=False, default=time.time)


class Data_Table_Map(Model):
    id = StringField(primary_key=True, ddl='varchar(32)', default=next_id)
    start_time = FloatField(ddl='double',  default=time.time)
    end_time = FloatField(ddl='double')
    index = IntegerField()

    @classmethod
    def get_last_table_index(cls):
        if cls.count_all() == 0:
            return 0
        else:
            data_table = cls.find_first('order start_time desc')
            if data_table:
                return data_table.index
            else:
                return 0
    @classmethod
    def add_table(cls):
        index = cls.get_last_table_index()
        new_table = cls.__new__()
        new_table.end_time = time.time()
        new_table.index = index+1
        new_table.insert()

    @classmethod
    def get_tables(cls, start_time, end_time):
        return cls.find_by('where start_time<? and end_time>?', start_time, end_time)

     



if __name__=="__main__":
    db.create_engine('sonic513', 'sonic513', 'collection_test', host='127.0.0.1',port='3307')

