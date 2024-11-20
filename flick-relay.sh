#/bin/bash

case $1 in
1)
  echo "Using Channel $1 on Modbus serial 0"
  ADAPTER=0
  OFFSET=0
  ;;
2)
  echo "Using Channel $1 on Modbus serial 0"
  ADAPTER=0
  OFFSET=4
  ;;
3)
  echo "Using Channel $1 on Modbus serial 1"
  ADAPTER=1
  OFFSET=0
  ;;
4)
  echo "Using Channel $1 on Modbus serial 1"
  ADAPTER=1
  OFFSET=4
  ;;
*)
  echo "Invalid channel choice"
  exit 1
esac

case $2 in
0)
  STATE="off"
  ;;
1)
  STATE="on"
  ;;
*)
  echo "Illegal relay state"
  exit 1
  ;;
esac

CHAN=$(($3+$OFFSET))
echo "Turning $STATE relay $CHAN on adapter $ADAPTER"
STATE=$(modpoll -b 9600 -p none -t 0 -1 -r $CHAN -c 1 /dev/ttyUSB$ADAPTER $2 | grep "Written")
echo $STATE
