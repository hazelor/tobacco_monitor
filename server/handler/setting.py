# coding=utf-8
from base import base_handler
import tornado, tornado.web

class setting_handler(base_handler):
    @tornado.web.authenticated
    def get(self):
        if not self.is_admin():
            self.redirect('/logout')

