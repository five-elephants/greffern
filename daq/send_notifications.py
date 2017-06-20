#!/usr/bin/env python
# coding=utf-8

import db_orm as db
import json
import urllib2
import yaml
import smtplib
from email.mime.text import MIMEText
from sqlalchemy import exists
#from check_alerts import notify

with open('/home/john/config.yml', 'r') as f:
    config = yaml.load(f)

api_url = config['api']['url'] + '/list-notifications'
token = config['api']['token']
smtp_server = '172.17.0.1'
sender_email = 'simonf256@googlemail.com'


def notify(dct):
    if dct['alert']['above_trigger']:
        above_trigger = u'Oberer Grenzwert:  {:.1f} °C\n'.format(
            float(dct['alert']['above_trigger']))
    else:
        above_trigger = u''

    if dct['alert']['below_trigger']:
        below_trigger = u'Unterer Grenzwert: {:.1f} °C\n'.format(
            float(dct['alert']['below_trigger']))
    else:
        below_trigger = u'' 

    msg = MIMEText(u"""
=== Alarm {} ausgelöst ===

Datum:             {}
Temperatur:        {:.1f} °C
{}{}
        """.format(dct['alert']['name'].encode('ascii', 'replace'),
                   dct['timestamp'].encode('ascii', 'replace'),
                   float(dct['temperature']['temperature']),
                   above_trigger.encode('ascii', 'replace'),
                   below_trigger.encode('ascii', 'replace')),
        _charset='utf-8')

    msg['Subject'] = 'Alarm {}'.format(dct['alert']['name'].encode('ascii', 'replace'))
    msg['From'] = sender_email
    msg['To'] = dct['alert']['notify_email']

    print msg.as_string()

    if dct['alert']['notify_email']:
        s = smtplib.SMTP(smtp_server)
        s.sendmail(sender_email, [dct['alert']['notify_email']], msg.as_string())
        s.quit()

        print "Sent mail to {}".format(dct['alert']['notify_email'])

def fetch_notifications(api_url, token):
    res = urllib2.urlopen('{}?token={}'.format(api_url, token)).read()
    notifications = json.loads(res)
    #print('new notifications: {}'.format(notifications))

    session = db.Session()

    for n in notifications:
        if not session.query(exists().where(db.Notification.id == int(n['id']))).scalar():
            print "adding {}".format(n)

            new = db.Notification()
            new.from_dict(n)
            session.add(new)

            notify(n)

            session.commit()


if __name__ == '__main__':
    fetch_notifications(api_url, token)
