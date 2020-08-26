#!/bin/bash
while true; do
	pid=$(ps ax | grep -i "fetchcord" | grep -v grep | awk '{print $1}')
	if [ ! -z "$pid" ]; then
		kill -15 $pid
	fi
	fetchcord --terminal=st --termfont="Joy Pixels" --time 120 &
	/opt/Discord/Discord &
	if [ $? -eq 0 ]; then
		exit
	fi
	sleep 25
done
