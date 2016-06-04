__author__ = 'guoxiao'

import serial
import ctypes, binascii
from macros import SERIAL_PORT_NAME, SERIAL_PORT_BAUD, SERIAL_PORT_TIMEOUT
import confUtils
from queueUtils import DataPool
from commUtils import *
from confUtils import *
import gpio, time

dev_conf = get_dev_conf()

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


def intArrayToString(array):
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


def formCommand(addr, code, start_pos, num_pos):
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
    ser = args['serial']
    command = formCommand(1, 3, 0, 72)
    hexer = intArrayToString(command).decode("hex")
    ser.write(hexer)
    ans = ser.readall()
    construct_datas(ans)


def construct_datas(ans):
    start_pos = 3

    mac_md5 = get_md5(get_mac_address())
    date = time.time()


    for pos_content in dev_conf:
        c_res = {}
        c_res['mac_address'] = mac_md5
        c_res['date'] = date
        c_res['position'] = pos_content['position']
        c_res['data'] = {}
	try:
            for data_content in pos_content['contents']:
                c_res['data'][data_content['name']] = bytes_to_float(ans, data_content['start_pos']+start_pos)
            print 'tag:------------', c_res
            DataPool.get_instance().push_data(c_res)
	except:
	    pass
    #DataPool.get_instance().push_data(c_res)


if __name__ == '__main__':
    exe_collection_datas({'serial':init_serial_port()})
