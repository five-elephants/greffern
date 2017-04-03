#!/bin/bash

tempread=`cat /sys/bus/w1/devices/10-0008030d05fb/w1_slave`
temp=`echo "scale=2; "\`echo ${tempread##*=}\`" /1000" | bc`

echo $temp
