
PASSWORD_SALT = '!QAZ@WSXcde3)Okm9i'

CAPTURED_DIR = "static/img/captured/"

THUMBNAIL_DIR = "static/img/thumbnail/"

CONF_DIR ="conf/"

DATA_INFO_FILENAME = "device_infos.conf"

CHART_INFO_FILENAME = "chart_tobacco_dev.conf"

#about img page
IMAGE_NUMBER_FOR_PAGE = 16

THUMBNAIL_SIZE = 150

MAX_TABLE_LINES = 80000

RAINFALL_PRE_SHOT = 0.2 #0.2mm

DEV_ERROR_COUNT = 10
DEV_ERROR_DURATION = 60 
DEV_STATUS_GOOD = 0
DEV_STATUS_INACTIVE = 1
DEV_STATUS_WARNING = 2
DEV_STATUS_ERROR = 3

PERMISSION_ADMIN = 1
PERMISSION_USER = 0
PERMISSION_ITEMS = [
		{'name': 'admin', 'value': PERMISSION_ADMIN}, 
		{'name':'user', 'value': PERMISSION_USER}]

TIME_HOUR_FORMAT = "%b %d %Y %H"
