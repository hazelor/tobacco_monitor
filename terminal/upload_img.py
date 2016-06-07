#coding=utf-8
import time
import sys
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
from macros import *
import os


def img_upload(device_mac, device_pos,created_at, file_name):
    if device_mac == "":
        return False

    if device_pos == "":
        return False

    upload_path = CAPTURED_DIR
    file_path = os.path.join(upload_path, file_name)
    #try:
    datagen, headers = multipart_encode({"mac":device_mac,"pos":device_pos,"date":created_at,"file": open(file_path, "rb")})
    url = "http://%s:%s/%s"%(SERVER_URL, UPDATE_PORT, API_IMAGE_URL)
    
    request = urllib2.Request(url, datagen, headers)
    res = urllib2.urlopen(request, timeout = 5000).read()
    print res
    if res == "ok":
        return True
    else:
        return False
    #except:
    #    return False
    

if __name__ == "__main__":
    register_openers()
    
    img_upload("001d72946153", 1, time.time(), sys.argv[1])

    
