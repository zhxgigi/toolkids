#!/bin/bash
set -e
set -o pipefail
startday="20120101"
endday="20120131"
date="$startday"
enddate=`date -d "+1 day $endday" +%Y%m%d`
while [[ $date < $enddate ]]
do
    date=`date -d "+1 day $date" +%Y%m%d`
    echo $date
done
