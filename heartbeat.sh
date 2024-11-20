#/bin/bash

CPUTEMP=$(sensors | grep "Core 0:" | awk '{ print $3; }' | sed 's/[^0-9.]*//g')
#RSSI=$(iw dev wlan0 link | grep signal | awk '{print $2}')
RSSI=0
DISKUSE=$(df -hm | grep p2 | awk '{print $3}')
DISKTOT=$(df -hm | grep p2 | awk '{print $2}')
DISKPCT=$(df -hm | grep p2 | awk '{print $3 / $2 * 100}')
RAMUSE=$(free -m | grep Mem: | awk '{print $3}')
RAMTOT=$(free -m | grep Mem: | awk '{print $2}')
RAMPCT=$(free -m | grep Mem: | awk '{print $3/$2 * 100}')
UPTIME=$(uptime -p | awk '{print $2, $3, $4, $5, $6, $7}')
AVLOAD=$(uptime | awk '{print $8 $9 $10}')
TS=$(date)
echo "{\"cpu_temperature\":$CPUTEMP, \"rssi\":$RSSI, \"disk_use\":\"$DISKUSE/$DISKTOT ($DISKPCT%)\", \"ram_use\": \"$RAMUSE/$RAMTOT ($RAMPCT%)\", \"uptime\":\"$UPTIME\",\"avg_load\":\"$AVLOAD\", \"ts\": \"$TS\"}" | jq

