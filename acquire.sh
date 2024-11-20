#/bin/bash

if [ -z "$1" ]
  then
    	echo "Invalid channel. Provide a valid channel num."
  else
	set - $1
	NUM=$1
	DEVID=$(cat /home/beleaf/identifiers | head -$1 | tail -1)

	RAWPH=$(/home/beleaf/latte-dosing-multi/scripts/ph-read.sh $1)
	PH=$(echo $RAWPH | awk '{print $2}')
	PT=$(echo $RAWPH | awk '{print $4}')

	EC_CMD="python3 /home/beleaf/latte-dosing-multi/scripts/ec-read-mod.py $1"
	#RAWEC=$(python3 /home/beleaf/latte-dosing-multi/scripts/ec-read.py)
	RAWEC=$(eval "$EC_CMD" | head)

#	echo $RAWEC

	EC=$(echo $RAWEC | awk '{print $16}')
	ET=$(echo $RAWEC | awk '{print $18}')
	SL=$(echo $RAWEC | awk '{print $20}')

	TP=$(bc -l <<< "scale=2; ($PT+$ET)/2")
	echo "{\"device_id\":\"$DEVID\",\"ph\":$PH,\"ec\":$EC,\"salinity\":$SL,\"water_temp\":$TP}" | jq
fi
