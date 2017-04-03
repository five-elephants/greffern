#!/usr/bin/env python3

import db
import os
import re
import datetime

sensor_regex = re.compile(r'.*t=(\d+)')

def read_sensors():
    path = '/sys/bus/w1/devices/'

    res = {}
    for subdir,dirs,files in os.walk(path):
        #print('subdir = {}'.format(subdir))

        device_dirs = [ i for i in dirs if i.startswith('10-') ]
        for device_dir in device_dirs:
            #print('device_dir: {}'.format(device_dir))

            with open('{}{}/w1_slave'.format(subdir, device_dir), 'r') as f:
                f.readline()
                txt = f.readline()

                m = sensor_regex.match(txt) 
                if m:
                    temp = int(m.groups(1)[0])
                    res[device_dir] = temp
                    #print('temperature = {}'.format(temp))

                #print('{}'.format(txt))

    return res

def update_db(temps):
    now = datetime.datetime.now()
    inserts = [ {
            'timestamp': now,
            'sensor_id': k,
            'temperature': float(v)
        } for k,v in temps.items() ]

    db.con.execute(db.temperatures.insert(), inserts)

if __name__ == '__main__':
    temps = read_sensors()
    print(temps)
    update_db(temps)
