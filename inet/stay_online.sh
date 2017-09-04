#!/bin/sh

if ! ping -w 60 -c 10 8.8.8.8 ; then
	echo "Not online"
else
	echo "Online"
fi


