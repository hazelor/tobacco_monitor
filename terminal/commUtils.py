__author__ = 'guoxiao'

import uuid, md5
import threading, time
import struct
import socket,struct, fcntl
import redis


def get_ip_address(ifname): 
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
    return socket.inet_ntoa(fcntl.ioctl( 
        s.fileno(), 
        0x8915,  # SIOCGIFADDR 
        struct.pack('256s', ifname[:15]) 
    )[20:24]) 

def get_mac_address():
    mac = uuid.UUID(int = uuid.getnode()).hex[-12:]
    return mac

def get_md5(raw_str):
    mdtool = md5.new()
    mdtool.update(raw_str)
    return mdtool.hexdigest()


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


class CountDownExec(CountDownTimer):
    """
    a timer that execute an action at the end of the timer run.
    """
    instance = {}

    @staticmethod
    def get_instance(key_name, seconds = 2, action = None, args=[]):
        if CountDownExec.instance.has_key(key_name):
            ins = CountDownExec.instance[key_name]
        else:
            CountDownExec.instance[key_name] = CountDownExec(seconds, action, args)
            ins = CountDownExec.instance[key_name]
        return ins

    def __init__(self, seconds, action, args=[]):
        self.args = args
        self.action = action
        self.seconds = seconds
        CountDownTimer.__init__(self, seconds)

    def run(self):
        CountDownTimer.run(self)
        self.action(self.args)
        # TProcess = CountDownExec(self.seconds, self.action, self.args)

        r=redis.Redis()
        duration = r.get('duration')
        if duration:
            duration = int(duration)
        else:
            duration = 10
        TProcess = CountDownExec(duration, self.action, self.args)
       
        TProcess.start()

    def set_duration(self, seconds):
        self.seconds = seconds
        self.runTime = seconds
        TProcess = CountDownExec(self.seconds, self.action, self.args)
        TProcess.start()


def bytes_to_int(buf, offset):
    return struct.unpack_from(">I", buf, offset)[0]


def bytes_to_float(buf, offset):
    return struct.unpack_from(">f", buf, offset)[0]

