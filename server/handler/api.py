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

        device_mac = jdatas['mac']
        device_pos = jdatas['pos']
        data_content = jdatas['data_content']
        #insert the new data to redis
        r=redis.Redis()
        r.hmset("col_datas_%s_%s"%(device_mac, device_pos), data_content)
        #get the last table in redis and if there is not a record in redis and get the newest record in the table map
        index = r.hget("last_table_index")
        if not index:
            index = Data_Table_Map.get_last_table_index()
        #parse the data
        #insert into the table
        #if the line of table more than 20w records then create a new table and update table map in the database
        date = data_content['date']
        content = data_content['content']
        dev = Device()
        pos = Position_Data()
        device_id = dev.get_device_by_mac(device_mac)
        dev = dev.creator(device_id)
        position_id = pos.get_position_id(device_id, device_pos)
        DataParser.get_instance().parse_dev(index, position_id, dev.device_type,  content)

class api_image_handler(base_handler):
    def post(self):

        file_metas=self.request.files['file']
        if len(file_metas) > 0:
            device_mac = self.get_argument('mac', '')
            device_pos = self.get_argument('pos', '')
            created_at = self.get_argument('created_at',time.time())
            #print device_mac, device_pos, created_at
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

        device_id = dev.get_device_by_mac(device_mac)
        position_id = pos.get_position_id(device_id, device_pos)
        print "upload",device_id,position_id
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
        r.hmset('image_path_%s_%s'%(device_mac, device_pos),image.path)
        print img_id
        if not img_id:
            return False
        return True
    def on_upload_success(self, resp):
        if resp:
            self.write('ok')
        else:
            self.write('fail')