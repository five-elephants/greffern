#!/usr/bin/env python

from acquire import read_sensors
import datetime
import urllib2
import yaml

with open('/home/john/config.yml', 'r') as f:
    config = yaml.load(f)

api_url = config['api']['url']
token = config['api']['token']

def publish(temps):
    now = datetime.datetime.now()

    for uid,raw_temp in temps.items():
        value = float(raw_temp) / 1000.0
        timestamp = now.strftime('%Y-%m-%d-%H-%M-%S')

        res = urllib2.urlopen('{}?token={}&timestamp={}&uid={}&value={}'.format(
            api_url, token, timestamp, uid, value)).read()

        if res != 'OK':
            print('This did not work: {}'.format(res))

if __name__ == '__main__':
    temps = read_sensors()
    print(temps)
    publish(temps)	
