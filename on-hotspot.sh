#/bin/bash

nmcli con add type wifi ifname wlan0 con-name WS10F1D2_Local autoconnect yes ssid WS10F1D2_Local
nmcli con modify WS10F1D2_Local 802-11-wireless.mode ap 802-11-wireless.band bg ipv4.method shared
nmcli con modify WS10F1D2_Local wifi-sec.key-mgmt wpa-psk
nmcli con modify WS10F1D2_Local wifi-sec.psk "Beleafarmrb11"
nmcli con up WS10F1D2_Local
