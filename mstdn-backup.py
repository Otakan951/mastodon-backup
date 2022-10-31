#!/usr/bin/env python3
import datetime
import os
import tarfile
import configparser
import shutil
import requests
from distutils import dir_util

dt_now = datetime.datetime.now()
month = dt_now.strftime('%Y%m')
day = dt_now.strftime('%d')
date = day + dt_now.strftime('%d%H%M%S')

config_file = os.path.dirname(os.path.abspath(__file__)) + "/config.ini"
config = configparser.ConfigParser()
config.read(config_file, encoding='utf-8')

work_path = config['common']['work_path']
mstdn_path = config['common']['mstdn_path']
target_image1 = config['mstdn_media']['target_image1']
target_image2 = config['mstdn_media']['target_image2']
target_image3 = config['mstdn_media']['target_image3']
target_image4 = config['mstdn_media']['target_image4']
postgresql_container = config['postgreSQL_info']['postgresql_container']
db_user = config['postgreSQL_info']['db_user']
db_name = config['postgreSQL_info']['db_name']
access_token = config['common']['token']
mstdn_domain = config['common']['domain']
visibility = config['common']['visibility']

work_path = work_path + month + "/"
temp_path = work_path + 'temp/'
os.makedirs(temp_path, exist_ok=True)
db_file = temp_path + 'db_dump.sql'
redis_original = mstdn_path + 'redis/dump.rdb'
redis_file = temp_path + 'redis_dump.rdb'
media_path = mstdn_path + 'public/system'

cmd = 'docker exec -t ' + postgresql_container + ' pg_dump -Fp -U ' +  db_user + ' ' + db_name + ' > ' +  db_file
os.system(cmd)
db_size = os.path.getsize(db_file)
shutil.copy(redis_original, redis_file)
redis_size = os.path.getsize(redis_file)

db_archive = work_path  + date + '_db.tar.gz'
with tarfile.open(db_archive, 'w:gz') as t:
    t.add(db_file, arcname='dump.sql')
    t.add(redis_file, arcname='dump.rdb')
shutil.rmtree(temp_path)

if "01" == day:
    img_archive = work_path  + date + '_image.tar.gz'
    with tarfile.open(img_archive, 'w:gz') as t:
        t.add(media_path + target_image1, arcname=target_image1)
        t.add(media_path + target_image2, arcname=target_image2)
        t.add(media_path + target_image3, arcname=target_image3)
        t.add(media_path + target_image4, arcname=target_image4)
    img_size = os.path.getsize(img_archive)
else:
    img_size = -1

sentence = "DB:" + str(db_size) + "\nRedis:" + str(redis_size) + "\nImg:" + str(img_size)
headers = {'Authorization': 'Bearer {}'.format(access_token)}
url = "https://{}/api/v1/statuses".format(mstdn_domain)
json_info = {"status": sentence, "visibility": visibility}
requests.post(url, headers=headers, json=json_info)
