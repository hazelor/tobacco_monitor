from base import base_handler
import time
import json
from model.data import Data_Table_Map, Data
from model.device_observered import Device_Observed
from model.position import Position_Data
import tornado
import tornado.web



class data_history_handler(base_handler):
    @tornado.web.authenticated
    def get(self):
        usr = self.get_current_user()
        device_observed = Device_Observed()
        devices = device_observed.observed_devices(usr.id)
        position = Position_Data()
        if not devices or len(devices) < 1:
            return self.render('no_devices.html', user_name=usr.name, page_name="browser")
        devs_info = {}
        for dev in devices:
            devs_info[dev.location] = position.get_position_by_device_id(dev.id)
        return self.render('history.html',
            page_name = 'history',
            devs_info = devs_info,
            user_name=usr.name)

class data_history_query_handler(base_handler):
    def get(self):
        pos_id = self.get_argument('pos_id','')
        type_id = self.get_argument('type_id','')
        start_time=self.get_argument('start_time')+':00'
        start_time = time.mktime(time.strptime(start_time, '%Y-%m-%d %H:%M:%S'))
        end_time=self.get_argument('end_time')+':00'
        end_time = time.mktime(time.strptime(end_time, '%Y-%m-%d %H:%M:%S'))
        tables = Data_Table_Map.get_tables(start_time, end_time)
        data_list = []
        for table in tables:
            data_list.extend(Data.find_by('where position_id = ? and type_id = ?', pos_id, type_id, sub_name = str(table.index)))
        self.write(json.dumps(data_list))

