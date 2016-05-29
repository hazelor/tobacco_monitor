# coding=utf-8
import os,sys
import redis
import mysql.connector
from celery import Celery,platforms
import json,time
from util.dbtool import *
from util.commons import *
from util.confs import *
import collections

reload(sys)
sys.setdefaultencoding( "utf-8" )

celery = Celery("tasks", broker="amqp://")
celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'amqp')
celery.conf.CELERYD_MAX_TASKS_PER_CHILD = 10
# celery.conf.update(
#     CELERY_TASK_SERIALIZER='json',
#     CELERY_ACCEPT_CONTENT=['json'],
#     CELERY_RESULT_SERIALIZER ='json',
# )
platforms.C_FORCE_ROOT = True

@celery.task(name='handler.tasks.db_save')
def db_save(jdatas):
    r=redis.Redis()
    data_dict={'air_temperature':[],'air_humidity':[],'soil_temperature':[],'soil_humidity':[],'measured_concentration':[],'target_concentration':[], 'measured_concentration_avg_30m':[],'measured_concentration_avg_20s':[],'calibrate_concentration':[]}
    if len(jdatas) != 0:
        for jdata in jdatas:
            mac_address=jdata['mac_address']
            date=jdata['date']
            position=jdata['position']
            for k,v in jdata['data'].iteritems():
                data_dict[k].append((mac_address, position, v, date))
                r.hmset(mac_address+','+str(position)+','+k, {'date':date, 'value':v})
    with database_resource() as cursor:
        cursor.executemany('insert into air_temperature (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['air_temperature'])
        cursor.executemany('insert into air_humidity (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['air_humidity'])
        cursor.executemany('insert into soil_temperature (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['soil_temperature'])
        cursor.executemany('insert into soil_humidity (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['soil_humidity'])
        cursor.executemany('insert into measured_concentration (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['measured_concentration'])
        cursor.executemany('insert into target_concentration (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['target_concentration'])
        cursor.executemany('insert into measured_concentration_avg_30m (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['measured_concentration_avg_30m'])
        cursor.executemany('insert into measured_concentration_avg_20s (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['measured_concentration_avg_20s'])
        cursor.executemany('insert into calibrate_concentration (mac_address, position, value, date) values (%s, %s, %s, %s)', data_dict['calibrate_concentration'])
    return 'Y'

@celery.task(name='handler.tasks.db_query')
def db_query(mac_address, position, type, start_time, end_time):
    if type=='':
        data=[]
        with database_resource() as cursor:
            sql = "select date,value from %s where mac_address='%s' and position=%s and date BETWEEN %s and %s" % ('measured_concentration_avg_20s', mac_address, position, start_time, end_time)
            cursor.execute(sql)
            measured_concentration_data=cursor.fetchall()
            sql = "select date,value from %s where mac_address='%s' and position=%s and date BETWEEN %s and %s" % ('target_concentration', mac_address, position, start_time, end_time)
            cursor.execute(sql)
            target_concentration_data=cursor.fetchall()
        # if target_concentration_data and measured_concentration_data:
        #     data.append(measured_concentration_data)
        #     data.append(target_concentration_data)
        #     return data
        if measured_concentration_data:
            data.append(measured_concentration_data)
        else:
            data.append('')
        if target_concentration_data:
            data.append(target_concentration_data)
        else:
            data.append('')
        return data
        

    else:
        sql = "select date,value from %s where mac_address='%s' and position=%s and date BETWEEN %s and %s" % (type, mac_address, position, start_time, end_time)
        with database_resource() as cursor:
            cursor.execute(sql)
            data = cursor.fetchall()
        if data:
            #data = json.dumps(data)
            return data
        # return sql


@celery.task(name='handler.tasks.redis_query')
def redis_query(mac_address, postion):
    type_list=[{'air_temperature':'空气温度'},{'air_humidity':'空气湿度'},{'soil_temperature':'土壤温度'},{'soil_humidity':'土壤湿度'},{'measured_concentration':'测量浓度'},{'target_concentration':'目标浓度'},{'measured_concentration_avg_30m':'测量浓度30min均值'},{'measured_concentration_avg_20s':'测量浓度20s均值'},{'calibrate_concentration':'传感器校准值'}]
    data=[[],[[],[]]]
    r=redis.Redis()
    # mac_address = get_md5(mac_address)
    data[1][0].append(r.hget(mac_address+','+postion+','+'measured_concentration_avg_20s', 'date'))
    data[1][0].append(r.hget(mac_address+','+postion+','+'measured_concentration_avg_20s', 'value'))
    data[1][1].append(r.hget(mac_address+','+postion+','+'target_concentration', 'date'))
    data[1][1].append(r.hget(mac_address+','+postion+','+'target_concentration', 'value'))
    # data = json.dumps(data)
    for item in type_list:
        for k,v in item.items():
            value = r.hget(mac_address+','+postion+','+k, 'value')
            if value:
                data[0].append(v)
                data[0].append(value)
    return data

@celery.task(name='handler.tasks.data_zip')
def data_zip(mac_address_list, start_time, end_time):
    chamber_file_list = []
    for mac_address in mac_address_list:
        # device_list=[]
        with database_resource() as cursor:
            sql="select mac_address_position,name,member from air_chamber WHERE mac_address='%s' "%(mac_address)
            cursor.execute(sql)
            device_list=cursor.fetchall()
        for device in device_list:
            position = (device[0]).split(',')[1]
            file_dir = os.path.join(getPWDDir(),DOWNLOAD_DIR)
            index=1
            file_list=[]
            chamber_file_path=os.path.join(file_dir,device[1]+'.csv')
            chamber_file_list.append(chamber_file_path)
            members = (device[2]).split('_')
            for item in members:
                data=db_query(mac_address, position, short_name_to_english_name[item], start_time, end_time)
                file_path = os.path.join(file_dir,device[1]+'_%d.csv' % (index))
                file_list.append(file_path)
                f= open(file_path,'w+')
                index += 1
                if data:
                    line_list = []
                    line_list.append("%s,%s,\n" %(short_name_to_english_name[item], "date time"))
                    for d in data:
                        line_list.append("%f,%s,\n" %(d[1], time.strftime("%Y-%m-%d %X", time.localtime(d[0]))))
                    f.writelines(line_list)
    # for k, v in g_chamber_conf.items():
    #     mac_address = get_md5(k.strip().split(',')[0])
    #     position = int(k.split(',')[1])
    #     chamber_name = v['name']
    #     file_dir = os.path.join(getPWDDir(),DOWNLOAD_DIR)
    #     index = 1
    #     file_list = []
    #     chamber_file_path = os.path.join(file_dir,chamber_name+'.csv')
    #     chamber_file_list.append(chamber_file_path)
    #
    #     for type, name in v['data_contents'].items():
    #         data = db_query(mac_address, position, type, start_time, end_time)
    #         file_path = os.path.join(file_dir,chamber_name+'_%d.csv' % (index))
    #         # print file_path
    #         file_list.append(file_path)
    #         f= open(file_path,'w+')
    #         index += 1
    #         if data:
    #             line_list = []
    #             line_list.append("%s,%s,\n" %(name, "date time"))
    #             for d in data:
    #                 line_list.append("%f,%s,\n" % (d[1],time.asctime(time.localtime(d[0]))))
    #             f.writelines(line_list)

        #merge the files
            cmd = "paste"
            for p in file_list:
                cmd = cmd +" " + p
            cmd = cmd +'|cat > ' + chamber_file_path
            # print cmd
            os.system(cmd)
            cmd = "rm "
            rm_files_path = os.path.join(file_dir, device[1] +'_')
            cmd = cmd + rm_files_path + "*"
            os.system(cmd)
    local_time = time.localtime(time.time())
    zip_file_name = "data_%d_%d_%d_%d_%d_%d.zip" %(local_time.tm_year, local_time.tm_mon, local_time.tm_mday, local_time.tm_hour, local_time.tm_min, local_time.tm_sec)
    zip_file_path = os.path.join(file_dir, zip_file_name)
    zip_files_name = DOWNLOAD_DIR +'/*.csv'
    cmd = "zip %s %s" %(zip_file_path, zip_files_name)
    os.system(cmd)
    cmd = "rm %s" %(zip_files_name)
    os.system(cmd)
    return zip_file_name


@celery.task(name='handler.tasks.data_zip_by_category')
def data_zip_by_category(mac_address_list, start_time, end_time):
    category_file_list = []
    file_dir = os.path.join(getPWDDir(),DOWNLOAD_DIR)
    for k,category_name in short_name_to_english_name.items():
        # category_file_path=os.path.join(file_dir,category_name+'.csv')
        # category_file_list.append(category_file_path)
        # datas_dict=collections.OrderedDict()
        for mac_address in mac_address_list:
	    # datas_dict=collections.OrderedDict()
	    index=1
	    file_list=[]
            with database_resource() as cursor:
                sql="select location from device WHERE mac_address='%s' "%(mac_address)
                cursor.execute(sql)
                mac_address_name=cursor.fetchone()
		category_file_path=os.path.join(file_dir,mac_address_name[0]+category_name+'.csv')
		category_file_list.append(category_file_path)
                sql="select position from %s_%s WHERE mac_address='%s' "%(category_name, 'member', mac_address)
                cursor.execute(sql)
                positions = cursor.fetchall()
            # datas_dict={}
            for position in positions:
		file_path=os.path.join(file_dir,mac_address_name[0]+category_name+'-%d.csv'%(index))
		file_list.append(file_path)
		index+=1
                mac_address_position = ','.join([mac_address,position[0]])
                with database_resource() as cursor:
                    sql="select name from air_chamber WHERE mac_address_position='%s' "%(mac_address_position)
                    cursor.execute(sql)
                    name=cursor.fetchone()
                    sql="select date,value from %s WHERE mac_address='%s' and position='%s' and date BETWEEN %s AND %s "%(category_name, mac_address, position[0], start_time, end_time)
                    cursor.execute(sql)
                    datas=cursor.fetchall()
                    # datas_dict[name]=data
            	f= open(file_path,'w+')
            	# for k,v in datas_dict.items():
		if datas:
                    line_list=[]
                    line_list.append("%s,%s,\n" %("date time", name[0]))
                    for data in datas:
                        line_list.append("%s,%f,\n" %(time.strftime("%Y-%m-%d %X", time.localtime(data[0])), data[1]))
                    f.writelines(line_list)
            	f.flush()
            	f.close()
	    # merge file
	    cmd='paste'
	    for p in file_list:
	        cmd=cmd+' '+p
	    cmd=cmd+'|cat > '+category_file_path
	    os.system(cmd)
	    cmd='rm '
	    rm_file_path=os.path.join(file_dir,mac_address_name[0]+category_name+'-')
	    cmd=cmd+rm_file_path+'*'
	    os.system(cmd)
    local_time = time.localtime(time.time())
    zip_file_name = "data_%d_%d_%d_%d_%d_%d.zip" %(local_time.tm_year, local_time.tm_mon, local_time.tm_mday, local_time.tm_hour, local_time.tm_min, local_time.tm_sec)
    zip_file_path = os.path.join(file_dir, zip_file_name)
    zip_files_name = DOWNLOAD_DIR +'/*.csv'
    cmd = "zip %s %s" %(zip_file_path, zip_files_name)
    os.system(cmd)
    cmd = "rm %s" %(zip_files_name)
    os.system(cmd)
    return zip_file_name



@celery.task(name='handler.tasks.user_check')
def user_check(username, password):
    sql = "select * from user where username='%s' and password='%s' " % (username, password)
    with database_resource() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
    if data:
        return data


@celery.task(name='handler.tasks.device_query')
def device_query(username):
    sql = "select mac_address from device where username='%s' " % (username)
    with database_resource() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
    if data:
        return data

@celery.task(name='handler.tasks.db_query_basic')
def db_query_basic(sql):
    with database_resource() as cursor:
        cursor.execute(sql)
        data = cursor.fetchall()
    if data:
        return data


# @celery.task(name='handler.tasks.interval_redis_save')
# def interval_redis_save(mac_address, interval):
#     r=redis.Redis()
#     r.hmset(mac_address, {'interval':interval})
#     return 'Y'

@celery.task(name='handler.tasks.interval_redis_query')
def interval_redis_query(mac_address):
    r=redis.Redis()
    data = r.hget(mac_address, 'interval')
    if data:
        return data
    else:
        return ''



if __name__ == "__main__":
    celery.start()
