__auther__= "guo xiao"

from marcos import *
from hashlib import sha1
import os
import md5
import threading, time

def get_pwd_dir():
    return os.getcwd()

def get_md5(raw_str):
    mdtool = md5.new()
    mdtool.update(raw_str)
    return mdtool.hexdigest()


def hash_password(password):
    return sha1('{password}{salt}'.format(
        password = sha1(password).hexdigest(),
        salt = PASSWORD_SALT)).hexdigest()

def check_user_exists(func):
    import model
    def wrapper(self, user_id):
        u= model.user.User().find_first("id = ?",user_id)
        if not u:
            self.redirect("/login")
        self.user = u
        return func(self, user_id)


class Timer(threading.Thread):
    """
    very simple but useless timer.
    """
    def __init__(self, seconds):
        self.runTime = seconds
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(self.runTime)

class CountDownTimer(Timer):
    """
    a timer that can counts down the seconds.
    """
    def run(self):
        counter = self.runTime
        for sec in range(self.runTime):
            #print counter
            time.sleep(1.0)
            counter -= 1