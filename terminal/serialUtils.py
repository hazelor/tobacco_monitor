__author__ = 'guoxiao'

import serial
import ctypes, binascii
from macros import SERIAL_PORT_NAME, SERIAL_PORT_BAUD, SERIAL_PORT_TIMEOUT
from macros import ADDRESS_RAINFALL, ADDRESS_AI, NUM_REGISTER_RAINFALL, NUM_REGISTER_AI, FUNC_RAINFALL, FUNC_AI
from macros import SUB_ADDRESS_SIGN

from queueUtils import DataPool, RainfallDataPool
from commUtils import *

import gpio, time
import random

def init_serial_port():
    ser = serial.Serial(SERIAL_PORT_NAME, SERIAL_PORT_BAUD, timeout=SERIAL_PORT_TIMEOUT)
    return ser


def open_serial_port(ser):
    if not ser.isOpen():
        ser.open()
    return ser


def close_serial_port(ser):
    if ser.isOpen():
        ser.close()
    return ser


def intToHexString(data):
    s= hex(data)
    if len(s[2::])%2==1:
        s ="0" +s[2::]
        return s
    return s[2::]


def int_array_to_string(array):
    if len(array) == 0:
        return ""
    s=""
    if not isinstance(array[0], int):
        return
    for item in array:
        s+=intToHexString(item)
    return s


def CRC16(data):
    CRC16Lo = 0xff;
    CRC16Hi = 0xFF;
    CL = 0x01 ;
    CH = 0xA0 ;
    for i in range(len(data)):
        CRC16Lo ^= data[i]
        for Flag in range(8):
            SaveHi = CRC16Hi
            SaveLo = CRC16Lo
            CRC16Hi >>= 1
            CRC16Lo >>= 1
            if (SaveHi & 0x01) == 0x01:
                CRC16Lo  |=0x80
            if (SaveLo & 0x01) == 0x01:
                CRC16Hi  ^= CH
                CRC16Lo  ^= CL
    return (CRC16Hi<<8)|CRC16Lo


def form_command(addr, code, start_pos, num_pos):
    data=[]
    data.append(addr)
    data.append(code)
    data.append(start_pos/256)
    data.append(start_pos%256)
    data.append(num_pos/256)
    data.append(num_pos%256)
    crc =CRC16(data)
    data.append(crc%256)
    data.append(crc/256)
    return data


def exe_collection_datas(args):
    try:
        ser = args['serial']
        rainfall_command = form_command(SUB_ADDRESS_SIGN, FUNC_RAINFALL, ADDRESS_RAINFALL, NUM_REGISTER_RAINFALL)
        hexer = int_array_to_string(rainfall_command).decode("hex")
        #ser.write(hexer)
        #ans = ser.readall()
        #rainfall_value = construct_rainfall_datas(ans)
        rainfall_value=[random.random()]
        AI_command = form_command(SUB_ADDRESS_SIGN, FUNC_AI, ADDRESS_AI, NUM_REGISTER_AI)
        hexer = int_array_to_string(AI_command).decode('hex')
        #ser.write(hexer)
        #ans = ser.readall()
        #ai_value = construct_ai_datas(ans)
        ai_value = [random.random() for i in range(7)]
        #print "ai value:",ai_value
    
        res = {}
        res['mac'] = get_mac_address()
        res['data_content'] = {}
        res['data_content']['date'] = time.time()
        ai_value.extend(rainfall_value)
        res['data_content']['content'] = ai_value
        print res
        DataPool.get_instance().push_data(res)
    except:
        pass
    
    

def construct_rainfall_datas(ans):
    start_pos = 3
    try:
        res = bytes_to_short(ans, start_pos)
        return [res]
        #RainfallDataPool.get_instance().push_data(res)
        #return [RainfallDataPool.get_instance().get_sum()]
    except:
        pass

def construct_ai_datas(ans):
    g_data_conf = load_data_conf()
    start_pos = 3
    res = []
    try:
        for data_info in g_data_conf:
            d = bytes_to_short(ans, data_info['start_pos']*2+start_pos)
            print d
            d = float(d)
            d = (d-data_info['min_origin'])/(data_info['max_origin']-data_info['min_origin'])*(data_info['max_value']-data_info['min_value'])+data_info['min_value']
            res.append(d)
        return res
    except:
        pass


if __name__ == '__main__':
    exe_collection_datas({'serial':init_serial_port()})
