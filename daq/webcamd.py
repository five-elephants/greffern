#!/usr/bin/env python

import daemon
import daemon.pidlockfile

from webcam import webcam

with daemon.DaemonContext(pidfile=daemon.pidlockfile.PIDLockFile('/var/run/webcamd.pid')):
	webcam()
