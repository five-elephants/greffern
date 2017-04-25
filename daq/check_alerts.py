#!/usr/bin/env python
# coding=utf-8

import db_orm as db
import smtplib
from email.mime.text import MIMEText

smtp_server = '172.17.0.1'
sender_email = 'simonf256@googlemail.com'

def get_temperature(sensor):
    if sensor.temperatures:
        data = sensor.temperatures[-1]
        return data.temperature, data.timestamp
    else:
        return None,None

def notify(alert, temp, timestamp, trigger, level):
    print "Notify on alert '{}': {} {} {}".format(
        alert.name,
        temp,
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
                   temp,
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
                   

def check_alerts():
    triggered = False
    session = db.Session()

    for sensor in session.query(db.Sensor):
        temp,timestamp = get_temperature(sensor)
        if temp is None: continue

        for alert in sensor.alerts:
            if alert.below_trigger and temp < alert.below_trigger:
                notify(alert, temp, timestamp, 'below', alert.below_trigger)
                triggered = True

            if alert.above_trigger and temp > alert.above_trigger:
                notify(alert, temp, timestamp, 'above', alert.above_trigger)
                triggered = True

    return triggered


if __name__ == '__main__':
    check_alerts()
