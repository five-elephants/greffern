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
    print('new alerts: {}'.format(alerts))

    session = db.Session()

    # update or add new alerts
    for alert in alerts:
        row = session.query(db.Alert).filter(db.Alert.id == alert['id']).one_or_none()
        if not row is None:
            row.from_dict(alert)
        else:
            row = db.Alert() 
            row.from_dict(alert)
            session.add(row)

    # delete old ones
    obsolete = session.query(db.Alert)\
        .filter(~db.Alert.id.in_([ alert['id'] for alert in alerts ]))
    for obs in obsolete:
        session.delete(obs)

    new_alerts = session.query(db.Alert)
    for alert in new_alerts:
        print(alert)

    session.commit()


if __name__ == '__main__':
    pull_alerts()

