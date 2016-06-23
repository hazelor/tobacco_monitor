from base import base_handler
import redis
import tornado, tornado.web
import json
import time
from model.position import Position_Data, Position_Image
from model.device import Device
from model.device_observed import Device_Observed
from model.data import DataParser
from model.image import Image

from util.marcos import *

class data_preview_handler(base_handler):
    @tornado.web.authenticated
    def get(self,*args, **kwargs):
        usr = self.get_current_user()
        device_observed = Device_Observed()
        devices = device_observed.observed_devices(usr.id)
        position = Position_Data()
        if not devices or len(devices) < 1:
            return self.render('no_devices.html', user_name=usr.name, page_name="browser")
        positions = []
        sel_device_id = self.get_argument('sel_device_id','')
        if sel_device_id == "":
            dev = devices[0]
        else:
            dev =Device.get(sel_device_id)

        datas_infos = DataParser.get_instance().get_data_types(dev.dev_type)



        return self.render('preview.html',
                page_name='preview',
                devices = devices,
                sel_dev=dev,
                datas_infos = datas_infos,
                user_name=usr.name,
                )

class data_preview_realtime_handler(base_handler):
    def get(self, *args, **kwargs):
        sel_device_id = self.get_argument('sel_device_id','')
        dev = Device.get(sel_device_id)
        if dev:
            r  = redis.Redis()
            data_content = r.get("col_datas_%s" %(dev.mac))
            data_content = eval(data_content)
            res = DataParser.get_instance().parse_to_json(dev.dev_type, data_content['content'], data_content['date']*1000)
            res = json.dumps(res)
            self.write(res)
            return self.finish()




class img_preview_handler(base_handler):
    @tornado.web.authenticated
    def get(self, *args,**kwargs):
        usr = self.get_current_user()
        device_observed = Device_Observed()
        position = Position_Image()
        image = Image()
        devices = device_observed.observed_devices(usr.id)
        if not devices or len(devices) < 1:
            return self.render('no_devices.html', user_name=usr.name, page_name="browser")

        positions = []
        for dev in devices:
            positions.extend(position.get_position_by_device_id(dev.id))
        current_position_id = self.get_argument('position_id', '')
        current_page = self.get_argument('page', '')
        if current_page:
            current_page = int(current_page)
        else:
            current_page = 1
            
        if current_position_id:
            current_position_id = current_position_id
        else:
            # positions = position.get_position_by_device_id(devices[0].id)
            if positions:
                current_position_id = positions[0].id
            else:
                current_position_id = 0
        print "used position id:",current_position_id
        total_image_num = image.count_by_position_id(current_position_id)
        total_page_num = total_image_num/IMAGE_NUMBER_FOR_PAGE+1
        start_image_num = (current_page - 1)*IMAGE_NUMBER_FOR_PAGE + 1

        if total_page_num < current_page:
            current_page = total_page_num

        images = image.find_by('where `position_id`=? order by `created_at` desc limit ? offset ?',
                               current_position_id,
                               IMAGE_NUMBER_FOR_PAGE,
                               (current_page - 1)*IMAGE_NUMBER_FOR_PAGE)
        for img in images:
            img.created_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(img.created_at))
        # get the start and end page num
        if current_page > 3:
            start_page_num = current_page-3
        else:
            start_page_num = 1

        end_page_num = start_page_num+6
        if end_page_num>total_page_num:
            end_page_num = total_page_num
            start_page_num = end_page_num-6
            if start_page_num<1:
                start_page_num = 1

        end_image_num  = start_image_num+len(images)-1
        print "image num:",total_image_num

        return self.render('browser.html',
                           page_name='browser',
                           positions=positions,
                           current_position_id=current_position_id,
                           current_page=current_page,
                           total_page_num=total_page_num,
                           total_image_num=total_image_num,
                           start_image_num=start_image_num,
                           end_image_num=end_image_num,
                           start_page_num=start_page_num,
                           end_page_num=end_page_num,
                           user_name=usr.name,
                           images=images
                           )

