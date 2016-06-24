#!/usr/bin/env python
# -*- coding: utf-8 -*-
from transwarp.db import next_id
from transwarp.orm import Model, StringField, BooleanField, FloatField, TextField, IntegerField
import time,os
import json
import redis
from util.marcos import CONF_DIR, DATA_INFO_FILENAME,CHART_INFO_FILENAME, MAX_TABLE_LINES,RAINFALL_PRE_SHOT
from util import *
from transwarp import db
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class DataParser():
    
    __instance = None
    
    @staticmethod
    def get_instance():
        if DataParser.__instance == None:
            DataParser.__instance  = DataParser()
        return DataParser.__instance
    def __init__(self):
        self._data_infos = {}
        self._chart_infos = []
        data_info_path = os.path.join(CONF_DIR, DATA_INFO_FILENAME)
        with open(data_info_path,'r+') as dis:
            contents = dis.readlines()
            contents = [x.strip() for x in contents]
            json_str = ''.join(contents)
            #print "the json string:",json_str
            self._data_infos = eval(json_str)
            #print self._data_infos
        chart_info_path = os.path.join(CONF_DIR,CHART_INFO_FILENAME)
        with open(chart_info_path,'r+') as cis:
            contents = cis.readlines()
            contents = [x.strip() for x in contents]
            json_str = ''.join(contents)
            self._chart_infos = eval(json_str)


    def has_type(self, dev_type):
        for dev_info in self._data_infos:
            if dev_info['dev_type'] == dev_type.strip():
                return True
        return False
    def get_data_types(self, dev_type):
        for dev_info in self._data_infos:
            if dev_info['dev_type'] == dev_type.strip():
                return dev_info['data_content']
        return []
    def get_data_type(self, dev_type, type_id):
        for dev_info in self._data_infos:
            if dev_info['dev_type'] == dev_type.strip():
                for data_info in dev_info['data_content']:
                    if data_info['type_id'] == type_id.strip():
                        return data_info
        return {}

    def get_chart_info(self):
        return self._chart_infos


    def parse_dev(self,  table_index, dev_id, dev_type, data_content):
        table_index = int(table_index)
        for dev_info in self._data_infos:
            if dev_info['dev_type'] == dev_type.strip():
                for index in range(min(len(data_content), len(dev_info['data_content']))):
                    d = Data(device_id = dev_id, type_id = dev_info['data_content'][index]['type_id'], value = data_content[index])
                    if d.count_all(sub_name = str(table_index)) > MAX_TABLE_LINES:
                        table_index+=1
                        cdtm = Data_Table_Map.find_first("where `index` = ?", table_index)
                        if cdtm == None:
                            Data_Table_Map.add_table(table_index)
                        #Data.create(sub_name=str(table_index))
                        #dtm = Data_Table_Map(end_time = time.time, index = table_index)
                        #dtm.insert()

                    d.insert(sub_name=str(table_index))
                    cdtm = Data_Table_Map.find_first("where `index` = ?", table_index)
                    cdtm.end_time = time.time()
                    cdtm.update()

    def parse_to_json(self, dev_type, data_content, date, dev_id=""):
        res = []
        for dev_info in self._data_infos:
            if dev_info['dev_type'] == dev_type.strip():
                for index in range(min(len(data_content), len(dev_info['data_content']))):
                    if dev_info['data_content'][index]['duration'] == 0:
                        res.append({'name':dev_info['data_content'][index]['name'],
                                    'type_id':dev_info['data_content'][index]['type_id'],
                                    'unit':dev_info['data_content'][index]['unit'],
                                    'value': data_content[index],
                                    'date':date})
                    else:
                        end_time = int(time.time()/3600)*3600
                        start_time = end_time - 3600
                        tables = Data_Table_Map.get_tables(start_time, end_time)
                        data_list = []
                        for table in tables:
                            data_list.extend(Data.find_by('where device_id = ? and type_id = ? and created_at between ? and ?', dev_id, dev_info['data_content'][index]['type_id'], start_time, end_time, sub_name = str(table.index)))

                        data_list = map(lambda di: di.value,data_list)
                        value = reduce(lambda di_x, di_y:di_x+di_y, data_list)
                        print "rainfall-----:",value
                        res.append({'name':dev_info['data_content'][index]['name'],
                                    'type_id':dev_info['data_content'][index]['type_id'],
                                    'unit':dev_info['data_content'][index]['unit'],
                                    'value': value*RAINFALL_PRE_SHOT,
                                    'date':end_time*1000})
        return res



class Data(Model):
    __table__ = 'col_data'

    id = StringField(primary_key=True, ddl='varchar(32)', default=next_id)
    device_id = StringField(ddl='varchar(50)')
    type_id = StringField(ddl='varchar(50)')
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
            data_table = cls.find_first('order by start_time desc')
            if data_table:
                return data_table.index
            else:
                return 0
    @classmethod
    def add_table(cls,index):
        r = redis.Redis()
        dt = Data()
        dt.create_table(sub_name = str(index))
        r.set("last_table_index",index)
        new_table = Data_Table_Map()
        new_table.end_time = time.time()
        new_table.index = index
        new_table.insert()
    
    

    @classmethod
    def get_tables(cls, start_time, end_time):
        return cls.find_by('where start_time<? and end_time>?', end_time, start_time)

     



if __name__=="__main__":
    db.create_engine('sonic513', 'sonic513', 'tobacco_monitor', host='127.0.0.1',port='3306')
    dtm = Data_Table_Map()
    print dtm.find_first("where 'index'=?",index)

