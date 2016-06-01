# coding=utf-8
from base import base_handler

class setting_handler(base_handler):
    @tornado.web.authenticated
    def get(self):
        if not is_admin():
            self.redirect('/logout')

