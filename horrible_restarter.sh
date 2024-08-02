#!/usr/bin/env bash

logfile=$1
jobid=$2
maxage=$3

while true
do
    sleep `echo $maxage"/10" | bc`
    agecalc=`date +%s`-`stat -c %Y $logfile`
    age=`echo $agecalc | bc`
    if [ "$age" -gt "$maxage" ]
    then
        echo "Write has hung!"
        scancel $jobid
        exit
    fi
done
