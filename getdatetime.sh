#/bin/bash

DATESTR=$(TZ='Asia/Jakarta' date "+%u %H %M %Z")
DOW=$(echo $DATESTR | awk '{print $1}')
HOU=$(echo $DATESTR | awk '{print $2}')
MIN=$(echo $DATESTR | awk '{print $3}')
#echo $DATESTR
echo "{\"dow\":$DOW,\"hour\":$HOU,\"minutes\":$MIN}" | jq

