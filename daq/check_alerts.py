#!/usr/bin/env python
# coding=utf-8

import db_orm as db
import smtplib
from email.mime.text import MIMEText
from functools import partial

smtp_server = '172.17.0.1'
sender_email = 'simonf256@googlemail.com'

def notify(alert, temp, timestamp, trigger, level):
    print "Notify on alert '{}': {} {} {}".format(
        alert.name,
        temp.temperature,
        trigger,
        level)

    if alert.notify_email:
        if trigger == 'above':
            direction_txt = 'überschritten'
        elif trigger == 'below':
            direction_txt = 'unterschritten'

        msg = MIMEText("""
=== Alarm {} ausgelöst ===

Datum:      {}
Temperatur: {:.1f} °C
Grenzwert:  {:.1f} °C

Der Grenzwert {:.1f} °C für den Alarm {} wurde {}.
        """.format(alert.name,
                   timestamp.strftime('%Y-%m-%d  %H:%M'),
                   temp.temperature,
                   level,
                   level,
                   alert.name,
                   direction_txt))
        msg['Subject'] = 'Alarm {}'.format(alert.name)
        msg['From'] = sender_email
        msg['To'] = alert.notify_email

        s = smtplib.SMTP(smtp_server)
        s.sendmail(sender_email, [alert.notify_email], msg.as_string())
        s.quit()

        print "Sent mail to {}".format(alert.notify_email)

    session = db.Session()
    notice = db.Notification(alert_id=alert.id, temperature_id=temp.id)
    session.add(notice)
    session.commit()
                   
def find_crossings(alert):
    def test(cur, prev, f):
        #print "f({}) = {} and not f({} = {}".format(
        #    cur, f(cur), prev, f(prev))
        return f(cur) and not f(prev)

    if alert.below_trigger:
        test_below = partial(test, f=lambda x: x.temperature < alert.below_trigger)
    else:
        test_below = lambda _: False

    if alert.above_trigger:
        test_above = partial(test, f=lambda x: x.temperature > alert.above_trigger)
    else:
        test_above = lambda _: False

        
    cross_below = []
    cross_above = []
    last_temp = None

    session = db.Session()
    q = session.query(db.Temperature).\
        filter(db.Temperature.sensor_id == alert.sensor.id).\
        order_by(db.Temperature.timestamp)
    if alert.notifications:
        q = q.filter(db.Temperature.timestamp > alert.notifications[-1].timestamp)

    for temp in q:
        if not last_temp is None:
            #print "Testing {}, {}".format(last_temp, temp)
            if test_below(temp, last_temp):
                cross_below.append(temp)
            if test_above(temp, last_temp):
                cross_above.append(temp)

        last_temp = temp

    return cross_below, cross_above

def check_alerts():
    triggered = False
    session = db.Session()

    for sensor in session.query(db.Sensor):
        for alert in sensor.alerts:
            cross_below,cross_above = find_crossings(alert)

            print "below: ", cross_below
            print "above: ", cross_above

            if cross_below:
                notify(alert,
                       cross_below[-1],
                       cross_below[-1].timestamp,
                       'below',
                       alert.below_trigger)
                triggered = True

            if cross_above:
                notify(alert,
                       cross_above[-1],
                       cross_above[-1].timestamp,
                       'above',
                       alert.above_trigger)
                triggered = True


    return triggered


if __name__ == '__main__':
    check_alerts()
