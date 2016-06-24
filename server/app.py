#coding=utf-8
import tornado.ioloop
import tornado.web
import routes
import tornado.options
from tornado.options import define, options
from model.device import DeivceStatusChecker
tornado.options.parse_command_line()
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

define('www_domain', default='127.0.0.1', type = str, help='env domain')
define('port', default=8080, type = int, help='app listen port')
define('debug', default=True, type = bool, help='is debuging?')


def create_app():
    settings = {
        'login_url': '/login',
        'static_path': 'static',
        'template_path': 'template',
        'cookie_secret': '16oETzKXQAGaYdkL6gEmGeJJFuYh7EQnp2XdTP1o/Vo=',
        'xsrf_cookies': False,
        'debug': options.debug,
        #'autoescape': None,
    }
    return tornado.web.Application(routes.handlers, **settings)


def connect_db():
    import transwarp.db as dbutil
    dbutil.create_engine('sonic513', 'sonic513', 'tobacco_monitor', port=3306)

if __name__ == "__main__":
    app = create_app()
    connect_db()
    app.listen(options.port)
    DeivceStatusChecker.get_instance().start()
    tornado.ioloop.IOLoop.instance().start()
