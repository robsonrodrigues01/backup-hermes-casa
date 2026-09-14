#!/bin/bash
LOG=/home/hermes/tools/ghost-turbo.log
> "$LOG"
for i in $(seq 1 3600); do
  ps -eo pid=,ppid=,lstart=,args= | grep -E "dashboard --host|gateway run --replace" | grep -v grep | grep -v turbo-cam | awk -v t="$(date -u +%FT%.2TZ)" '{print t";"$0}' >> "$LOG"
  sleep 0.25
done
