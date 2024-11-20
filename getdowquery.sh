#/bin/bash

if [ -z "$1" ]
  then
        echo "Invalid channel. Provide a valid channel num."
  else
        set - $1
        DEVID=$(cat /home/beleaf/identifiers | head -$1 | tail -1)
fi

DOW=$(TZ='Asia/Jakarta' date "+%A")
DOW=$(echo $DOW | tr '[:upper:]' '[:lower:]')
STRING="starthour"
STARTHOUR=$(echo "$STRING" | tr 'h' 'H')
#echo "{\"dow\":\"$DOW\"}" | jq
echo "SELECT * FROM dosing_schedules WHERE identifier='$DEVID' AND is_enabled=true AND $DOW=true;"
