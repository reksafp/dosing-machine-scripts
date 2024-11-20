#! /bin/bash

string="starhour"
startHour=$(echo "$string" | sed 's/h/H/')
echo "$startHour"
