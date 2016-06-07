
__author__ = 'guoxiao'

import Queue, threading


class RainfallDataPool:
    instance = None
    mutex = threading.Lock()

    def __init__(self, max_size):
        self.queue = []
        self.max_size = max_size

    @staticmethod
    def get_instance(max_size = 180):
        if RainfallDataPool.instance == None:
            RainfallDataPool.mutex.acquire()
            RainfallDataPool.instance = RainfallDataPool(max_size)
            RainfallDataPool.mutex.release()

        return RainfallDataPool.instance

    def push_data(self, data):
        RainfallDataPool.mutex.acquire()
        if len(self.queue) >= self.max_size:
            self.queue.pop()
        print "rainfall queue insert the data:",data
        self.queue.insert(0,data)
        print "rainfall queue insert the data after:",self.queue
        RainfallDataPool.mutex.release()

    def get_sum(self):
        print 'rainfall queue:',self.queue
        #RainfallDataPoll.mutex.acquire()
        res = sum(self.queue)
        print 'rainfall queue res:',res
        #RainfallDataPool.mutex.release()
        return res
        

class DataPool:
    instance = None
    mutex = threading.Lock()

    def __init__(self, max_size):
        self.queue = Queue.Queue(max_size)
        self.max_size = max_size
        self.g_counts_reboot = 0

    @staticmethod
    def get_instance(max_size = 20):
        if(DataPool.instance == None):
            DataPool.mutex.acquire()
            if(DataPool.instance == None):
                DataPool.instance = DataPool(max_size)
            DataPool.mutex.release()

        return DataPool.instance

    def push_data(self, data):
        DataPool.mutex.acquire()
        if len(self.queue.queue) >= self.max_size:
            self.queue.get(block = False)
        self.queue.put(data)
        DataPool.mutex.release()

    def pull_data(self):
        res = []
        DataPool.mutex.acquire()
        if(not self.queue.empty()):
            res = self.queue.get(block=False)
        DataPool.mutex.release()
        return res

    def get_len(self):
        DataPool.mutex.acquire()
        l = len(self.queue.queue)
        DataPool.mutex.release()
        return l
