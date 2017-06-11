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
    alerts = json.loads(res)

    session = db.Session()

    # clear old alerts
    old_alerts = session.query(db.Alert).all()
    session.delete(old_alerts)

    # add new alerts
    for alert in alerts:
        row = db.Alert()
        row.from_dict(alert)
        session.add(row)

    session.commit()


if __name__ == '__main__':
    pull_alerts()

