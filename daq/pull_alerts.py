#!/usr/bin/env python

import db_orm as db
import json
import urllib2
import yaml

with open('/home/john/config.yml', 'r') as f:
    config = yaml.load(f)

api_url = config['api']['url'] + '/list-alerts'
token = config['api']['token']


def pull_alerts():
    res = urllib2.urlopen('{}?token={}'.format(api_url, token)).read()
    print(json.loads(res))


if __name__ == '__main__':
    pull_alerts()

