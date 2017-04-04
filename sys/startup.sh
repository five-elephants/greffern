#!/bin/sh

# logging
syslogd

# start postgresql database
touch /var/log/postgres
chown postgres:postgres /var/log/postgres
su -c "pg_ctl start -D /data/db -l /var/log/postgres" - postgres

# cron for data acquisition
crond

# start web interface
export FLASK_APP=/home/john/app.py
flask run --host=0.0.0.0
