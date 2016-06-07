# coding=utf-8
from base import base_handler
from model.device_observed import Device_Observed
from model.position import Position_Image
from model.image import Image
from model.data import DataParser
import tornado
import redis

#tcelery.setup_nonblocking_producer()


class about_handler(base_handler):
    def get(self):
        return self.render('about.html',
                           page_name='about')


class home_handler(base_handler):
    @tornado.web.authenticated
    def get(self):
        user = self.get_current_user()
        dev_observed = Device_Observed()
        device_counts = dev_observed.count_user_devices(user.id)
        res_image = self.get_image_summary_info(user)
        res_data = self.get_data_summary_info(user)
        self.on_get_summery_info(res_image, res_data)


    def get_image_summary_info(self, user):
        dev_observed = Device_Observed()
        res = {'user_name':user.name,'device_counts': dev_observed.count_user_devices(user.id), 'device_info': []}
        devices = dev_observed.observed_devices(user.id)
        print devices
        pos = Position_Image()
        for dev in devices:
            contents_dev = {}
            print dev
            contents_dev['location'] = dev.location
            contents_dev['position_contents'] = []
            positions = pos.get_position_by_device_id(dev.id)
            if positions:
                for pos in positions:
                    img = Image()
                    image_count = img.count_by('where position_id = ?', pos.id)
                    contents_dev['position_contents'].append({'position': pos.position,
                                                              'duration': pos.duration,
                                                              'image_count': image_count,
                                                              'object_name': pos.object_name})
            res['device_info'].append(contents_dev)

        return res

    def get_data_summary_info(self, user):
        dev_observed = Device_Observed()
        devices = dev_observed.observed_devices(user.id)
        r  = redis.Redis()
        reses = []
        for dev in devices:
            data_content = r.get("col_datas_%s" %(dev.mac))
            data_content = eval(data_content)
            print "data_content:",type(data_content)
            if data_content:
                res = DataParser.get_instance().parse_to_json(dev.dev_type, data_content['content'], data_content['date'])
                res['location'] = dev.location
                reses.append(res)
        return reses

    def on_get_summery_info(self, res_image, res_data):
        user_name = res_image['user_name']
        device_counts = res_image['device_counts']
        device_info = res_image['device_info']

        return self.render('home.html',
                           user_name=user_name,
                           device_counts=device_counts,
                           device_image_info=device_info,
                           device_data_info = res_data,
                           page_name='home')
