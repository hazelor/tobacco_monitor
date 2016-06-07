#!/usr/bin/env python
#--coding:utf-8--

__author__ = 'guoxiao'



ISOTIMEFORMAT = "%Y-%m-%d-%H-%M-%S"
AIR_HUMIDITY = "air_humidity" #空气湿度
AIR_TEMPERATURE = "air_temperature" #空气温度
SOIL_HUMIDITY = "soil_humidity" #土壤湿度
SOIL_TEMPERATURE = "soil_temperature" #土壤温度
MEASURED_CONCENTRATION = "measured_concentration" #测量浓度
TARGET_CONCENTRATION = "target_concentration" #目标浓度

MEASURED_CONCENTRATION_AVG_30M = "measured_concentration_avg_30m"
MEASURED_CONCENTRATION_AVG_20S = "measured_concentration_avg_20s"
CALIBRATE_CONCENTRATION = "calibrate_concentration"
OBJECT_DIFF = "object_diff"
ACTION_TIME = "action_time"
BACKUP1 = "backup1"
BACKUP2 = "backup2"

SERVER_URL = "localhost"
UPDATE_PORT = "8080"

DEV_TYPE = "dev_tobacco"

API_DATA_URL = "/api/data"
API_CTRL_URL = "/api/ctrl"
API_IMAGE_URL = "api/image"


SERIAL_PORT_NAME = '/dev/ttyUSB0'
SERIAL_PORT_BAUD = 9600
SERIAL_PORT_TIMEOUT = 0.5

RES_SUCCESS = 'ok'
RES_FAIL = 'fail'

CTRL_UPDATE_DURATION = 10

ADDRESS_RAINFALL = 404
ADDRESS_AI = 700

NUM_REGISTER_RAINFALL = 1
NUM_REGISTER_AI = 8 

FUNC_AI = 3
FUNC_RAINFALL = 3

SUB_ADDRESS_SIGN = 1

CONF_FILE_PATH = "device_infos.conf"
CAPTURED_DIR = "/home/sonic513/cam_survilliance_server/static/img/captured"
