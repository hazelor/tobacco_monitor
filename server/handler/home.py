__author__ = 'sonic-server'

from base import base_handler

class home_handler(base_handler):
    def get(self, *args, **kwargs):
        self.redirect("/preview")