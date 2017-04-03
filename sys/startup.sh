#!/bin/sh
syslogd
su -c "pg_ctl start -D /data/db -l /data/db/pg_ctl.logfile" - postgres
crond
/bin/bash
