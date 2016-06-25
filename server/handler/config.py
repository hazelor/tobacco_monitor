from base import base_handler
import tornado, tornado.web
from model.data import DataParser
import json

class data_conf_handler(base_handler):
    def get(self):
        self.write(json.dumps(DataParser.get_instance().get_chart_info()))
        self.finish()