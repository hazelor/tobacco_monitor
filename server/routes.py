__author__ = 'sonic-server'

from handler import *
handlers = [
    (r'/', home_handler),
    (r'/preview',preview_handler),
    (r'/preview/realtime', preview_realtime_handler),
    (r'/download',download_handler),
    (r'/history',history_handler),
    (r'/history/query', history_query_handler),
    (r'/setting',setting_handler),
    (r'/setting/setting/(\w+)',setting_handler),
    (r"/setting/(\w+)",setting_handler),
    (r'/api/dataChannel', data_handler),
    (r'/api/ctrl', ctrl_handler),
    (r'/login', login_handler),
    (r'/logout', logout_handler)
]

modules = {'basic': setting_basicModule,
}
