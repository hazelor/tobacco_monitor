__author__ = 'sonic-server'

from handler import *
handlers = [
    (r'/', home_handler),
    (r'/data/preview',data_preview_handler),
    (r'/img/preview',img_preview_handler),
    (r'/data/preview/realtime', data_preview_realtime_handler),
    (r'/data/history',data_history_handler),
    (r'/data/history/query', data_history_query_handler),
    (r'/api/data', api_data_handler),
    (r'/login', login_handler),
    (r'/logout', logout_handler),
    (r'/setting', setting_handler),
    (r"/setting/(\w+)",setting_handler),
]

modules = {}
