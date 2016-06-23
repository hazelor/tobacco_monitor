# coding=utf-8
from base import base_handler
import redis
import os,sys
import json
import time
import tornado
from model.position import Position_Data, Position_Image
from model.data import Data_Table_Map,Data, DataParser
from model.device import Device
from model.image import Image
from util import *
from util.marcos import *

class api_data_handler(base_handler):
    def post(self):
        jdatas = json.loads(self.request.body)
        for jdata in jdatas:

            device_mac = jdata['mac']
            data_content = jdata['data_content']
            #insert the new data to redis
            r=redis.Redis()
            r.set("col_datas_%s"%(device_mac), data_content)
            #get the last table in redis and if there is not a record in redis and get the newest record in the table map
            index = r.get("last_table_index")
            if not index:
                index = Data_Table_Map.get_last_table_index()
            print "last index:", index
            dtm = Data_Table_Map.find_first("where `index`=?", int(index))
            if dtm == None:
                Data_Table_Map.add_table(index)
            
            #parse the data
            #insert into the table
            #if the line of table more than 20w records then create a new table and update table map in the database
            date = data_content['date']
            content = data_content['content']
            dev = Device()
            dev = dev.get_device_by_mac(device_mac)
            DataParser.get_instance().parse_dev(index, dev.id, dev.dev_type,  content)
        self.write('ok')

class api_image_handler(base_handler):
    def post(self):

        file_metas=self.request.files['file']
        if len(file_metas) > 0:
            device_mac = self.get_argument('mac', '')
            device_pos = self.get_argument('pos', '')
            created_at = self.get_argument('date',time.time())
            print device_mac, device_pos, created_at
            meta = file_metas[0]
            res = self.img_upload(device_mac, device_pos,created_at, meta)
            if res:
                self.on_upload_success(res)

    def img_upload(self, device_mac, device_pos,created_at, meta):
        if device_mac == "":
            return False

        if device_pos == "":
            return False
        dev = Device()
        pos = Position_Image()
        #print "upload_img",device_mac,device_pos

        dev = dev.get_device_by_mac(device_mac)
        position_id = pos.get_position_id(dev.id, device_pos)
        print "upload",dev.id,position_id
        upload_path = os.path.join(get_pwd_dir(), CAPTURED_DIR)
        filename = meta['filename']
        filename = os.path.basename(filename)
        print filename,'----',upload_path

        filepath = os.path.join(upload_path, filename)
        with open(filepath, 'wb') as up:
            up.write(meta['body'])

        img = Image()
        img.path = filename
        img.position_id = position_id
        img.created_at = created_at
        img_id = img.create()
        r=redis.Redis()
        r.set('image_path_%s_%s'%(device_mac, device_pos),img.path)
        print img_id
        if not img_id:
            return False
        return True
    def on_upload_success(self, resp):
        if resp:
            self.write('ok')
        else:
            self.write('fail')
