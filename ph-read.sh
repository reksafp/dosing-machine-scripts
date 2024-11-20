#/bin/bash

case $1 in
1)
#  echo "Reading pH probe #1 on adapter 0"
  ADAPTER=0
  ADDRESS=2
  ;;
2)
#  echo "Reading pH probe #2 on adapter 0"
  ADAPTER=0
  ADDRESS=5
  ;;
3)
#  echo "Reading pH probe #3 on adapter 1"
  ADAPTER=1
  ADDRESS=2
  ;;
4)
#  echo "Reading pH probe #4 on adapter 1"
  ADAPTER=1
  ADDRESS=5
  ;;
*)
  echo "Invalid channel choice"
  exit 1
esac

RAWRET=$(modpoll -b 9600 -p none -o 0.1 -t 4:hex -a $ADDRESS -1 -r 2 -c 4 /dev/ttyUSB$ADAPTER | awk -F '[' '{print $2}')
HIWORD=$(echo $RAWRET | awk '{print $4}')
LOWORD=$(echo $RAWRET | awk '{print $2}')
HITEMP=$(echo $RAWRET | awk '{print $8}')
LOTEMP=$(echo $RAWRET | awk '{print $6}')

#echo $RAWRET
PH=$(echo "${HIWORD##*0x}${LOWORD##*0x}" | python3 -c 'import struct; print(round(struct.unpack("!f", bytes.fromhex(input()))[0],2))')
TP=$(echo "${HITEMP##*0x}${LOTEMP##*0x}" | python3 -c 'import struct; print(round(struct.unpack("!f", bytes.fromhex(input()))[0],2))')

echo "ph_val: $PH"
echo "ph_tmp: $TP"
