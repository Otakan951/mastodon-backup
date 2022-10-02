#!/usr/bin/env python3
import datetime
import os
import tarfile
import configparser
from distutils import dir_util

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')

work_dir = config['common']['work_dir']
media_path = config['mstdn_media']['media_path']
target_image1 = config['mstdn_media']['target_image1']
target_image2 = config['mstdn_media']['target_image2']
target_image3 = config['mstdn_media']['target_image3']
target_image4 = config['mstdn_media']['target_image4']

postgresql_container = config['postgreSQL_info']['postgresql_container']
db_user = config['postgreSQL_info']['db_user']
db_name = config['postgreSQL_info']['db_name']

dt_now = datetime.datetime.now()
date = dt_now.strftime('%Y%m%d%H%M%S')

temp_dir = work_dir + 'temp/'
os.makedirs(work_dir, exist_ok=True)

db_file = temp_dir + 'dump.sql'
cmd = 'docker exec -t ' + postgresql_container + ' pg_dump -Fp -U ' +  db_user + ' ' + db_name + ' > ' +  db_file
os.system(cmd)

img_file = work_dir  + date + '.tar.gz'
with tarfile.open(img_file, 'w:gz') as t:
    t.add(media_path + target_image1, arcname=target_image1)
    t.add(media_path + target_image2, arcname=target_image2)
    t.add(media_path + target_image3, arcname=target_image3)
    t.add(media_path + target_image4, arcname=target_image4)
    t.add(db_file, arcname='dump.sql')


